# Supervised Fine-Tuning (SFT) Plan
**Objective.** Teach the model to (a) answer SEEKCommons questions with sources, (b) use the Hub’s entities/relations consistently (IRIs/Q‑IDs), and (c) translate natural‑language questions into graph queries and interpretations. This leans on RDF identity + semantics so the model stops guessing and starts following links.

## Scope & priority intents

1. **Who/what/where** over the network (people, projects, software, venues).
2. **Provenance‑first** answers (always show where a fact came from).
3. **Graph thinking:** explain a result path (“X → authored → Y → presented at → Z”).
4. **Query translation:** NL → parameterized SPARQL template (then explain results in plain English).
5. **Ethical/care language** when data are partial/contested.

## Data sources for SFT (supervised fine‑tuning)

- Seed QA & task templates derived from Day‑1/Day‑2 workshop goals (e.g., “Which resources align to topic X?”, “Which fellows are linked to Y?”).-These are already enumerated in the workshop agenda and are ideal for instruction pairs.
- Wikidata items + Scholia pages for fellows, venues, grants, software; use Q‑IDs as ground truth labels. (Scholia screenshots/JSON excerpts become references for explanations.)
- ORCID & Zenodo records (IDs, titles, DOIs) curated during prep; include examples that link persons→works→datasets→software so the model learns identity linking patterns.

## Annotation format

Each training example is a JSONL item with:

```json
{
  "input": "Find open datasets related to microclimate modeling by SEEKCommons fellows and show sources.",
  "tools_allowed": ["sparql_query", "doi_resolve", "orcid_lookup"],
  "gold_thought": [
    "Map 'microclimate' to P921 topic Q1143079",
    "Query: fellow → author of work → has topic microclimate → has dataset DOI",
    "Return top 10 with item labels and references"
  ],
  "gold_actions": [
    {"tool": "sparql_query", "args": {"template": "author_topic_dataset", "topic_qid": "Q1143079"}}
  ],
  "gold_output": {
    "answer": "...plain‑English synthesis with caveats...",
    "citations": ["wd:Qxxx", "doi:10.xxxx/zenodo.xxxx", "scholia:author/Qyyy"]
  }
}
```
## Templates the model must master

- **Identify & disambiguate** (“Which ‘Alice Johnson’?” → prefer ORCID‑linked entity).
- **Explain inference** with RDFS/OWL logic (“worksFor ⇒ Person/Organization; locatedIn is transitive”). Keep explanations short but accurate.
- **State limits** (“This hub tracks open resources; private/internal outputs may be missing”).

## Quantity & mix (v0.1)

- 1,200–2,000 instruction items total
  - 40% hub discovery (who/what/where)
  - 35% query translation + explanation
  - 15% data stewardship/ethics responses
  - 10% error‑handling (rate limits, empty results)

## Training recipe (high‑level)

- Base: a compact 3–8B open model with strong tool‑call formatting.
- SFT: 2–3 epochs, cosine decay LR, batch 128–256 seqs @ 4k ctx.
- Guardrails: always require attribution fields in answers; fail closed on missing sources.

## Deliverables

- `seekcommons-sft-v0.1.jsonl` (curated set)
- Prompt schemas + 10 canonical SPARQL templates
- A mini model card (purpose, data, risks, metrics, license)

**Rationale.** Teaching the model to treat identities (IRIs/Q‑IDs) as the answer reduces ambiguity and compounds accuracy on traversals—exactly the advantage RDF brings as a knowledge layer for AI.