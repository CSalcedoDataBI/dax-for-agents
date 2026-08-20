---
name: INFO.DEPENDENCIES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-dependencies-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.DEPENDENCIES

Returns a table with information about each dependency in the semantic model. This function provides metadata about object dependencies and relationships between model objects.

## Syntax

```dax
INFO.DEPENDENCIES ( [<Restriction name>, <Restriction value>], ... )
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

| Column name | Data type | Description |
| --- | --- | --- |
| [DATABASE_NAME] | String | Name of the database containing the object |
| [OBJECT_TYPE] | String | Type of the object (e.g., ATTRIBUTE_HIERARCHY, HIERARCHY, MEASURE) |
| [TABLE] | String | Name of the table containing the object |
| [OBJECT] | String | Name of the object |
| [EXPRESSION] | String | Expression associated with the object |
| [REFERENCED_OBJECT_TYPE] | String | Type of the referenced object |
| [REFERENCED_TABLE] | String | Name of the table containing the referenced object |
| [REFERENCED_OBJECT] | String | Name of the referenced object |
| [REFERENCED_EXPRESSION] | String | Expression of the referenced object |
| [QUERY] | String | Query context for the dependency |

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
	INFO.DEPENDENCIES()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _Dependencies =
		INFO.DEPENDENCIES()

	VAR _Tables = 
		SELECTCOLUMNS(
			INFO.TABLES(),
			"TABLE", [Name],
			"Table ID", [ID]
		)

	VAR _ReferencedTables = 
		SELECTCOLUMNS(
			INFO.TABLES(),
			"REFERENCED_TABLE", [Name],
			"Referenced Table ID", [ID]
		)

	VAR _CombinedWithTables =
		NATURALLEFTOUTERJOIN(
			_Dependencies,
			_Tables
		)

	VAR _CombinedWithReferencedTables =
		NATURALLEFTOUTERJOIN(
			_CombinedWithTables,
			_ReferencedTables
		)

	RETURN
		SELECTCOLUMNS(
			_CombinedWithReferencedTables,
			"Object Type", [OBJECT_TYPE],
			"Table", [TABLE],
			"Object", [OBJECT],
			"Referenced Object Type", [REFERENCED_OBJECT_TYPE],
			"Referenced Table", [REFERENCED_TABLE],
			"Referenced Object", [REFERENCED_OBJECT]
		)
	ORDER BY [TABLE], [OBJECT]
```
## See also

- [INFO.CALCDEPENDENCY](./info-calcdependency.md)
- [INFO.RELATEDCOLUMNDETAILS](./info-relatedcolumndetails.md)
- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
