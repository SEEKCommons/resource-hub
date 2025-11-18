# Reinforcement Learning from Human Feedback (RLHF) + Active‑Learning Plan

**Purpose.** Capture *preferences* for answer style/ordering and keep improving the model on real SEEKCommons questions, while aligning with our openness/ethics commitments.

## Where preference data come from

- Live workshops & office hours: collect (question, tool calls, raw results, draft answer) and ask participants to choose the better of two model answers (A/B).
- Curation sessions (Hub maintainers): pairwise choices on “which result set is more useful/transparent?” with short rationales.
- Edge‑case queues: questions that caused empty/ambiguous results.

## Labeling rubric (what raters reward)

1. Faithfulness & provenance (facts match the graph; citations included).
2. Clarity & brevity (answers ≤ 200 words + a tiny table).
3. Reproducibility (includes how to rerun the template).
4. Care language (notes uncertainty/bias; suggests how to improve the graph).
5. Community alignment (uses ORCID/DOI/Q‑IDs when available).

## Pipeline (30/60/90)

- **Day 0–30:** Collect ~1–2k preference pairs; train a lightweight reward model (or use direct preference optimization) on top of the SFT model; keep tool‑use unchanged.
- **Day 31–60:** Active learning loop: mine “low‑confidence/low‑overlap” queries from logs; prioritize items lacking citations or with conflicting sources; relabel; refresh DPO.
- **Day 61–90:** Add evaluator‑Llama style auto‑checks for: (a) citation presence, (b) table correctness vs. tool output, (c) banned claims (no source). Escalate fails for human review.

## Safety & governance

- No PII beyond public scholarly IDs (ORCID, Q‑IDs, DOIs).
- Respect WDQS/ORCID/Zenodo ToS; cache only metadata.
- Align with linked‑data ethics guidance surfaced in our Resource Hub references (bias, governance, provenance), and treat **provenance recording + constraint checks in CI** as first‑class quality controls.

## Success metrics

- **Answer correctness@top‑3** vs. gold tables (≥ 85%).
- **Citation coverage** (≥ 95% answers include at least one resolvable source).
- **Reproducibility rate** (≥ 90% include a runnable template + params).
- **User‑rated helpfulness** (↑ by ≥ 15% after each RLHF round).

**Why it works here.** Our domain is structured and federated; RLHF should optimize style and prioritization, while correctness is anchored by RDF semantics (domain/range, subclassing, transitivity) and explicit graph traversal — “a little semantics goes a long way.”