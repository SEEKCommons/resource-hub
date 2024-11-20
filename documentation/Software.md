```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>

START = @<Software>

<Software> EXTRA wdt:P31 {
    wdt:P31 [ wd:Q7397 ] ;      # Instance of: Software
    wdt:P178 IRI+ ;             # Developer (optional, can have multiple values)
    wdt:P277 IRI+ ;             # Programming language (optional)
    wdt:P306 IRI+ ;             # Operating system (optional)
    wdt:P1324 IRI* ;            # Source code repository URL (optional, multiple allowed)
    wdt:P856 IRI? ;             # Official website (optional)
    wdt:P275 IRI? ;             # Copyright license (optional)
    wdt:P571 xsd:dateTime? ;    # Inception (optional)
    wdt:P348 xsd:string? ;      # Version identifier (optional)
    wdt:P156 IRI* ;             # Follows (optional, links to software it follows)
    wdt:P136 IRI* ;             # Genre (optional, e.g., video game, productivity software)
    wdt:P2078 IRI* ;            # User manual URL (optional)
}
```
