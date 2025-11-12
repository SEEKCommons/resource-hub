#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shakespeare embeddings → HDF5 “vector DB” with play/sonnet metadata + query

Usage:
  # 1) Build once (skips if file already exists)
  python shakespeare_hdf5_vectors.py build --out shakespeare.h5

  # Force rebuild
  python shakespeare_hdf5_vectors.py build --out shakespeare.h5 --rebuild

  # 2) List works
  python shakespeare_hdf5_vectors.py list-works --h5 shakespeare.h5

  # 3) Query globally
  python shakespeare_hdf5_vectors.py query --h5 shakespeare.h5 --text "to be or not to be" --top-k 10

  # 4) Query within a specific work (title substring match, e.g. "Macbeth")
  python shakespeare_hdf5_vectors.py query --h5 shakespeare.h5 --text "dagger" --work "Macbeth" --top-k 5
"""

import argparse
import datetime as dt
import io
import os
import re
import sys
from typing import List, Tuple, Dict, Optional

import numpy as np
import requests
import h5py
from tqdm import tqdm

# Tokenizer for chunking by tokens
from transformers import AutoTokenizer
# Sentence-level embeddings (compact, 384-dim; suitable for semantic search)
from sentence_transformers import SentenceTransformer


# -----------------------------
# 1) Download & clean Gutenberg
# -----------------------------
GUTENBERG_URLS = [
    # Common modern “-0” UTF-8 edition
    "https://www.gutenberg.org/files/100/100-0.txt",
    # Historic cache path
    "https://www.gutenberg.org/cache/epub/100/pg100.txt",
    # Alternate mirrors (kept for robustness)
    "https://www.gutenberg.org/cache/epub/100/pg100.txt.utf8",
]

START_MARK = "*** START OF THE PROJECT GUTENBERG EBOOK"
END_MARK = "*** END OF THE PROJECT GUTENBERG EBOOK"

def download_shakespeare_text(timeout=30) -> str:
    last_err = None
    for url in GUTENBERG_URLS:
        try:
            r = requests.get(url, timeout=timeout)
            if r.ok and r.text and len(r.text) > 100000:
                text = r.text
                # Trim Gutenberg header/footer if present
                start = text.find(START_MARK)
                end = text.find(END_MARK)
                if start != -1 and end != -1 and end > start:
                    text = text[start:end]
                    # Drop the START line itself
                    text = "\n".join(text.splitlines()[1:])
                return text
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(f"Failed to download Shakespeare text. Last error: {last_err}")


# ----------------------------------------------------
# 2) Split into works (plays) and individual sonnets
# ----------------------------------------------------
# We locate top-level uppercase headings for plays/sections.
# For “THE SONNETS”, we further split on Roman-numeral headings.
PLAY_TITLE_PATTERNS = [
    r"THE TRAGEDY OF [A-Z ,\-\.’'&]+",
    r"THE COMEDY OF [A-Z ,\-\.’'&]+",
    r"THE HISTOR(Y|IES) OF [A-Z ,\-\.’'&]+",
    r"THE LIFE (?:AND DEATH )?OF KING [A-Z IVX]+",
    r"THE LIFE OF TIMON OF ATHENS",
    r"PERICLES, PRINCE OF TYRE",
    r"THE TWO NOBLE KINSMEN",
    r"THE WINTER'S TALE",
    r"A MIDSUMMER(?:-NIGHT'S| NIGHT'S)? DREAM",
    r"LOVE'S LABOU?R'?S LOST",
    r"MUCH ADO ABOUT NOTHING",
    r"MEASURE FOR MEASURE",
    r"ALL'S WELL THAT ENDS WELL",
    r"AS YOU LIKE IT",
    r"TWELFTH NIGHT(?:; OR, WHAT YOU WILL)?",
    r"THE MERCHANT OF VENICE",
    r"THE MERRY WIVES OF WINDSOR",
    r"THE TAMING OF THE SHREW",
    r"THE TWO GENTLEMEN OF VERONA",
    r"THE TEMPEST",
    r"(?:THE TRAGEDY OF )?HAMLET, PRINCE OF DENMARK",
    r"(?:THE TRAGEDY OF )?OTHELLO, THE MOOR OF VENICE",
    r"(?:THE TRAGEDY OF )?MACBETH",
    r"(?:THE TRAGEDY OF )?KING LEAR",
    r"(?:THE TRAGEDY OF )?ROMEO AND JULIET",
    r"(?:THE TRAGEDY OF )?JULIUS CAESAR",
    r"(?:THE TRAGEDY OF )?ANTONY AND CLEOPATRA",
    r"(?:THE TRAGEDY OF )?CORIOLANUS",
    r"(?:THE TRAGEDY OF )?TITUS ANDRONICUS",
    r"CYMBELINE",
    r"TROILUS AND CRESSIDA",
    r"(?:THE LIFE AND DEATH OF )?KING JOHN",
    r"(?:THE TRAGEDY OF )?KING RICHARD II",
    r"(?:THE FIRST PART OF )?KING HENRY IV",
    r"(?:THE SECOND PART OF )?KING HENRY IV",
    r"(?:THE LIFE OF )?KING HENRY V",
    r"(?:THE TRAGEDY OF )?KING RICHARD III",
    r"(?:THE FIRST PART OF )?KING HENRY VI",
    r"(?:THE SECOND PART OF )?KING HENRY VI",
    r"(?:THE THIRD PART OF )?KING HENRY VI",
    r"(?:THE )?SONNETS",
    r"VENUS AND ADONIS",
    r"THE RAPE OF LUCRECE",
    r"THE PASSIONATE PILGRIM",
    r"A LOVER'S COMPLAINT",
]

PLAY_TITLE_RE = re.compile(r"^(?:" + r"|".join(PLAY_TITLE_PATTERNS) + r")\s*$")

ROMAN_RE = re.compile(r"^\s*[IVXLCDM]+\s*$")

def split_works(text: str) -> List[Tuple[str, str]]:
    """
    Returns a list of (title, body) tuples.
    For SONNETS: returns 154 entries "Sonnet I", ..., splitting by Roman numerals.
    """
    lines = text.splitlines()
    # Identify candidate top headings (all-caps-ish lines)
    headings = []
    for i, line in enumerate(lines):
        L = line.strip()
        if not L:
            continue
        if L.upper() == L and PLAY_TITLE_RE.match(L):
            headings.append((i, L))

    # Build coarse sections between headings
    sections = []
    for idx, (line_no, title) in enumerate(headings):
        start = line_no + 1
        end = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
        body = "\n".join(lines[start:end]).strip()
        sections.append((title, body))

    works: List[Tuple[str, str]] = []
    for title, body in sections:
        if "SONNETS" in title:
            # Further split into individual sonnets by Roman numeral headings on their own lines
            son_lines = body.splitlines()
            son_positions = []
            for i, l in enumerate(son_lines):
                if ROMAN_RE.match(l.strip()):
                    son_positions.append((i, l.strip()))
            # Pair up into (start, end)
            for j, (pos, roman) in enumerate(son_positions):
                start = pos + 1
                end = son_positions[j + 1][0] if j + 1 < len(son_positions) else len(son_lines)
                son_body = "\n".join(son_lines[start:end]).strip()
                if son_body:
                    works.append((f"Sonnet {roman}", son_body))
        else:
            works.append((title.title(), body))
    return works


# ----------------------------------------
# 3) Chunking by tokens (for embedding)
# ----------------------------------------
def chunk_by_tokens(
    tokenizer: AutoTokenizer,
    text: str,
    max_tokens: int = 256,
    overlap: int = 32
) -> List[str]:
    """
    Split text into chunks by tokenizer length; return decoded strings.
    """
    ids = tokenizer.encode(text, add_special_tokens=False)
    if not ids:
        return []
    chunks = []
    step = max_tokens - overlap if max_tokens > overlap else max_tokens
    for start in range(0, len(ids), step):
        window = ids[start : start + max_tokens]
        if not window:
            break
        chunk_text = tokenizer.decode(window, skip_special_tokens=True)
        chunk_text = chunk_text.strip()
        if chunk_text:
            chunks.append(chunk_text)
    return chunks


# ----------------------------------------
# 4) Embedding model helper
# ----------------------------------------
def get_embedder(name: str = "sentence-transformers/all-MiniLM-L6-v2") -> SentenceTransformer:
    return SentenceTransformer(name)

def embed_texts(embedder: SentenceTransformer, texts: List[str], batch_size: int = 64) -> np.ndarray:
    vecs = embedder.encode(texts, batch_size=batch_size, show_progress_bar=True, normalize_embeddings=True)
    # ensure float32
    return np.asarray(vecs, dtype=np.float32)


# ----------------------------------------
# 5) HDF5 layout & write
# ----------------------------------------
def write_hdf5(
    h5_path: str,
    all_chunks: List[str],
    all_work_ids: List[int],
    embeddings: np.ndarray,
    works_index: List[Dict[str, object]],
    meta: Dict[str, str],
):
    assert len(all_chunks) == embeddings.shape[0] == len(all_work_ids)
    N, D = embeddings.shape

    # variable-length UTF-8 string dtype
    vlen_str = h5py.string_dtype("utf-8")

    with h5py.File(h5_path, "w") as h5:
        # /meta as attributes on a group
        gmeta = h5.create_group("meta")
        for k, v in meta.items():
            gmeta.attrs[k] = v

        # /chunks group
        gchunks = h5.create_group("chunks")
        gchunks.create_dataset(
            "text",
            data=np.array(all_chunks, dtype=object),
            dtype=vlen_str,
            chunks=True,
            compression="gzip",
            compression_opts=4,
        )
        gchunks.create_dataset(
            "work_id",
            data=np.asarray(all_work_ids, dtype=np.int32),
            dtype=np.int32,
            chunks=True,
            compression="gzip",
            compression_opts=4,
        )
        gchunks.create_dataset(
            "embedding",
            data=embeddings,  # already normalized
            dtype=np.float32,
            chunks=True,
            compression="gzip",
            compression_opts=4,
        )

        # /works group with a compact index table
        gworks = h5.create_group("works")
        dt = np.dtype(
            [
                ("work_id", np.int32),
                ("title", vlen_str),
                ("start_row", np.int64),
                ("end_row", np.int64),  # exclusive
            ]
        )
        rows = np.empty(len(works_index), dtype=dt)
        for i, rec in enumerate(works_index):
            rows[i] = (
                np.int32(rec["work_id"]),
                rec["title"],
                np.int64(rec["start_row"]),
                np.int64(rec["end_row"]),
            )
        gworks.create_dataset(
            "index",
            data=rows,
            dtype=dt,
            chunks=True,
            compression="gzip",
            compression_opts=4,
        )


# ----------------------------------------
# 6) Builder (idempotent unless --rebuild)
# ----------------------------------------
def build_if_missing(out_path: str, rebuild: bool = False):
    if os.path.exists(out_path) and not rebuild:
        print(f"[build] HDF5 already exists at {out_path}. Skipping regeneration.")
        return

    print("[build] Downloading Shakespeare from Project Gutenberg…")
    text = download_shakespeare_text()

    print("[build] Splitting into works (plays + individual sonnets)…")
    works = split_works(text)  # List[ (title, body) ]
    print(f"[build] Found {len(works)} works.")

    # Prepare tokenizer & embedder
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    embedder = get_embedder()

    # Chunk, track per-work ranges
    all_chunks: List[str] = []
    all_work_ids: List[int] = []
    works_index: List[Dict[str, object]] = []
    row_cursor = 0

    for work_id, (title, body) in enumerate(tqdm(works, desc="Chunking works")):
        chunks = chunk_by_tokens(tokenizer, body, max_tokens=256, overlap=32)
        if not chunks:
            continue
        start_row = row_cursor
        all_chunks.extend(chunks)
        all_work_ids.extend([work_id] * len(chunks))
        row_cursor += len(chunks)
        works_index.append(
            dict(
                work_id=work_id,
                title=title,
                start_row=start_row,
                end_row=row_cursor,  # exclusive
            )
        )

    print(f"[build] Total chunks: {len(all_chunks)}")

    print("[build] Embedding chunks (L2-normalized)…")
    embeddings = embed_texts(embedder, all_chunks, batch_size=64)  # (N, D)

    meta = {
        "created_at": dt.datetime.utcnow().isoformat() + "Z",
        "source": ",".join(GUTENBERG_URLS),
        "tokenizer": "bert-base-uncased",
        "embedder": "sentence-transformers/all-MiniLM-L6-v2",
        "embed_dim": str(embeddings.shape[1]),
        "chunking": "max_tokens=256,overlap=32 (BERT tokenizer)",
        "note": "Embeddings are unit-normalized; cosine ~ dot product",
    }

    print(f"[build] Writing HDF5 → {out_path}")
    write_hdf5(
        h5_path=out_path,
        all_chunks=all_chunks,
        all_work_ids=all_work_ids,
        embeddings=embeddings,
        works_index=works_index,
        meta=meta,
    )
    print("[build] Done.")


# ----------------------------------------
# 7) Query (cosine similarity, optional work filter)
# ----------------------------------------
def load_works_index(h5: h5py.File) -> List[Dict[str, object]]:
    idx = h5["works/index"]
    out = []
    for row in idx:
        out.append(
            dict(
                work_id=int(row["work_id"]),
                title=str(row["title"]),
                start_row=int(row["start_row"]),
                end_row=int(row["end_row"]),
            )
        )
    return out

def find_work_rows(works_index: List[Dict[str, object]], title_substring: str) -> Optional[Tuple[int, int]]:
    q = title_substring.lower()
    for rec in works_index:
        if q in rec["title"].lower():
            return (rec["start_row"], rec["end_row"])
    return None

def query_hdf5(
    h5_path: str,
    query_text: str,
    top_k: int = 5,
    work_filter: Optional[str] = None,
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> List[Dict[str, object]]:
    """
    Returns: list of {rank, score, row, work_id, work_title, text}
    """
    if not os.path.exists(h5_path):
        raise FileNotFoundError(h5_path)

    # Load model for the query vector (tiny, fast)
    embedder = get_embedder(model_name)
    qv = embedder.encode([query_text], normalize_embeddings=True)
    qv = qv.astype(np.float32)[0]  # (D,)

    with h5py.File(h5_path, "r") as h5:
        embs = h5["chunks/embedding"]    # (N, D) normalized
        texts = h5["chunks/text"]        # (N,)
        work_ids = h5["chunks/work_id"]  # (N,)
        works_idx = load_works_index(h5)

        # Optional restrict to a single work
        if work_filter:
            bounds = find_work_rows(works_idx, work_filter)
            if not bounds:
                raise ValueError(f'No work with title containing "{work_filter}"')
            lo, hi = bounds
            rows = np.arange(lo, hi, dtype=np.int64)
        else:
            rows = np.arange(embs.shape[0], dtype=np.int64)

        # Cosine similarity = dot product (embeddings are unit normalized)
        # To avoid loading full matrix at once for very large N, do in blocks:
        block = 131072  # 128k rows per block
        scores = np.empty(rows.shape[0], dtype=np.float32)
        for i in range(0, rows.shape[0], block):
            sl = rows[i : i + block]
            M = np.asarray(embs[sl, :], dtype=np.float32)  # (B, D)
            scores[i : i + len(sl)] = M @ qv  # dot product

        # Top-k
        k = min(top_k, scores.shape[0])
        # argpartition for efficiency
        idx = np.argpartition(-scores, k - 1)[:k]
        # sort exact
        idx = idx[np.argsort(-scores[idx])]

        results = []
        for rank, i_local in enumerate(idx, start=1):
            row = int(rows[i_local])
            score = float(scores[i_local])
            wid = int(work_ids[row])
            # map work_id→title quickly:
            wtitle = next((rec["title"] for rec in works_idx if rec["work_id"] == wid), f"work_id={wid}")
            results.append(
                dict(
                    rank=rank,
                    score=score,
                    row=row,
                    work_id=wid,
                    work_title=wtitle,
                    text=str(texts[row]),
                )
            )
        return results


# ----------------------------------------
# 8) CLI
# ----------------------------------------
def cli():
    p = argparse.ArgumentParser(description="Shakespeare → HDF5 vector DB (+ query)")
    sub = p.add_subparsers(dest="cmd", required=True)

    pb = sub.add_parser("build", help="Build the HDF5 (skips if exists unless --rebuild)")
    pb.add_argument("--out", required=True, help="Output HDF5 path")
    pb.add_argument("--rebuild", action="store_true", help="Force rebuild if file exists")

    pl = sub.add_parser("list-works", help="List works from an existing HDF5")
    pl.add_argument("--h5", required=True, help="Path to HDF5")

    pq = sub.add_parser("query", help="Query an existing HDF5 (cosine similarity)")
    pq.add_argument("--h5", required=True)
    pq.add_argument("--text", required=True, help="Query text")
    pq.add_argument("--work", default=None, help='Restrict to a work (title substring), e.g. "Macbeth"')
    pq.add_argument("--top-k", type=int, default=5)
    pq.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2",
                    help="Embedding model for the query (defaults to the one used at build time)")

    args = p.parse_args()

    if args.cmd == "build":
        build_if_missing(args.out, rebuild=args.rebuild)

    elif args.cmd == "list-works":
        if not os.path.exists(args.h5):
            print(f"File not found: {args.h5}", file=sys.stderr)
            sys.exit(1)
        with h5py.File(args.h5, "r") as h5:
            rows = load_works_index(h5)
        print(f"{'ID':>4} | {'Start':>7} | {'End':>7} | Title")
        print("-" * 80)
        for rec in rows:
            print(f"{rec['work_id']:>4} | {rec['start_row']:>7} | {rec['end_row']:>7} | {rec['title']}")

    elif args.cmd == "query":
        results = query_hdf5(args.h5, args.text, top_k=args.top_k, work_filter=args.work, model_name=args.model)
        for r in results:
            print(f"[{r['rank']:>2}] score={r['score']:.4f} row={r['row']} work_id={r['work_id']} title={r['work_title']}")
            # Truncate snippet for display
            snip = r["text"].replace("\n", " ")
            print("     ", (snip[:180] + "…") if len(snip) > 180 else snip)

if __name__ == "__main__":
    cli()