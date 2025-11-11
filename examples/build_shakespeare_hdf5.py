#!/usr/bin/env python3
"""
Persist a small vector database (text embeddings) to an HDF5 file.

What it does
------------
1) Downloads Shakespeare from Project Gutenberg (default: ebook #100 "The Complete Works").
2) Strips the Gutenberg header/footer.
3) Tokenizes and chunks the text to ~N tokens per chunk (overlap supported).
4) Embeds each chunk with a Sentence-Transformers model.
5) Writes an HDF5 file with:
   - /embeddings           float32 [N, D]
   - /embeddings_normed    float32 [N, D]    (L2-normalized for cosine search)
   - /texts                UTF-8 vlen string [N]
   - /doc_id               int32  [N]        (Gutenberg ID per chunk)
   - /title                UTF-8 vlen string [N]
   - /source_url           UTF-8 vlen string [N]
   - /start_token          int32  [N]
   - /end_token            int32  [N]
   - file attrs: model, model_dim, created_at, index_type, license_hint, etc.

It also supports query-time demo:
   python build_shakespeare_hdf5.py --out shakespeare.h5 --query "to be or not to be"

Notes
-----
- Text strings are stored as UTF-8 variable-length strings in HDF5.
- The "index" is a *flat cosine index* via normalized embeddings; this keeps dependencies light.
- For a production ANN, you could add FAISS/HNSW and serialize an index blob into HDF5.

"""

import argparse
import datetime as dt
import hashlib
import io
import os
import re
from typing import Iterable, List, Tuple

import numpy as np
import requests
import h5py
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer


# -------- Gutenberg download helpers --------

def candidate_gutenberg_urls(gutenberg_id: int) -> List[str]:
    """
    Generate a small set of canonical URL patterns that Project Gutenberg uses.
    We try a few common ones so this is resilient to minor hosting/layout changes.
    """
    gid = str(gutenberg_id)
    return [
        # New-style direct UTF-8 text endpoint:
        f"https://www.gutenberg.org/ebooks/{gid}.txt.utf-8",
        # Common 'files' layout with -0 meaning UTF-8 in many titles:
        f"https://www.gutenberg.org/files/{gid}/{gid}-0.txt",
        f"https://www.gutenberg.org/files/{gid}/{gid}.txt",
        # Legacy cache/epub layout:
        f"https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt",
        f"https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt.utf8",
    ]


def download_gutenberg_text(gutenberg_id: int, timeout: float = 30.0) -> Tuple[str, str]:
    """
    Try several URL patterns until one returns 200. Return (text, url_used).
    """
    last_err = None
    for url in candidate_gutenberg_urls(gutenberg_id):
        try:
            resp = requests.get(url, timeout=timeout)
            if resp.ok and resp.text:
                # Respect UTF-8 in-memory; requests decodes for us.
                return resp.text, url
        except Exception as e:
            last_err = e
    raise RuntimeError(f"Could not download Gutenberg ebook {gutenberg_id}. Last error: {last_err}")


def strip_gutenberg_boilerplate(text: str) -> str:
    """
    Remove the standard Project Gutenberg header and footer if present.
    Falls back gracefully if markers aren't found.
    """
    # Normalize line endings
    t = text.replace('\r\n', '\n').replace('\r', '\n')

    # Common start/end markers
    start_pat = re.compile(r'\*\*\* *START OF (THIS|THE) PROJECT GUTENBERG EBOOK.*?\n', re.IGNORECASE)
    end_pat   = re.compile(r'\*\*\* *END OF (THIS|THE) PROJECT GUTENBERG EBOOK.*?\n', re.IGNORECASE)

    start_match = start_pat.search(t)
    end_match   = end_pat.search(t)

    if start_match and end_match and end_match.start() > start_match.end():
        return t[start_match.end(): end_match.start()].strip()
    else:
        # If we don't detect markers, return as-is
        return t.strip()


# -------- Chunking with a tokenizer --------

