---
name: INFO.HIERARCHYSTORAGES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-hierarchystorages-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.HIERARCHYSTORAGES

Returns a table with information about each hierarchy storage in the semantic model. This function provides metadata about how hierarchies are stored.

## Syntax

```dax
INFO.HIERARCHYSTORAGES ( [<Restriction name>, <Restriction value>], ... )
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
| [ID] | Unique identifier for the hierarchy storage |
| [HierarchyID] | Identifier linking to the hierarchy |
| [Name] | Name of the hierarchy storage |
| [LevelDefinition] | Definition of levels within the hierarchy |
| [MaterializationType] | Type of materialization used for the hierarchy storage |
| [StructureType] | Type of structure used for the hierarchy |
| [SystemTableID] | Identifier of the system table associated with the hierarchy |

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
	INFO.HIERARCHYSTORAGES()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _HierarchyStorages =
		SELECTCOLUMNS(
			INFO.HIERARCHYSTORAGES(),
			"HierarchyStorageID", [ID],
			"HierarchyID", [HierarchyID],
			"Storage Name", [Name]
		)
	VAR _Hierarchies = 
		SELECTCOLUMNS(
			INFO.HIERARCHIES(),
			"HierarchyID", [ID],
			"Hierarchy Name", [Name]
		)
	VAR _CombinedTable =
		NATURALLEFTOUTERJOIN(
			_HierarchyStorages,
			_Hierarchies
		)
	RETURN
		SELECTCOLUMNS(
			_CombinedTable,
			"Hierarchy Name", [Hierarchy Name],
			"Storage Name", [Storage Name]
		)
	ORDER BY [Hierarchy Name]
```

## See also

- [INFO.HIERARCHIES](./info-hierarchies.md)
- [INFO.ATTRIBUTEHIERARCHIES](./info-attributehierarchies.md)
- [INFO.ATTRIBUTEHIERARCHYSTORAGES](./info-attributehierarchystorages.md)
- [INFO.LEVELS](./info-levels.md)
- [INFO.TABLES](./info-tables.md)

