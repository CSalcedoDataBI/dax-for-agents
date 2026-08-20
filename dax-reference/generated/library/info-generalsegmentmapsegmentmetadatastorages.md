---
name: INFO.GENERALSEGMENTMAPSEGMENTMETADATASTORAGES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-generalsegmentmapsegmentmetadatastorages-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.GENERALSEGMENTMAPSEGMENTMETADATASTORAGES

Returns a table with information about each general segment map segment metadata storage in the semantic model. This function provides metadata about segment map storage characteristics.

## Syntax

```dax
INFO.GENERALSEGMENTMAPSEGMENTMETADATASTORAGES ( [<Restriction name>, <Restriction value>], ... )
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
| [ID] | Unique identifier for the general segment map segment metadata storage |
| [SegmentMapStorageID] | Identifier linking to the segment map storage |
| [RecordCount] | Number of records in the segment |
| [Ordinal] | Ordinal position of the segment |

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
	INFO.GENERALSEGMENTMAPSEGMENTMETADATASTORAGES()
```

## Example 2 - DAX query with SELECTCOLUMNS

```dax
EVALUATE
    SELECTCOLUMNS(
        INFO.GENERALSEGMENTMAPSEGMENTMETADATASTORAGES(),
        "Segment Map Storage ID", [SegmentMapStorageID],
        "Record Count", [RecordCount],
        "Ordinal", [Ordinal]
    )
```

## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
