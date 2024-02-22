# Research Organization Wikidata Profile

```sparql
PREFIX target: <http://www.wikidata.org/entity/{{ q }}>
```

For example, The HDF Group would be  

```sparql
PREFIX target: <http://www.wikidata.org/entity/Q106509427>
```

## Basics

`target:` is [instance of](https://www.wikidata.org/wiki/Property:P31) a [organization](https://www.wikidata.org/wiki/Q43229) or [facility](https://www.wikidata.org/wiki/Q13226383)

Subclasses of [organization](https://www.wikidata.org/wiki/Q43229) are fine as well, e.g., [nonprofit organization](https://www.wikidata.org/wiki/Q163740).

`target:` has [official website](https://www.wikidata.org/wiki/Property:P856) `?url`

`target:` has [funder](https://www.wikidata.org/wiki/Property:P8324) ?funder

`target:` is [funded by grant](https://www.wikidata.org/wiki/Property:P11814) `?grant`

`target:` has [location](https://www.wikidata.org/wiki/Property:P276) `?location`

## Identifiers

`target:` has [ROR ID](https://www.wikidata.org/wiki/Property:P6782) `?rorid`

## Questions

- How do we tie this to 'research'?
