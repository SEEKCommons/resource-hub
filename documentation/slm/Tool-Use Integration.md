# Tool‑Use Integration

**Goal.** Give the SLM narrow, reliable “hands” for the few things our users actually need: run SPARQL, look up ORCID/DOIs, show Scholia summaries, and render tidy tables.

## Tools (minimal viable set)

1. `sparql_query`
    - Endpoint: `https://query.wikidata.org/sparql` (or Hub proxy)
    - Args: `{"template": "<name>", "params": {...}}`
    - Returns: `{"rows":[...], "columns":[...], "query": "<expanded sparql>", "source":"wikidata"}`
    - Templates (examples):
      - `author_topic_works(topic_qid, limit=20)`
      - `person_outputs(person_qid, type=[article,dataset,software])`
      - `initiative_network(initiative_qid, depth=2)`
      - `venue_recent(year_from, venue_qid)`
2. `doi_resolve`
    - Args: `{"doi":"10.5281/zenodo.12345"}`
    - `Returns: Bib metadata (title, creators, year, URL).`
    - Use: convert graph results into citeable lines.
3. `orcid_lookup`
    - Args: `{"orcid":"0000-0002-..."}`
    - Returns: works/affiliations minimal profile (cached).
    - Why: reinforces person identity & provenance paths emphasized in our planning and prep conversations (ORCID↔Wikidata↔Zenodo).
4. `scholia_card` (optional)
    - Args: `{"qid":"Qxxxx"}`
    - Returns: lightweight summary (topics, coauthors, venue counts) for quick context.

## Tool‑use prompt contract (excerpt)

```yaml
You may only call a tool when:
- You need structured results or citations.
- The user asked for data you cannot infer reliably.

Always:
- Prefer QIDs/IRIs when present.
- Return a short, source-backed answer + a compact table.
- Include a "How to reproduce" note with the SPARQL template name and parameters.
```

## Example end‑to‑end

**User:** “List recent open‑source tools our fellows published on urban heat islands.”

**Model → tool:**

```json
{"tool":"sparql_query","args":{"template":"author_topic_works","params":{"topic_qid":"Q754923"}}}
```

**Model ← tool result:** table of works + software tags + DOIs
Model answer: 3–6 bullets + citations (QIDs + DOIs) and a link to reproduce query.

## Observability & reliability

- Log template name + param hash + row count.
- Cache popular results for 60–90 minutes.
- Enforce rate limits & backoff for WDQS.
- If empty/timeout, the model must narrate what it tried and offer next steps (e.g., broaden topic or time window).

## Why RDF tools first?

Standards (IRIs, RDFS/OWL semantics, SPARQL) are what make cross‑team and cross‑partner federation feasible; attempting this with ad‑hoc property‑graph only stacks typically re‑implements RDF features later.