# SEEKCommons Small Language Model (SLM)

A compact, instruction‑tuned model that is *grounded* in the SEEKCommons Resource Hub knowledge graph (KG) and *augmented* with tools (predefined SPARQL/query endpoints, Scholia views, simple KG validators), so it can answer community questions with low hallucination and clear sources. The KG/semantic layer is the secret sauce—LLMs are far more accurate when they traverse explicit identities and relationships instead of guessing them.

## Scope, users, and success

**Users:** fellows, program staff, partners, librarians/data stewards.

**Top tasks:** answer “top 5 questions the community most wants the Hub to answer,” produce quick author/topic/venue reports, and expose query endpoints non‑coders can run. Track friction points for contribution, quality, and reuse.

**Success (examples):**

- ≥90% of “top 50” FAQs correctly answered with cited sources from the Hub/Wikidata.
- Tool‑use works for common flows (e.g., “author‑topic report” → JSON/CSV → chart) without making users write SPARQL.
- The SLM proactively suggests contribution improvements (e.g., “add your ORCID / link your Zenodo DOI”) and explains why that helps discovery.

## A model grounded in the knowledge layer

1. **Use RDF with IRIs.** Model people, organizations, projects, venues, software, datasets, grants with global identifiers (Wikidata Q‑IDs/ORCID/DOI). This reduces ambiguity and enables federation across partners and public data.
2. **Add light semantics (RDFS/OWL).** Even a little semantics (domain/range, subclass, inverse, transitivity) yields type inference and safer navigation (e.g., worksFor implies employs, locatedIn is transitive). This lets the SLM rely on deterministic reasoning rather than pattern‑matching guesses.
3. **Prefer standards for interoperability.** If property‑graph convenience is needed, keep RDF as the canonical exchange layer; standards win as soon as you need federation, external ontologies, or cross‑vendor queries.

Why this matters for the SLM: LLMs perform dramatically better when identities/relations are explicit (KG) rather than implied by column names or ad‑hoc schemas.

## Tools the SLM can call

Use tools so the (small) model stays lightweight while answers come from live, governed sources.

**Core tools the SLM should know:**

- `hub_query()` – a *parameterized* HTTP endpoint (AWS Lambda) that executes vetted SPARQL templates over the Resource Hub/Wikidata and returns JSON/CSV. (Exposes “query objects” so non‑experts don’t write SPARQL.)
- `scholia_profile()` – fetch prebuilt Scholia views (author/topic/venue) for quick visual exploration/explanation.
- `notebook_runner()` (optional) – a trigger or link to run a Jupyter template that: SPARQLWrapper → pandas → chart/CSV; good for reproducible analyses.
- `validate_kg_slice()` (optional) – run simple SHACL/consistency checks for a small subgraph to catch obvious issues before surfacing results (ties to OWL/RDFS constraints).

**Contribution helpers the SLM should recommend (not necessarily call):**

- **ORCID:** encourage users to maintain clean profiles; it’s the lowest‑friction start for identity and publications.
- **Zenodo/DOIs:** suggest minting DOIs for datasets/software (even placeholders) to improve discoverability and linking. (This “identity first, then linking” path is what users understand fastest.)

## Instruction/SFT dataset (the core of the SLM)

Create high‑quality, **tool‑using** instruction examples that reflect the community’s real needs (so the model learns when and how to call which tool). Start from workshop materials and transcripts, and from the “top questions” you already captured.

**Buckets of training examples:**

1. **FAQ → tool calls with citations.**
   - “Which SEEKCommons fellows are connected to topic X and in which venues?” → `hub_query(topic="X")` → summarize + cite items (Q‑IDs/URLs).
2. **How‑to contribution flows.**
   - *“How do I add my software so it shows up in the Hub?”* → steps: ORCID ↔ Zenodo DOI ↔ reconciliation to Wikidata; explain benefits.
3. **Explain a SPARQL result in plain language.** 
   - Given a JSON result from `hub_query`, the SLM explains it and offers next‑step visualizations (Scholia / notebook).
4. **Guardrails via semantics.**
   - Examples where the SLM defers to the validator (e.g., disallows impossible type mixes, suggests fixing a missing range/domain).
5. **Brainstorming partner prompts** (to help users refine questions and analyses)—short, conversational patterns the SLM can use to co‑develop a query/report with a user.

