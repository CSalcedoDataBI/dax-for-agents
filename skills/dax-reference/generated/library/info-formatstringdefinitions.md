---
name: INFO.FORMATSTRINGDEFINITIONS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-formatstringdefinitions-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.FORMATSTRINGDEFINITIONS

Returns a table with information about each format string definition in the semantic model. This function provides metadata about format string definitions for measures and columns.

## Syntax

```dax
INFO.FORMATSTRINGDEFINITIONS ( [<Restriction name>, <Restriction value>], ... )
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
| [ID] | Integer | Unique identifier for the format string definition |
| [ObjectID] | Integer | Identifier of the object (measure or column) that uses this format string |
| [ObjectType] | Integer | Type of object (measure, column, etc.) |
| [Expression] | String | DAX expression that defines the format string |
| [ModifiedTime] | DateTime | When the format string definition was last modified |
| [State] | Integer | Current state of the format string definition |
| [ErrorMessage] | String | Error message if the format string definition is in an error state |

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
	INFO.FORMATSTRINGDEFINITIONS()
```

## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
