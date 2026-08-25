---
name: INFO.PERSPECTIVETABLES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-perspectivetables-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.PERSPECTIVETABLES

Returns a table with information about each perspective table in the semantic model. This function provides metadata about tables included in perspectives.

## Syntax

```dax
INFO.PERSPECTIVETABLES ( [<Restriction name>, <Restriction value>], ... )
```

## Parameters

Parameters are optional for this DAX function. When parameters are used, both must be given. More than one pair of parameters is allowed. The restriction name and value are text and entered in double-quotes.

| Term | Definition |
|---|---|
| Restriction name | Name of the restriction used to filter the results. |
| Restriction value | Value used to filter the results of the restriction. |

## Restrictions

Typically, all columns of the DAX function results can be used as a restriction. Additional restrictions may also be allowed.

## Return value

A table whose columns match the schema rowset for perspective tables in the current semantic model.

|Column|Description|
|---|---|
|ID|Unique identifier for the perspective table relationship|
|PerspectiveID|Foreign key to the perspective containing this table|
|TableID|Foreign key to the table included in the perspective|
|IncludeAll|Boolean indicating whether all objects from the table are included in the perspective|
|ModifiedTime|Date and time when the perspective table was last modified|

## Remarks

- Typically used in DAX queries to inspect and document model metadata.
- Permissions required depend on the host. Querying full metadata may require model admin permissions.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	INFO.PERSPECTIVETABLES()
```

### Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
VAR _PerspectiveTables = 
    SELECTCOLUMNS(
        INFO.PERSPECTIVETABLES(),
        "PerspectiveID", [PerspectiveID],
        "TableID", [TableID],
        "Include All", [IncludeAll],
        "Modified", [ModifiedTime]
    )

VAR _Perspectives = 
    SELECTCOLUMNS(
        INFO.PERSPECTIVES(),
        "PerspectiveID", [ID],
        "Perspective Name", [Name],
        "Perspective Description", [Description]
    )

VAR _Tables = 
    SELECTCOLUMNS(
        INFO.TABLES(),
        "TableID", [ID],
        "Table Name", [Name],
        "Table Description", [Description]
    )

VAR _CombinedTable1 = 
    NATURALLEFTOUTERJOIN(
        _PerspectiveTables,
        _Perspectives
    )

VAR _CombinedTable2 = 
    NATURALLEFTOUTERJOIN(
        _CombinedTable1,
        _Tables
    )

RETURN
    SELECTCOLUMNS(
        _CombinedTable2,
        "Perspective Name", [Perspective Name],
        "Table Name", [Table Name],
        "Include All", [Include All],
        "Modified", [Modified]
    )
ORDER BY [Perspective Name], [Table Name]
```

## See also

- [INFO.PERSPECTIVES](./info-perspectives.md)
- [INFO.PERSPECTIVECOLUMNS](./info-perspectivecolumns.md)
- [INFO.PERSPECTIVEHIERARCHIES](./info-perspectivehierarchies.md)
- [INFO.PERSPECTIVEMEASURES](./info-perspectivemeasures.md)
- [INFO.TABLES](./info-tables.md)
