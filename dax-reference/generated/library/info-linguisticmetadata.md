---
name: INFO.LINGUISTICMETADATA
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-linguisticmetadata-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.LINGUISTICMETADATA

Returns a table with information about each linguistic metadata entry in the semantic model. This function provides metadata about linguistic metadata definitions.

## Syntax

```dax
INFO.LINGUISTICMETADATA ( [<Restriction name>, <Restriction value>], ... )
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
| [ID] | Unique identifier for the linguistic metadata entry |
| [CultureID] | Identifier of the culture associated with this metadata |
| [Content] | Content of the linguistic metadata |
| [ModifiedTime] | Timestamp of when the linguistic metadata was last modified |
| [ContentType] | Type of content stored in the linguistic metadata |

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
	INFO.LINGUISTICMETADATA()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _LinguisticMetadata =
		SELECTCOLUMNS(
			INFO.LINGUISTICMETADATA(),
			"LinguisticMetadataID", [ID],
			"CultureID", [CultureID],
			"ContentType", [ContentType]
		)
	VAR _Cultures = 
		SELECTCOLUMNS(
			INFO.CULTURES(),
			"CultureID", [ID],
			"Culture Name", [Name]
		)
	VAR _CombinedTable =
		NATURALLEFTOUTERJOIN(
			_LinguisticMetadata,
			_Cultures
		)
	RETURN
		SELECTCOLUMNS(
			_CombinedTable,
			"Culture Name", [Culture Name],
			"Content Type", [ContentType]
		)
	ORDER BY [Culture Name]
```

## See also

- [INFO.CULTURES](./info-cultures.md)
- [INFO.OBJECTTRANSLATIONS](./info-objecttranslations.md)
- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)

