---
name: INFO.PERSPECTIVEHIERARCHIES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-perspectivehierarchies-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.PERSPECTIVEHIERARCHIES

Returns a table with information about each perspective hierarchy in the semantic model. This function provides metadata about hierarchies included in perspectives.

## Syntax

```dax
INFO.PERSPECTIVEHIERARCHIES ( [<Restriction name>, <Restriction value>], ... )
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

A table whose columns match the schema rowset for perspective hierarchies in the current semantic model.

|Column|Description|
|---|---|
|ID|Unique identifier for the perspective hierarchy relationship|
|PerspectiveTableID|Foreign key to the perspective table containing this hierarchy|
|HierarchyID|Foreign key to the hierarchy included in the perspective|
|ModifiedTime|Date and time when the perspective hierarchy was last modified|

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
	INFO.PERSPECTIVEHIERARCHIES()
```

### Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
VAR _PerspectiveHierarchies = 
    SELECTCOLUMNS(
        INFO.PERSPECTIVEHIERARCHIES(),
        "PerspectiveTableID", [PerspectiveTableID],
        "HierarchyID", [HierarchyID],
        "Modified", [ModifiedTime]
    )

VAR _PerspectiveTables = 
    SELECTCOLUMNS(
        INFO.PERSPECTIVETABLES(),
        "PerspectiveTableID", [ID],
        "PerspectiveID", [PerspectiveID],
        "TableID", [TableID]
    )

VAR _Hierarchies = 
    SELECTCOLUMNS(
        INFO.HIERARCHIES(),
        "HierarchyID", [ID],
        "Hierarchy Name", [Name],
        "Table ID", [TableID]
    )

VAR _Perspectives = 
    SELECTCOLUMNS(
        INFO.PERSPECTIVES(),
        "PerspectiveID", [ID],
        "Perspective Name", [Name]
    )

VAR _CombinedTable1 = 
    NATURALLEFTOUTERJOIN(
        _PerspectiveHierarchies,
        _PerspectiveTables
    )

VAR _CombinedTable2 = 
    NATURALLEFTOUTERJOIN(
        _CombinedTable1,
        _Hierarchies
    )

VAR _CombinedTable3 = 
    NATURALLEFTOUTERJOIN(
        _CombinedTable2,
        _Perspectives
    )

RETURN
    SELECTCOLUMNS(
        _CombinedTable3,
        "Perspective Name", [Perspective Name],
        "Hierarchy Name", [Hierarchy Name],
        "Modified", [Modified]
    )
ORDER BY [Perspective Name], [Hierarchy Name]
```

## See also

- [INFO.PERSPECTIVES](./info-perspectives.md)
- [INFO.PERSPECTIVECOLUMNS](./info-perspectivecolumns.md)
- [INFO.PERSPECTIVEMEASURES](./info-perspectivemeasures.md)
- [INFO.PERSPECTIVETABLES](./info-perspectivetables.md)
- [INFO.TABLES](./info-tables.md)
