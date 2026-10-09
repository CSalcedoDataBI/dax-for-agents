---
name: INFO.USERDEFINEDFUNCTIONS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-userdefinedfunctions-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.USERDEFINEDFUNCTIONS

Returns a table with information about each user-defined function in the semantic model, with columns that match the schema rowset for user-defined function objects (for example, name, expression, and state).

## Syntax

```dax
INFO.USERDEFINEDFUNCTIONS ( [<Restriction name>, <Restriction value>], ... )
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
| [ID] | Unique identifier for the user-defined function |
| [ModelID] | Identifier of the model containing the user-defined function |
| [Name] | Name of the user-defined function |
| [Description] | Description of the user-defined function |
| [Expression] | DAX expression defining the user-defined function |
| [IsHidden] | Boolean indicating if the user-defined function is hidden from client tools |
| [State] | Current state of the user-defined function (e.g., Ready, Error) |
| [ErrorMessage] | Error message if the user-defined function is in an error state |
| [ModifiedTime] | Timestamp of when the user-defined function was last modified |
| [StructureModifiedTime] | Timestamp of when the user-defined function structure was last modified |
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
	INFO.USERDEFINEDFUNCTIONS()
```

## See also

- [INFO.FUNCTIONS](./info-functions.md)
- [INFO.MEASURES](./info-measures.md)