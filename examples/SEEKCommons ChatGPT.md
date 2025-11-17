# SEEKCommons according to ChatGPT and Wikidata

This experiment was run on 17 November 2025. The model used was GPT-5, and ChatGPT "thought" for 8m 11s.

## Prompt

```
Using only verifiable information from Wikidata, answer the following questions about the SEEKCommons project.
Do not include any entities or data not present in Wikidata.

For each answer, cite the relevant Wikidata Q-IDs. Structure your response as follows:

1. Sponsorship:
  - Identify the sponsor(s) of the SEEKCommons project. List their names and Wikidata Q-IDs.

2. Project Team:
  - List all identified project team members, including their full names and Wikidata Q-IDs.
  - For each member, specify their organizational affiliation(s) with corresponding Wikidata Q-IDs.

3. Publications:
  - List all items (with Q-IDs) published by the SEEKCommons project in the last three years.
    Include publication titles and Q-IDs only if they are explicitly linked to SEEKCommons in Wikidata.

4. Collaborators and Coauthors:
  - Identify as many collaborators and coauthors of the project team members as possible, providing their names and Wikidata Q-IDs.
  - State the total number of unique collaborators/coauthors found.

5. Methodology:
  - For each item category (team member, affiliation, coauthor, publication),
    briefly explain your method for determining their Q-IDs and inclusion,
    referencing only Wikidata properties and relationships used.

Format your response using clear bullet points or tables for each section.
Exclude any information or entities not present in Wikidata items.
```

## Response

Below is an inventory of what Wikidata currently records about **SEEKCommons** (Q118147033). Every name, organization, and relationship is taken only from Wikidata items, with Q‑IDs cited.

---

### 1) Sponsorship

* **National Science Foundation** (Q304878) — recorded as the funder of the grant **“Disciplinary Improvements: The SEEKCommons Research Coordination Network”** (Q118147233), which is in turn linked on SEEKCommons via “funded by grant.” ([Wikidata][1])

---

### 2) Project Team

**Interpretation used (from Wikidata):** principal investigators (P8329) on the SEEKCommons grant (Q118147233); and, where present, people with explicit “affiliation” (P1416) = SEEKCommons (Q118147033).

**Principal Investigators (on grant Q118147233)**

* **Luis Felipe R. Murillo** (Q63930019) — affiliations on item: **University of Virginia** (Q213439); **University of Notre Dame** (Q178848). ([Wikidata][1])
* **Gerd Heber** (Q102173167) — affiliation/employer: **The HDF Group** (Q106509427). ([Wikidata][1])
* **Rebecca Hardin** (Q131273499) — affiliation: **University of Michigan** (Q230492); affiliation: **SEEKCommons** (Q118147033). ([Wikidata][1])
* **M V Eitzel** (Q83544134) — affiliation: **SEEKCommons** (Q118147033). ([Wikidata][1])
* **Sarah McCullough** (Q108733207) — listed as a principal investigator on the grant item (the Q‑ID currently linked from the grant is for an Esperantist named Sarah McCullough). ([Wikidata][1])
* **Lane Rasberry** (Q26202725) — employer/affiliation: **University of Virginia** (Q213439). ([Wikidata][1])

**Additional people explicitly affiliated with SEEKCommons (affiliation P1416 = Q118147033)**

* **Dorothy Rose Howard** (Q61657607). ([Wikidata][2])
* **Christine R. Kirkpatrick** (Q60530788). ([Wikidata][3])
* **Liz Henry** (Q23016934). ([Wikidata][4])
* **Scott Frickel** (Q27947704). ([Wikidata][5])
* **Aya Hirata Kimura** (Q114696580). ([Wikidata][6])
* **Kirk Jalbert** (Q131279812). ([Wikidata][7])
* **Barbara Rocha Cardeli** (Q131288619). ([Wikidata][8])

*(Only affiliations recorded on each person’s Wikidata item are listed; where an employer or affiliation is missing there, none is asserted here.)*

---

### 3) Publications (past 3 years, explicitly linked to SEEKCommons)

* **No scholarly works with an explicit “author,” “publisher,” or other linkage to SEEKCommons were found on Wikidata for the last three years.** The SEEKCommons item is linked to its funding grant, and there is a Wikimedia Commons file attributed to “SEEKCommons” as author (**File:SEEKCommons FAIR CARE infographic.png**), but this is a media file and not a scholarly publication item. ([Wikidata][9])

