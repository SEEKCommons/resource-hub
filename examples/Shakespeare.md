# Shakespeare - Sample Wikidata SPARQL queries

You can paste any of the queries into [https://query.wikidata.org](https://query.wikidata.org) to produce the lists and counts directly from Wikidata.

## Comedies — list (title + Q‑ID)

### Shakespeare plays: comedies (list)

```sparql
SELECT ?work ?qid ?workLabel WHERE {
  # Author: William Shakespeare
  ?work wdt:P50 wd:Q692 .

  # Ensure the item is a play (instance-of or form-of-creative-work is / subclass-of play)
  { ?work wdt:P31/wdt:P279*  wd:Q25379 }
  UNION
  { ?work wdt:P7937/wdt:P279* wd:Q25379 } .

  # Genre is (subclass of) comedy
  ?work wdt:P136 ?genre .
  ?genre wdt:P279* wd:Q40831 .

  # Extract the Q-ID for convenience
  BIND(STRAFTER(STR(?work), "entity/") AS ?qid)

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY LCASE(?workLabel)
```

#### Count only (comedies)

```sparql
SELECT (COUNT(DISTINCT ?work) AS ?count) WHERE {
  ?work wdt:P50 wd:Q692 .
  { ?work wdt:P31/wdt:P279*  wd:Q25379 }
  UNION
  { ?work wdt:P7937/wdt:P279* wd:Q25379 } .
  ?work wdt:P136/wdt:P279* wd:Q40831 .
}
```

## Tragedies — list (title + Q‑ID)

### Shakespeare plays: tragedies (list)

```sparql
SELECT ?work ?qid ?workLabel WHERE {
  ?work wdt:P50 wd:Q692 .

  { ?work wdt:P31/wdt:P279*  wd:Q25379 }
  UNION
  { ?work wdt:P7937/wdt:P279* wd:Q25379 } .

  # Genre is (subclass of) tragedy
  ?work wdt:P136/wdt:P279* wd:Q80930 .

  BIND(STRAFTER(STR(?work), "entity/") AS ?qid)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY LCASE(?workLabel)
```

#### Count only (tragedies)

```sparql
SELECT (COUNT(DISTINCT ?work) AS ?count) WHERE {
  ?work wdt:P50 wd:Q692 .
  { ?work wdt:P31/wdt:P279*  wd:Q25379 }
  UNION
  { ?work wdt:P7937/wdt:P279* wd:Q25379 } .
  ?work wdt:P136/wdt:P279* wd:Q80930 .
}
```

## Histories — list (title + Q‑ID)

### Shakespeare plays: histories (list)

```sparql
SELECT ?work ?qid ?workLabel WHERE {
  ?work wdt:P50 wd:Q692 .

  { ?work wdt:P31/wdt:P279*  wd:Q25379 }
  UNION
  { ?work wdt:P7937/wdt:P279* wd:Q25379 } .

  # Genre is (subclass of) historical play (aka "history play")
  ?work wdt:P136/wdt:P279* wd:Q5774663 .

  BIND(STRAFTER(STR(?work), "entity/") AS ?qid)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY LCASE(?workLabel)
```

#### Count only (histories)

```sparql
SELECT (COUNT(DISTINCT ?work) AS ?count) WHERE {
  ?work wdt:P50 wd:Q692 .
  { ?work wdt:P31/wdt:P279*  wd:Q25379 }
  UNION
  { ?work wdt:P7937/wdt:P279* wd:Q25379 } .
  ?work wdt:P136/wdt:P279* wd:Q5774663 .
}
```

## One query to return all categories at once (with titles + Q‑IDs)

### Shakespeare plays grouped by root genre (comedy / tragedy / historical play)

```sparql
SELECT ?rootGenre ?rootGenreLabel ?work ?qid ?workLabel WHERE {
  VALUES ?rootGenre { wd:Q40831  wd:Q80930  wd:Q5774663 }  # comedy / tragedy / historical play

  ?work wdt:P50 wd:Q692 .
  { ?work wdt:P31/wdt:P279*  wd:Q25379 }
  UNION
  { ?work wdt:P7937/wdt:P279* wd:Q25379 } .

  ?work wdt:P136/wdt:P279* ?rootGenre .

  BIND(STRAFTER(STR(?work), "entity/") AS ?qid)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY ?rootGenreLabel LCASE(?workLabel)
```

#### Category counts in one shot

```sparql
SELECT ?rootGenreLabel (COUNT(DISTINCT ?work) AS ?count) WHERE {
  VALUES ?rootGenre { wd:Q40831  wd:Q80930  wd:Q5774663 }

  ?work wdt:P50 wd:Q692 .
  { ?work wdt:P31/wdt:P279*  wd:Q25379 }
  UNION
  { ?work wdt:P7937/wdt:P279* wd:Q25379 } .

  ?work wdt:P136/wdt:P279* ?rootGenre .

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
GROUP BY ?rootGenreLabel
ORDER BY ?rootGenreLabel
```
