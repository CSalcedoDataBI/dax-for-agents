---
name: INFO.STORAGEFOLDERS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-storagefolders-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.STORAGEFOLDERS

Returns a table with information about all table storage in the semantic model. This information helps you understand the model.

## Syntax

```dax
INFO.STORAGEFOLDERS([<Restriction name>, <Restriction value>], ...)
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

|Column|Description|
|---|---|
|[ID]|The name of the database|
|[OwnerID]||
|[OwnerType]||
|[Path]||

## Remarks

Can only be run by users with write permission on the semantic model and not when live connected to the semantic model in Power BI Desktop. This function can be used in [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries), and can't be used in calculations.

## Example 1 - DAX query

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	INFO.STORAGEFOLDERS()
```
## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
