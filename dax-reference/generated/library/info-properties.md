---
name: INFO.PROPERTIES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-properties-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.PROPERTIES

Returns a table with information about each property in the semantic model. This function provides metadata about properties defined for model objects.

## Syntax

```dax
INFO.PROPERTIES ( [<Restriction name>, <Restriction value>], ... )
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

A table whose columns match the schema rowset for properties in the current semantic model.

|Column|Description|
|---|---|
|PropertyName|Name of the property|
|PropertyDescription|Description explaining the purpose and usage of the property|
|PropertyType|Data type of the property value (e.g., String, Integer, Boolean)|
|PropertyAccessType|Access level of the property (e.g., Read, Write, ReadWrite)|
|IsRequired|Boolean indicating whether the property is required|
|Value|Current value of the property|

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
	INFO.PROPERTIES()
```

## See also

- [INFO.MODEL](./info-model.md)
- [INFO.EXPRESSIONS](./info-expressions.md)
- [INFO.CATALOGS](./info-catalogs.md)
- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
