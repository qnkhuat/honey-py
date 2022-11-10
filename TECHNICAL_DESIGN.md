(-> (a dictionary)
    figure out the order of execution
    recurisvely format each parts
    )


The goal of this project:
- Make writing sql easier by using a dictionary
- Initally:
  - it'll supports only some basic operations
    select, insert, update, set
    from join
    where, expresion(and, or, comparision),
  - able to config quote style


This looks like a good summarize on the atanomy of sql language: https://en.wikipedia.org/wiki/SQL_syntax

It has :
- keywords: things like select, from, where...
- identifiers: naem of table, columns...
- expressions:
- statemenets: the whole `select * from where ...;`


What options, extensiblity we want to have:
Must have:
- quote identifiers style

Nice to have(keep in mind these details when you design)
- easily adding new clause
- inline: no parmas
- option to capitalize keyword