**One concrete SFT example (simplified):**

- **User:** “List UVA‑affiliated fellows working on ‘knowledge graphs’ and where they publish.”
- **Assistant (plan):** Call hub_query with `affiliation="University of Virginia", topic="knowledge graphs"`. On success, summarize, then offer Scholia links.
- **Assistant (tool call):** `hub_query({"affiliation": "Q49115", "topic": "knowledge graph"})`
- **Assistant (final):** Summarized list with per‑person venues + *source Q‑IDs and DOIs cited inline;* “Open in Scholia” buttons.

## A base SLM + fine‑tune

Pick a *small* open model (≈3B–8B) suitable for on‑prem or modest cloud; apply [**parameter‑efficient** fine‑tuning (LoRA/QLoRA)](https://www.mercity.ai/blog-post/guide-to-fine-tuning-llms-with-lora-and-qlora) on your curated instruction set so it learns:

- the SEEKCommons vocabulary and entities,
- *when to call which tool,*
- how to *always* provide sources and avoid speculation.

Optionally add [**DPO/RLHF**](https://arxiv.org/abs/2305.18290) with small batches of real conversations from pilots/workshops to reinforce helpfulness, correctness, and proper tool‑use (e.g., prefer `hub_query` over guessing).

## Automation

Build a simple harness that:

- Replays the “top 50” questions as prompts and checks:
(a) **tool correctness** (right endpoint/parameters?), (b) **retrieval accuracy** versus expected KG slices, (c) **citation presence**.
- Runs **semantic sanity checks** (e.g., inferred types/relations are consistent with RDFS/OWL expectations) on the returned subgraph.
- Includes **human spot‑checks** from workshop scribes (“Does this answer the question we meant?”), which you already planned to capture.

## MVP

Deliver three things together (so anyone can use the SLM without writing SPARQL):

1. **Chat endpoint** with tool bindings (the SLM). System prompt instructs: *prefer tools → cite sources → explain tradeoffs → suggest ORCID/Zenodo links if data is missing.*
2. **Query objects API** (Lambda) exposing the 10–15 most useful reports (e.g., author‑topic, venue landscape, initiative connections), returning JSON/CSV ready for Sheets/Notebooks.
3. **Scholia + Notebook templates.** Buttons/links the SLM can hand back for “deeper dive” visuals or reproducible analysis.

## Governance, risk & ethics

- **Provenance first:** Answers must cite Q‑IDs/DOIs and the exact query object used.
- **Quality gates:** run constraint checks (SHACL/OWL) on small slices before presenting derived claims.
- **Open vs. sensitive:** encourage ORCID/Zenodo/Wikidata for public info; avoid ingesting private data.
- **Community review loops:** bias, governance, sustainability, explainability—and log all tool calls for audit.

## Appendix

## Tools schema

```json
{
  "tools": [
    {
      "name": "hub_query",
      "description": "Run a vetted, parameterized SPARQL template over the SEEKCommons KG/Wikidata and return JSON/CSV.",
      "args_schema": {
        "template_id": "string",
        "params": "object"
      }
    },
    {
      "name": "scholia_profile",
      "description": "Open a Scholia view for an author/topic/venue.",
      "args_schema": {
        "kind": "author|topic|venue",
        "qid": "string"
      }
    }
  ],
  "policies": {
    "always_cite": true,
    "never_guess_ids": true,
    "prefer_tools_over_free_text": true
  }
}
```

### System prompt

> You are the SEEKCommons Assistant. When a question can be answered from the Resource Hub/Wikidata, call `hub_query` first. Summarize results, include Q‑IDs/DOIs, and offer Scholia or notebook follow‑ups. If data is missing, suggest ORCID/Zenodo steps to improve coverage and explain why. Never fabricate identifiers or claims; when uncertain, return what the KG actually says and how to add or reconcile the missing pieces.

### First 10 “query objects” to publish(?)

- Author‑topic report
- Topic→venues
- Topic→initiatives
- Fellow→co‑authors
- Project→outputs (papers/software/datasets)
- Venue landscape for Topic X
- Organization’s SEEKCommons footprint
- Recent outputs in the last N months
- Cross‑initiative connectors
- Missing‑metadata report (helps contribution).