def chunk_text_by_tokens(
    tokenizer,
    text: str,
    max_tokens: int = 256,
    stride: int = 64
) -> List[Tuple[str, int, int]]:
    """
    Chunk `text` using the provided HuggingFace tokenizer into overlapping windows.

    Returns a list of (chunk_text, start_token_idx, end_token_idx).
    """
    assert max_tokens > 0 and stride >= 0 and stride < max_tokens

    ids = tokenizer.encode(text, add_special_tokens=False)
    n = len(ids)
    chunks = []
    if n == 0:
        return chunks

    step = max_tokens - stride
    for start in range(0, n, step):
        end = min(start + max_tokens, n)
        piece_ids = ids[start:end]
        piece_text = tokenizer.decode(piece_ids, clean_up_tokenization_spaces=True)
        chunks.append((piece_text, start, end))
        if end >= n:
            break
    return chunks


# -------- Embedding and persistence --------

def embed_texts(
    model: SentenceTransformer,
    texts: List[str],
    batch_size: int = 64,
    show_progress: bool = True
) -> np.ndarray:
    """
    Compute embeddings (float32) for a list of texts with batching.
    """
    # encode returns float32 numpy by default when convert_to_numpy=True
    emb = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=show_progress,
        convert_to_numpy=True,
        normalize_embeddings=False
    )
    # Ensure numpy float32
    if emb.dtype != np.float32:
        emb = emb.astype(np.float32, copy=False)
    return emb


def l2_normalize_rows(x: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    norms = np.linalg.norm(x, axis=1, keepdims=True)
    norms = np.maximum(norms, eps)
    return x / norms


def persist_to_hdf5(
    out_path: str,
    embeddings: np.ndarray,
    embeddings_normed: np.ndarray,
    texts: List[str],
    doc_ids: List[int],
    titles: List[str],
    source_urls: List[str],
    start_tokens: List[int],
    end_tokens: List[int],
    model_name: str,
    model_dim: int,
    license_hint: str,
) -> None:
    """
    Write all arrays and UTF-8 metadata to an HDF5 file.
    """
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)

    str_dtype = h5py.string_dtype(encoding='utf-8')
    now = dt.datetime.utcnow().isoformat() + "Z"

    with h5py.File(out_path, "w") as f:
        # Core vectors
        f.create_dataset(
            "embeddings", data=embeddings, dtype=np.float32,
            compression="gzip", compression_opts=4,
            chunks=(min(embeddings.shape[0], 1024), embeddings.shape[1])
        )
        f.create_dataset(
            "embeddings_normed", data=embeddings_normed, dtype=np.float32,
            compression="gzip", compression_opts=4,
            chunks=(min(embeddings_normed.shape[0], 1024), embeddings_normed.shape[1])
        )

        # Text + metadata (variable-length UTF-8 strings cannot be compressed by HDF5)
        f.create_dataset("texts", data=np.array(texts, dtype=object), dtype=str_dtype)
        f.create_dataset("title", data=np.array(titles, dtype=object), dtype=str_dtype)
        f.create_dataset("source_url", data=np.array(source_urls, dtype=object), dtype=str_dtype)
        f.create_dataset("doc_id", data=np.asarray(doc_ids, dtype=np.int32))
        f.create_dataset("start_token", data=np.asarray(start_tokens, dtype=np.int32))
        f.create_dataset("end_token", data=np.asarray(end_tokens, dtype=np.int32))

        # File-level attributes for provenance
        f.attrs["created_at_utc"] = now
        f.attrs["embedding_model"] = model_name
        f.attrs["embedding_dim"] = int(model_dim)
        f.attrs["index_type"] = "flat_cosine"  # cosine via dot(q, embeddings_normed.T)
        f.attrs["license_hint"] = license_hint
        f.attrs["about"] = (
            "Vector DB persisted in HDF5: embeddings, a flat cosine index (normalized vectors), "
            "and UTF-8 metadata for each chunk."
        )


# -------- Query demo (nearest neighbors using the flat cosine index) --------

def topk_cosine_from_hdf5(
    h5_path: str,
    model: SentenceTransformer,
    query: str,
    k: int = 5
):
    with h5py.File(h5_path, "r") as f:
        emb_normed = f["embeddings_normed"][:]      # [N, D]
        texts = f["texts"][:]
        titles = f["title"][:]
        source_urls = f["source_url"][:]

        # Encode query and normalize
        q = model.encode([query], convert_to_numpy=True, normalize_embeddings=False).astype(np.float32)[0]
        q = q / max(np.linalg.norm(q), 1e-12)

        # Cosine similarity == dot product for normalized vectors
        sims = emb_normed @ q
        idx = np.argpartition(sims, -k)[-k:]
        idx = idx[np.argsort(-sims[idx])]

        results = []
        for i in idx:
            results.append({
                "score": float(sims[i]),
                "title": str(titles[i]),
                "source_url": str(source_urls[i]),
                "text": str(texts[i])
            })
        return results