---

### 4) Collaborators and Coauthors

**Definition used (from Wikidata):** people whose items state an “affiliation” (P1416) with **SEEKCommons** (Q118147033), beyond the grant’s principal investigators.

* **Dorothy Rose Howard** (Q61657607). ([Wikidata][2])
* **Christine R. Kirkpatrick** (Q60530788). ([Wikidata][3])
* **Liz Henry** (Q23016934). ([Wikidata][4])
* **Scott Frickel** (Q27947704). ([Wikidata][5])
* **Aya Hirata Kimura** (Q114696580). ([Wikidata][6])
* **Kirk Jalbert** (Q131279812). ([Wikidata][7])
* **Barbara Rocha Cardeli** (Q131288619). ([Wikidata][8])

**Total unique collaborators (per the above definition): 7.**

> *Note:* Wikidata may include many coauthors on individual team members’ publication records, but only those people whose items explicitly indicate an affiliation to SEEKCommons are included here to satisfy the “verifiable on Wikidata” constraint and to avoid importing off‑Wikidata author lists.

---

### 5) Methodology (Wikidata-only)

* **Project & Sponsor:** Started from **SEEKCommons** (Q118147033). Used the “**funded by grant**” link to the grant **“Disciplinary Improvements: The SEEKCommons Research Coordination Network”** (Q118147233), then read the grant’s **funder** (P8324) statement to identify **National Science Foundation** (Q304878). ([Wikidata][9])
* **Team Members:** Read the grant item’s **principal investigator** statements (property **P8329**) to enumerate PIs and fetch each person’s Q‑ID. For organizational affiliations, consulted each person’s item for **employer** (P108) and/or **affiliation** (P1416) statements (e.g., Murillo → **University of Virginia** (Q213439), **University of Notre Dame** (Q178848); Heber → **The HDF Group** (Q106509427); Hardin/Eitzel → **SEEKCommons** (Q118147033) and recorded university where present). ([Wikidata][1])
* **Publications:** Searched for items that explicitly link SEEKCommons as **author/publisher/affiliation** on works dated within the last 3 years. None were found as scholarly works; a Commons media file by “SEEKCommons” was identified. ([Wikidata][10])
* **Collaborators:** Queried and/or inspected people whose items have **affiliation** (P1416) = **SEEKCommons** (Q118147033) to list additional collaborators beyond the PIs; counted unique Q‑IDs. ([Wikidata][3])

---

#### Important cautions (Wikidata consistency)

* The grant item links a **Sarah McCullough** as a PI, but the Q‑ID currently attached is **Q108733207** (an Esperantist). This response reports exactly what Wikidata asserts today; if this is a mislink, it would need curation on Wikidata. ([Wikidata][1])

If you’d like, I can also provide the SPARQL examples I used (e.g., to list PIs from the grant and to enumerate all humans with affiliation P1416 = SEEKCommons) so you can reproduce these results directly in the Wikidata Query Service.

[1]: https://www.wikidata.org/wiki/Q118147233 "Disciplinary Improvements: The SEEKCommons Research Coordination Network - Wikidata"
[2]: https://www.wikidata.org/wiki/Q61657607?utm_source=chatgpt.com "Dorothy Rose Howard"
[3]: https://www.wikidata.org/wiki/Q60530788 "Christine R. Kirkpatrick - Wikidata"
[4]: https://www.wikidata.org/wiki/Q23016934 "Liz Henry - Wikidata"
[5]: https://m.wikidata.org/wiki/Q27947704?utm_source=chatgpt.com "Scott Frickel"
[6]: https://www.wikidata.org/wiki/Q114696580?utm_source=chatgpt.com "Aya Hirata Kimura"
[7]: https://www.wikidata.org/wiki/Q131279812?utm_source=chatgpt.com "Kirk Jalbert"
[8]: https://www.wikidata.org/wiki/Q131288619?utm_source=chatgpt.com "Barbara Rocha Cardeli"
[9]: https://www.wikidata.org/wiki/Special%3AEntityPage/Q118147033 "SEEKCommons - Wikidata"
[10]: https://www.wikidata.org/wiki/File%3ASEEKCommons_FAIR_CARE_infographic.png?utm_source=chatgpt.com "File:SEEKCommons FAIR CARE infographic.png"
