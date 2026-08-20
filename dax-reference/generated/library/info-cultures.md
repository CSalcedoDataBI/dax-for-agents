---
name: INFO.CULTURES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-cultures-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.CULTURES

Returns a table with information about each culture in the semantic model. This function provides metadata about the cultures and locales supported by the model.

## Syntax

```dax
INFO.CULTURES ( [<Restriction name>, <Restriction value>], ... )
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
| [ID] | Integer | Unique identifier for the culture |
| [ModelID] | Integer | Identifier of the semantic model |
| [Name] | String | Name of the culture (e.g., en-US) |
| [LinguisticMetadataID] | Integer | Identifier for linguistic metadata associated with the culture |
| [ModifiedTime] | DateTime | Date and time when the culture was last modified |
| [StructureModifiedTime] | DateTime | Date and time when the culture structure was last modified |

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
	INFO.CULTURES()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _Cultures =
		INFO.CULTURES()

	VAR _Model = 
		SELECTCOLUMNS(
			INFO.MODEL(),
			"ModelID", [ID],
			"Model Name", [Name]
		)

	VAR _CombinedTable =
		NATURALLEFTOUTERJOIN(
			_Cultures,
			_Model
		)

	RETURN
		SELECTCOLUMNS(
			_CombinedTable,
			"Model Name", [Model Name],
			"Culture Name", [Name],
			"Modified Time", [ModifiedTime],
			"Structure Modified Time", [StructureModifiedTime]
		)
	ORDER BY [Culture Name]
```
## See also

- [INFO.OBJECTTRANSLATIONS](./info-objecttranslations.md)
- [INFO.LINGUISTICMETADATA](./info-linguisticmetadata.md)
- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
