# NSF Grant

```sparql
PREFIX  schema: <http://schema.org/>
PREFIX  p:     <http://www.wikidata.org/prop/>
PREFIX  wdt:   <http://www.wikidata.org/prop/direct/> 
PREFIX  skos:  <http://www.w3.org/2004/02/skos/core#> 
PREFIX  rdfs:  <http://www.w3.org/2000/01/rdf-schema#> 

start = @<NSFGrant>

<NSFGrant>{
        rdfs:label   .* ;
        schema:description  .* ;
        schema:name         .* ;
        skos:altLabel       .* ;
        skos:prefLabel      .* ;
        wdt:P31  [ wd:Q230788 ]; # instance of = grant
        wdt:P11858          .* ; # NSF award ID
        wdt:P580            .* ; # start time
        wdt:P582            .* ; # end time
        wdt:P17  [ wd:Q30 ]    ; # country = USA
        wdt:P2769           .* ; # budget
}
```

Example:

```sparql
SELECT ?grant WHERE {
  ?grant wdt:P11858 ?awardID;
    wdt:P580 ?startDate;
    wdt:P582 ?endDate;
    wdt:P17 wd:Q30;
    wdt:P2769 ?budget.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY (?startDate)
```
[Try it!](https://query.wikidata.org/#SELECT%20%3Fgrant%20WHERE%20%7B%0A%20%20%3Fgrant%20wdt%3AP11858%20%3FawardID%3B%0A%20%20%20%20wdt%3AP580%20%3FstartDate%3B%0A%20%20%20%20wdt%3AP582%20%3FendDate%3B%0A%20%20%20%20wdt%3AP17%20wd%3AQ30%3B%0A%20%20%20%20wdt%3AP2769%20%3Fbudget.%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%7D%0AORDER%20BY%20%28%3FstartDate%29)