# -------- CLI --------

def main():
    parser = argparse.ArgumentParser(description="Persist Shakespeare embeddings to HDF5 (vector DB demo).")
    parser.add_argument("--gutenberg-id", type=int, default=100,
                        help="Project Gutenberg ebook ID to download (default: 100, 'Complete Works').")
    parser.add_argument("--title", type=str, default="The Complete Works of William Shakespeare",
                        help="Human-readable title to store with chunks.")
    parser.add_argument("--out", type=str, default="data/shakespeare.h5", help="Output HDF5 path.")
    parser.add_argument("--model", type=str, default="sentence-transformers/all-MiniLM-L6-v2",
                        help="Sentence-Transformers model name.")
    parser.add_argument("--max-tokens", type=int, default=256, help="Tokens per chunk.")
    parser.add_argument("--stride", type=int, default=64, help="Token overlap between chunks.")
    parser.add_argument("--batch", type=int, default=64, help="Embedding batch size.")
    parser.add_argument("--no-progress", action="store_true", help="Disable progress bars.")
    parser.add_argument("--query", type=str, default=None,
                        help="If provided, will run a demo top-K search from the saved HDF5.")
    parser.add_argument("--topk", type=int, default=5, help="Top-K results to return for --query.")
    args = parser.parse_args()

    # Download text
    print(f"Downloading Gutenberg ebook #{args.gutenberg_id} ...")
    raw_text, url_used = download_gutenberg_text(args.gutenberg_id)
    cleaned = strip_gutenberg_boilerplate(raw_text)

    # Model + tokenizer
    print(f"Loading embedding model: {args.model}")
    model = SentenceTransformer(args.model)
    try:
        hf_tokenizer = AutoTokenizer.from_pretrained(args.model)
    except Exception:
        # Fallback: use the internal tokenizer if exposed, else a BERT base tokenizer
        hf_tokenizer = getattr(model, "tokenizer", AutoTokenizer.from_pretrained("bert-base-uncased"))

    # Chunking
    print(f"Chunking text (max_tokens={args.max_tokens}, stride={args.stride}) ...")
    chunks = chunk_text_by_tokens(hf_tokenizer, cleaned, max_tokens=args.max_tokens, stride=args.stride)

    if len(chunks) == 0:
        raise RuntimeError("No chunks produced; check tokenizer/model choice or input text.")

    texts = [c[0] for c in chunks]
    start_tokens = [c[1] for c in chunks]
    end_tokens = [c[2] for c in chunks]
    doc_ids = [args.gutenberg_id] * len(chunks)
    titles = [args.title] * len(chunks)
    source_urls = [url_used] * len(chunks)

    print(f"Embedding {len(texts)} chunks ...")
    embeddings = embed_texts(model, texts, batch_size=args.batch, show_progress=not args.no_progress)
    embeddings_normed = l2_normalize_rows(embeddings)

    # License note to store (for your README/workshop talk track)
    license_hint = (
        "Project Gutenberg public domain texts. See the Gutenberg site for terms "
        "and keep headers/attribution when redistributing."
    )

    # Persist to HDF5
    print(f"Writing HDF5 to {args.out} ...")
    persist_to_hdf5(
        out_path=args.out,
        embeddings=embeddings,
        embeddings_normed=embeddings_normed,
        texts=texts,
        doc_ids=doc_ids,
        titles=titles,
        source_urls=source_urls,
        start_tokens=start_tokens,
        end_tokens=end_tokens,
        model_name=args.model,
        model_dim=embeddings.shape[1],
        license_hint=license_hint,
    )

    print("Done.")

    # Optional live query demo
    if args.query:
        print(f"\nQuery: {args.query}")
        results = topk_cosine_from_hdf5(args.out, model, args.query, k=args.topk)
        for i, r in enumerate(results, 1):
            snippet = r["text"].replace("\n", " ")
            if len(snippet) > 220:
                snippet = snippet[:217] + "..."
            print(f"\n[{i}] score={r['score']:.3f}")
            print(f"   title     : {r['title']}")
            print(f"   source    : {r['source_url']}")
            print(f"   chunk text: {snippet}")


if __name__ == "__main__":
    main()
