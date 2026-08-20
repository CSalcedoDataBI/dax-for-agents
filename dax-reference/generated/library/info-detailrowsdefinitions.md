---
name: INFO.DETAILROWSDEFINITIONS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-detailrowsdefinitions-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.DETAILROWSDEFINITIONS

Returns a table with information about each detail rows definition in the semantic model. This function provides metadata about detail rows definitions for measures.

## Syntax

```dax
INFO.DETAILROWSDEFINITIONS ( [<Restriction name>, <Restriction value>], ... )
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
| [ID] | Integer | Unique identifier for the detail rows definition |
| [ObjectID] | Integer | Identifier of the object this detail rows definition belongs to |
| [ObjectType] | String | Type of the object (e.g., measure, table) |
| [Expression] | String | DAX expression for the detail rows definition |
| [ModifiedTime] | DateTime | Date and time when the detail rows definition was last modified |
| [State] | Integer | State of the detail rows definition |
| [ErrorMessage] | String | Error message if the detail rows definition has an error |

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
	INFO.DETAILROWSDEFINITIONS()
```
## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
