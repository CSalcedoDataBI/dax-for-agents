---
name: INFO.SEGMENTMAPSTORAGES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-segmentmapstorages-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.SEGMENTMAPSTORAGES

Returns a table with information about each segment map storage in the semantic model. This function provides metadata about segment map storage characteristics.

## Syntax

```dax
INFO.SEGMENTMAPSTORAGES ( [<Restriction name>, <Restriction value>], ... )
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

A table whose columns match the schema rowset for segment map storages in the current semantic model.

|Column|Description|
|---|---|
|ID|Unique identifier for the segment map storage|
|PartitionStorageID|Foreign key to the partition storage using this segment map|
|Type|Type of segment map storage|
|RecordCount|Number of records in the segment map|
|SegmentCount|Number of segments in the segment map|
|RecordsPerSegment|Average number of records per segment|

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
	INFO.SEGMENTMAPSTORAGES()
```

### Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
VAR _SegmentMapStorages = 
    SELECTCOLUMNS(
        INFO.SEGMENTMAPSTORAGES(),
        "PartitionStorageID", [PartitionStorageID],
        "Type", [Type],
        "Record Count", [RecordCount],
        "Segment Count", [SegmentCount],
        "Records Per Segment", [RecordsPerSegment]
    )

VAR _PartitionStorages = 
    SELECTCOLUMNS(
        INFO.PARTITIONSTORAGES(),
        "PartitionStorageID", [ID],
        "PartitionID", [PartitionID],
        "Storage Name", [Name]
    )

VAR _Partitions = 
    SELECTCOLUMNS(
        INFO.PARTITIONS(),
        "PartitionID", [ID],
        "TableID", [TableID],
        "Partition Name", [Name]
    )

VAR _Tables = 
    SELECTCOLUMNS(
        INFO.TABLES(),
        "TableID", [ID],
        "Table Name", [Name]
    )

VAR _CombinedTable1 = 
    NATURALLEFTOUTERJOIN(
        _SegmentMapStorages,
        _PartitionStorages
    )

VAR _CombinedTable2 = 
    NATURALLEFTOUTERJOIN(
        _CombinedTable1,
        _Partitions
    )

VAR _CombinedTable3 = 
    NATURALLEFTOUTERJOIN(
        _CombinedTable2,
        _Tables
    )

RETURN
    SELECTCOLUMNS(
        _CombinedTable3,
        "Table Name", [Table Name],
        "Partition Name", [Partition Name],
        "Storage Type", [Type],
        "Record Count", [Record Count],
        "Segment Count", [Segment Count],
        "Records Per Segment", [Records Per Segment]
    )
ORDER BY [Table Name], [Partition Name]
```

## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
