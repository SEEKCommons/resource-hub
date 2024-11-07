# NSF Grant

```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
prefix wd: <http://www.wikidata.org/entity/>
prefix wdt: <http://www.wikidata.org/prop/direct/>

start = @<NSFGrant>

<NSFGrant>{
#        wdt:P31   [ wd:Q230788 ] ; # instance of = grant
        wdt:P1476             .* ; # title
#        wdt:P17   [ wd:Q30 ]     ; # country = USA
        wdt:P921              .* ; # main subject
        wdt:P580              .* ; # start time
        wdt:P582              .* ; # end time
#        wdt:P2769             .* ; # budget
#        wdt:P8329             .* ; # principal investigator
        wdt:P11858            .* ; # NSF award ID
}
```
[Try it!](https://shex-simple.toolforge.org/wikidata/packages/shex-webapp/doc/shex-simple.html?data=Endpoint:%20https://query.wikidata.org/sparql&hideData&manifest=[]&textMapIsSparqlQuery)

Example:

```sparql
SELECT ?grant WHERE {
  ?grant (wdt:P31/(wdt:P279*)) wd:Q230788;
    wdt:P11858 ?awardID;
    wdt:P580 ?startDate;
    wdt:P582 ?endDate.
#    wdt:P17 wd:Q30;
#    wdt:P2769 ?budget.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY (?startDate)
```
[Try it!](https://query.wikidata.org/#SELECT%20%3Fgrant%20WHERE%20%7B%0A%20%20%3Fgrant%20%28wdt%3AP31%2F%28wdt%3AP279%2a%29%29%20wd%3AQ230788%3B%0A%20%20%20%20wdt%3AP11858%20%3FawardID%3B%0A%20%20%20%20wdt%3AP580%20%3FstartDate%3B%0A%20%20%20%20wdt%3AP582%20%3FendDate.%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%7D%0AORDER%20BY%20%28%3FstartDate%29)
