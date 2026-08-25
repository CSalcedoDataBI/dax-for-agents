---
name: INFO.EXPRESSIONS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-expressions-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.EXPRESSIONS

Returns a table with information about each expression in the semantic model. This function provides metadata about expressions defined in the model.

## Syntax

```dax
INFO.EXPRESSIONS ( [<Restriction name>, <Restriction value>], ... )
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
|--|--|--|
| [ID] | Integer | Unique identifier for the expression |
| [ModelID] | Integer | Identifier of the model containing the expression |
| [Name] | String | Name of the expression |
| [Description] | String | Description of the expression |
| [Kind] | Integer | Type of expression (e.g., calculated table, shared expression) |
| [Expression] | String | DAX expression text |
| [ModifiedTime] | DateTime | When the expression was last modified |
| [QueryGroupID] | Integer | Identifier of the query group if applicable |
| [ParameterValuesColumnID] | Integer | Column identifier for parameter values if applicable |
| [MAttributes] | String | Additional attributes in JSON format |
| [LineageTag] | String | Lineage tag for tracking purposes |
| [SourceLineageTag] | String | Source lineage tag for tracking purposes |

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
	INFO.EXPRESSIONS()
```

## See also

- [INFO.MODEL](./info-model.md)
- [INFO.PROPERTIES](./info-properties.md)
- [INFO.CATALOGS](./info-catalogs.md)
- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
