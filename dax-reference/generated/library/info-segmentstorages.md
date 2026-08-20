---
name: INFO.SEGMENTSTORAGES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-segmentstorages-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.SEGMENTSTORAGES

Returns a table with information about each segment storage in the semantic model. This function provides metadata about segment storage characteristics.

## Syntax

```dax
INFO.SEGMENTSTORAGES ( [<Restriction name>, <Restriction value>], ... )
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

A table whose columns match the schema rowset for segment storages in the current semantic model.

|Column|Description|
|---|---|
|ID|Unique identifier for the segment storage|
|ColumnPartitionStorageID|Foreign key to the column partition storage using this segment|
|SegmentCount|Number of segments in the storage|
|StorageFileID|Foreign key to the storage file containing the segment data|

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
	INFO.SEGMENTSTORAGES()
```

### Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
VAR _SegmentStorages = 
    SELECTCOLUMNS(
        INFO.SEGMENTSTORAGES(),
        "ColumnPartitionStorageID", [ColumnPartitionStorageID],
        "Segment Count", [SegmentCount],
        "StorageFileID", [StorageFileID]
    )

VAR _ColumnPartitionStorages = 
    SELECTCOLUMNS(
        INFO.COLUMNPARTITIONSTORAGES(),
        "ColumnPartitionStorageID", [ID],
        "ColumnStorageID", [ColumnStorageID],
        "PartitionStorageID", [PartitionStorageID]
    )

VAR _StorageFiles = 
    SELECTCOLUMNS(
        INFO.STORAGEFILES(),
        "StorageFileID", [ID],
        "File Name", [FileName]
    )

VAR _CombinedTable1 = 
    NATURALLEFTOUTERJOIN(
        _SegmentStorages,
        _ColumnPartitionStorages
    )

VAR _CombinedTable2 = 
    NATURALLEFTOUTERJOIN(
        _CombinedTable1,
        _StorageFiles
    )

RETURN
    SELECTCOLUMNS(
        _CombinedTable2,
        "Column Storage ID", [ColumnStorageID],
        "Partition Storage ID", [PartitionStorageID],
        "Segment Count", [Segment Count],
        "File Name", [File Name]
    )
ORDER BY [Column Storage ID]
```

## See also

- [INFO.COLUMNSTORAGES](./info-columnstorages.md)
- [INFO.COLUMNPARTITIONSTORAGES](./info-columnpartitionstorages.md)
- [INFO.DICTIONARYSTORAGES](./info-dictionarystorages.md)
- [INFO.STORAGEFILES](./info-storagefiles.md)
- [INFO.TABLESTORAGES](./info-tablestorages.md)
