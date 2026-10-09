---
name: INFO.PERSPECTIVES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-perspectives-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.PERSPECTIVES

Returns a table with information about each perspective in the semantic model. This function provides metadata about perspectives defined in the model.

## Syntax

```dax
INFO.PERSPECTIVES ( [<Restriction name>, <Restriction value>], ... )
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

A table whose columns match the schema rowset for perspectives in the current semantic model.

|Column|Description|
|---|---|
|ID|Unique identifier for the perspective|
|ModelID|Foreign key to the model containing this perspective|
|Name|Name of the perspective|
|Description|Description of the perspective|
|ModifiedTime|Date and time when the perspective was last modified|

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
	INFO.PERSPECTIVES()
```

### Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
VAR _Perspectives = 
    SELECTCOLUMNS(
        INFO.PERSPECTIVES(),
        "PerspectiveID", [ID],
        "Perspective Name", [Name],
        "Perspective Description", [Description],
        "Modified", [ModifiedTime]
    )

VAR _PerspectiveTables = 
    SELECTCOLUMNS(
        INFO.PERSPECTIVETABLES(),
        "PerspectiveID", [PerspectiveID],
        "TableID", [TableID],
        "IncludeAll", [IncludeAll]
    )

VAR _Tables = 
    SELECTCOLUMNS(
        INFO.TABLES(),
        "TableID", [ID],
        "Table Name", [Name]
    )

VAR _CombinedTable1 = 
    NATURALLEFTOUTERJOIN(
        _Perspectives,
        _PerspectiveTables
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
        "Perspective Description", [Perspective Description],
        "Table Name", [Table Name],
        "Include All", [IncludeAll],
        "Modified", [Modified]
    )
ORDER BY [Perspective Name], [Table Name]
```

## See also

- [INFO.PERSPECTIVECOLUMNS](./info-perspectivecolumns.md)
- [INFO.PERSPECTIVEHIERARCHIES](./info-perspectivehierarchies.md)
- [INFO.PERSPECTIVEMEASURES](./info-perspectivemeasures.md)
- [INFO.PERSPECTIVETABLES](./info-perspectivetables.md)
- [INFO.TABLES](./info-tables.md)
