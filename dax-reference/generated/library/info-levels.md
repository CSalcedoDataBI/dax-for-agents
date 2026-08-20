---
name: INFO.LEVELS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-levels-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.LEVELS

Returns a table with information about each level in the semantic model. This function provides metadata about hierarchy levels and their properties.

## Syntax

```dax
INFO.LEVELS ( [<Restriction name>, <Restriction value>], ... )
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

A table with the following columns:

| Column | Description |
|--------|-------------|
| [ID] | Unique identifier for the level |
| [HierarchyID] | Identifier of the hierarchy containing this level |
| [Ordinal] | Ordinal position of the level within the hierarchy |
| [Name] | Name of the level |
| [Description] | Description of the level |
| [ColumnID] | Identifier of the column associated with this level |
| [ModifiedTime] | Timestamp of when the level was last modified |
| [LineageTag] | Lineage tag for tracking data lineage |
| [SourceLineageTag] | Source lineage tag from the original data source |

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
	INFO.LEVELS()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _Levels =
		SELECTCOLUMNS(
			INFO.LEVELS(),
			"LevelID", [ID],
			"HierarchyID", [HierarchyID],
			"Level Name", [Name],
			"Ordinal", [Ordinal]
		)
	VAR _Hierarchies = 
		SELECTCOLUMNS(
			INFO.HIERARCHIES(),
			"HierarchyID", [ID],
			"Hierarchy Name", [Name]
		)
	VAR _CombinedTable =
		NATURALLEFTOUTERJOIN(
			_Levels,
			_Hierarchies
		)
	RETURN
		SELECTCOLUMNS(
			_CombinedTable,
			"Hierarchy Name", [Hierarchy Name],
			"Level Name", [Level Name],
			"Ordinal", [Ordinal]
		)
	ORDER BY [Hierarchy Name], [Ordinal]
```

## See also

- [INFO.HIERARCHIES](./info-hierarchies.md)
- [INFO.ATTRIBUTEHIERARCHIES](./info-attributehierarchies.md)
- [INFO.HIERARCHYSTORAGES](./info-hierarchystorages.md)
- [INFO.ATTRIBUTEHIERARCHYSTORAGES](./info-attributehierarchystorages.md)
- [INFO.TABLES](./info-tables.md)