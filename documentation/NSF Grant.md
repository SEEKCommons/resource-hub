# NSF Grant

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

# Example SPARQL query: SELECT ?p { VALUES ?p { wd:Q118147233 }}

START = @<NSFGrant>

<NSFGrant> EXTRA wdt:P31 wdt:17 {
    wdt:P31   [ wd:Q230788 ] ;         # Instance of: Grant
    wdt:P1476 rdf:langString? ;        # Title (optional)
    wdt:P17   [ wd:Q30 ] ;             # Country: USA
    wdt:P921 IRI+ ;                    # Main subject (multiple allowed)
    wdt:P580 xsd:dateTime? ;           # Start time (optional)
    wdt:P582 xsd:dateTime? ;           # End time (optional)
    wdt:P2769 xsd:decimal? ;           # Budget
    wdt:P8329 IRI+ ;                   # Principal investigator (multiple allowed)
    wdt:P11858 xsd:string /[0-9]{7}/ ; # NSF award ID
}
```
[Try it!](https://shex-simple.toolforge.org/wikidata/packages/shex-webapp/doc/shex-simple.html?data=Endpoint:%20https://query.wikidata.org/sparql&hideData&manifest=[]&textMapIsSparqlQuery)
