---
name: INFO.HIERARCHIES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-hierarchies-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.HIERARCHIES

Returns a table with information about each hierarchy in the semantic model. This function provides metadata about hierarchies and their properties.

## Syntax

```dax
INFO.HIERARCHIES ( [<Restriction name>, <Restriction value>], ... )
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
| [ID] | Unique identifier for the hierarchy |
| [TableID] | Identifier of the table containing the hierarchy |
| [Name] | Name of the hierarchy |
| [Description] | Description of the hierarchy |
| [IsHidden] | Boolean indicating if the hierarchy is hidden from client tools |
| [State] | Current state of the hierarchy (e.g., Ready, Processing) |
| [HierarchyStorageID] | Identifier linking to the hierarchy storage information |
| [ModifiedTime] | Timestamp of when the hierarchy was last modified |
| [StructureModifiedTime] | Timestamp of when the hierarchy structure was last modified |
| [RefreshedTime] | Timestamp of when the hierarchy was last refreshed |
| [DisplayFolder] | Display folder for organizing hierarchies in client tools |
| [HideMembers] | Setting for hiding hierarchy members |
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
	INFO.HIERARCHIES()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _Hierarchies =
		SELECTCOLUMNS(
			INFO.HIERARCHIES(),
			"HierarchyID", [ID],
			"Hierarchy Name", [Name],
			"TableID", [TableID]
		)
	VAR _Tables = 
		SELECTCOLUMNS(
			INFO.TABLES(),
			"TableID", [ID],
			"Table Name", [Name]
		)
	VAR _CombinedTable =
		NATURALLEFTOUTERJOIN(
			_Hierarchies,
			_Tables
		)
	RETURN
		_CombinedTable
	ORDER BY [Hierarchy Name]
```

## See also

- [INFO.ATTRIBUTEHIERARCHIES](./info-attributehierarchies.md)
- [INFO.HIERARCHYSTORAGES](./info-hierarchystorages.md)
- [INFO.ATTRIBUTEHIERARCHYSTORAGES](./info-attributehierarchystorages.md)
- [INFO.LEVELS](./info-levels.md)
- [INFO.TABLES](./info-tables.md)
