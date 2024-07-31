# Research Project Wikidata Profile

```sparql
PREFIX target: <http://www.wikidata.org/entity/{{ q }}>
```

For example, SEEKCommons would be  

```sparql
PREFIX target: <http://www.wikidata.org/entity/Q118147033>
```

## Basics

We do **NOT** duplicate the description of the research project. We link to the NSF award instead.

`target:` is [instance of](https://www.wikidata.org/wiki/Property:P31) a [research project](https://www.wikidata.org/wiki/Q1298668)

`target:` started at [start time](https://www.wikidata.org/wiki/Property:P580) `?yyyymmdd`

`target:` ended at [end time](https://www.wikidata.org/wiki/Property:P582) `?yyyymmdd`

`target:` has [official website](https://www.wikidata.org/wiki/Property:P856) `?url`

`target:` has [funder](https://www.wikidata.org/wiki/Property:P8324) [National Science Foundation](https://www.wikidata.org/wiki/Q304878)

`target:` is [funded by grant](https://www.wikidata.org/wiki/Property:P11814) `?grant`

`target:` has [research site](https://www.wikidata.org/wiki/Property:P6153) `?location`

`target:` has [location](https://www.wikidata.org/wiki/Property:P276) `?location`

`target:` has [principal investigator](https://www.wikidata.org/wiki/Property:P8329) `?pi`

`target:` has [main subject](https://www.wikidata.org/wiki/Property:P921) `?subject`

## Identifiers

`target:` has [National Science Foundation award](https://www.wikidata.org/wiki/Property:P11858) `?awardno`

## Publications

`target:` [has part(s)](https://www.wikidata.org/wiki/Property:527) `?publication`

Link the publication to the research project with [part of](https://www.wikidata.org/wiki/Property:P361) `target:`

## Related Resources

`target:` has [GitHub username](https://www.wikidata.org/wiki/Property:P2037) `?name`

`target:` has [Zotero ID](https://www.wikidata.org/wiki/Property:P10557) `?zid`

## Loose Ends

- Data repositories & data sets
- Partner organizations
  - [partnership with](https://www.wikidata.org/wiki/Property:P2652) `?partner`
  - [participant](https://www.wikidata.org/wiki/Property:P710) `?part`