# Hardware

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

# Example SPARQL query: SELECT ?p { VALUES ?p { wd:Q16626381 }}

START = @<Hardware>

<Hardware> EXTRA wdt:P31 {
    #wdt:P31 [ wd:Q39631 ] ;       # Instance of: Hardware (or subclass, e.g., computer hardware)
    wdt:P31 [ wd:Q159172 ] ;       # Instance of: Open Hardware
    wdt:P176 IRI+ ;              # Manufacturer (e.g., Apple, Intel, Dell)
    wdt:P571 xsd:dateTime? ;     # Inception (optional)
    wdt:P5123 xsd:dateTime? ;    # Date of production end (optional)
    wdt:P137 IRI* ;              # Operator (optional, e.g., who uses or manages the hardware)
    wdt:P1196 IRI* ;             # Intended public (optional, e.g., consumer, enterprise, etc.)
    wdt:P1629 IRI* ;             # Compatible with (e.g., operating system, hardware standards)
    wdt:P275 IRI? ;              # License (optional, e.g., open hardware license)
    wdt:P348 xsd:string? ;       # Version identifier (optional, for specific models)
    wdt:P4878 IRI* ;             # Technical specifications (optional, links to related items or documents)
    wdt:P856 IRI? ;              # Official website (optional)
    wdt:P1324 IRI* ;             # Source code repository (optional, for open-source hardware)
    wdt:P155 IRI* ;              # Preceded by (links to predecessor hardware, if applicable)
    wdt:P156 IRI* ;              # Follows (links to successor hardware, if applicable)
}
```
[Try it!](https://shex-simple.toolforge.org/wikidata/packages/shex-webapp/doc/shex-simple.html?data=Endpoint:%20https://query.wikidata.org/sparql&hideData&manifest=[]&textMapIsSparqlQuery)
