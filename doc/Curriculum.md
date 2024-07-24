# Curriculum

A curriculum is a structured set of educational experiences and content that outlines what students are expected to learn and how they will learn it over a specific period, such as a school year or a course. It typically includes:

- **Objectives and Goals:** What students should know and be able to do by the end of the course or program.
- **Content:** The subject matter, topics, and materials that will be covered.
- **Teaching Methods:** The instructional strategies and approaches teachers will use to deliver the content.
- **Assessment Methods:** The tools and techniques used to evaluate student learning and progress, such as exams, quizzes, projects, and assignments.
- **Resources and Materials:** The textbooks, digital tools, readings, and other materials that support learning.
- **Sequence and Pacing:** The order in which topics will be taught and the timeline for covering them.

In this document, we describe how to represent SEEKCommons curricula in the SEEKCommons Resource Hub. Our working example of a curriculum will be the series of workshops for SEEKCommons fellows. The Wikidata entry for this curriculum is https://www.wikidata.org/wiki/Q126722701.

What makes this entry a curriculum?

- Well, the entry itself is **not** a curriculum, but it represents a curriculum. The resource hub does not store the curriculum content itself but rather metadata about the curriculum. The curriculum content (modules) is stored in the SEEKCommons website, in Zenodo records, YouTube videos, etc. The resource hub provides a way to discover and access these resources. This information can then be used by a *renderer* to display them in any form required.
- `Q126722701` is, among other things, an instance of (`Property:P31`) of [curriculum](https://www.wikidata.org/wiki/Q1402601) (`Q1402601`)
- The curriculum's author (`Property:P50`) is the [SEEKCommons project](https://www.wikidata.org/wiki/Q118147033)
- A description of the curriculum (`Property:P973`) can be found at a URL such as https://seekcommons.org/fellowship-application.html
  - Alternatively, there could be a *described by source* (`Property:1343`) statement
- At the time of this writing, the curriculum encompasses seven modules provided in has part(s) (`Property:P527`) statements
  - The module order is represented via *series ordinal* (`Property:P1545`) statements.
  - While it is possible to support rather intricate module nesting structures, at the moment, we support simple linear sequences only.

There could be additional statements, e.g., citations and references, and more information is better, but this is the minimum.

List the SEEKCommons curricula in Wikidata:

```sparql
SELECT DISTINCT ?curr ?currLabel ?url WHERE {
  ?curr wdt:P31 wd:Q1402601 ;           # Instance of = curriculum
        wdt:P50 wd:Q118147033 .         # Author = SEEKCommons project
  OPTIONAL { ?curr wdt:P973 ?url. }     # Described at URL
  OPTIONAL { ?curr wdt:P1343 ?source. } # Described at source 
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
```
[Try it!](https://query.wikidata.org/#SELECT%20DISTINCT%20%3Fcurr%20%3FcurrLabel%20%3Furl%20%3Fsource%20WHERE%20%7B%0A%20%20%3Fcurr%20wdt%3AP31%20wd%3AQ1402601%20%3B%20%20%20%20%20%20%20%20%20%20%20%23%20Instance%20of%20%3D%20curriculum%0A%20%20%20%20%20%20%20%20wdt%3AP50%20wd%3AQ118147033%20.%20%20%20%20%20%20%20%20%20%23%20Author%20%3D%20SEEKCommons%20project%0A%20%20OPTIONAL%20%7B%20%3Fcurr%20wdt%3AP973%20%3Furl.%20%7D%20%20%20%20%20%23%20Described%20at%20URL%0A%20%20OPTIONAL%20%7B%20%3Fcurr%20wdt%3AP1343%20%3Fsource.%20%7D%20%23%20Described%20at%20source%20%0A%20%20%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%7D)

List the modules in SEEKCommons curricula:

```sparql
SELECT DISTINCT ?modLabel WHERE {
  ?curr wdt:P31 wd:Q1402601 ;           # Instance of = curriculum
        wdt:P50 wd:Q118147033 ;         # Author = SEEKCommons project
        wdt:P527 ?mod .                 # Has parts = *
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
```
[Try it!](https://query.wikidata.org/#SELECT%20DISTINCT%20%3FmodLabel%20WHERE%20%7B%0A%20%20%3Fcurr%20wdt%3AP31%20wd%3AQ1402601%20%3B%20%20%20%20%20%20%20%20%20%20%20%23%20Instance%20of%20%3D%20curriculum%0A%20%20%20%20%20%20%20%20wdt%3AP50%20wd%3AQ118147033%20%3B%20%20%20%20%20%20%20%20%20%23%20Author%20%3D%20SEEKCommons%20project%0A%20%20%20%20%20%20%20%20wdt%3AP527%20%3Fmod%20.%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%23%20Has%20parts%20%3D%20%2a%0A%20%20%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%7D)





## Modules

Learning modules are identified as instances of [learning module](https://www.wikidata.org/wiki/Q93208411) (`Q93208411`). Typical statements about modules include:

- The module's author(s) (`Property:P50`) or author name string(s) (`Property:P2093`)
- A publication date (`Property:P577`)
- The work(s) a module cites (`Property:2860`)

A typical example is the *Commons in Science and Technology* module https://www.wikidata.org/wiki/Q126722621. Its content (presentation) can be found in a [Zenodo record](https://zenodo.org/record/12162246), which is referenced via a ZenodoID statement (`Property:4901`).
