---
name: INFO.OBJECTTRANSLATIONS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-objecttranslations-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.OBJECTTRANSLATIONS

Returns a table with information about each object translation in the semantic model. This function provides metadata about translations for model objects.

## Syntax

```dax
INFO.OBJECTTRANSLATIONS ( [<Restriction name>, <Restriction value>], ... )
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

| Column | Data Type | Description |
|--------|-----------|-------------|
| [ID] | Integer | Unique identifier for the object translation |
| [CultureID] | Integer | ID of the culture this translation applies to |
| [ObjectID] | Integer | ID of the object being translated |
| [ObjectType] | Integer | Type of object being translated |
| [Property] | String | Property name that is being translated |
| [Value] | String | Translated value for the property |
| [ModifiedTime] | DateTime | Date and time when the translation was last modified |

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
	INFO.OBJECTTRANSLATIONS()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _ObjectTranslations =
		INFO.OBJECTTRANSLATIONS()

	VAR _Cultures = 
		SELECTCOLUMNS(
			INFO.CULTURES(),
			"CultureID", [ID],
			"Culture Name", [Name]
		)

	VAR _CombinedTable =
		NATURALLEFTOUTERJOIN(
			_ObjectTranslations,
			_Cultures
		)

	RETURN
		SELECTCOLUMNS(
			_CombinedTable,
			"Culture Name", [Culture Name],
			"Object Type", [ObjectType],
			"Property", [Property],
			"Translated Value", [Value],
			"Modified Time", [ModifiedTime]
		)
	ORDER BY [Culture Name], [Object Type], [Property]
```
## See also

- [INFO.CULTURES](./info-cultures.md)
- [INFO.LINGUISTICMETADATA](./info-linguisticmetadata.md)
- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
