---
name: INFO.RELATIONSHIPINDEXSTORAGES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-relationshipindexstorages-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.RELATIONSHIPINDEXSTORAGES

Returns a table with information about each relationship index storage in the semantic model. This function provides metadata about relationship index storage characteristics.

## Syntax

```dax
INFO.RELATIONSHIPINDEXSTORAGES ( [<Restriction name>, <Restriction value>], ... )
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

A table whose columns match the schema rowset for relationship index storages in the current semantic model.

|Column|Description|
|---|---|
|ID|Unique identifier for the relationship index storage|
|RelationshipStorageID|Foreign key to the relationship storage using this index|
|IndexType|Type of index used for the relationship|
|Flags|Index configuration flags and options|
|RecordCount|Number of records in the relationship index|
|SecondaryRecordCount|Number of secondary records in the relationship index|
|StorageFolderID|Foreign key to the storage folder containing the index|
|StorageFileID|Foreign key to the storage file containing the index|
|SystemTableID|Foreign key to the primary system table|
|SecondarySystemTableID|Foreign key to the secondary system table|

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
	INFO.RELATIONSHIPINDEXSTORAGES()
```

### Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
VAR _RelationshipIndexStorages = 
    SELECTCOLUMNS(
        INFO.RELATIONSHIPINDEXSTORAGES(),
        "RelationshipStorageID", [RelationshipStorageID],
        "Index Type", [IndexType],
        "Record Count", [RecordCount],
        "Secondary Record Count", [SecondaryRecordCount],
        "Flags", [Flags]
    )

VAR _RelationshipStorages = 
    SELECTCOLUMNS(
        INFO.RELATIONSHIPSTORAGES(),
        "RelationshipStorageID", [ID],
        "RelationshipID", [RelationshipID],
        "Storage Name", [Name]
    )

VAR _Relationships = 
    SELECTCOLUMNS(
        INFO.RELATIONSHIPS(),
        "RelationshipID", [ID],
        "Relationship Name", [Name]
    )

VAR _CombinedTable1 = 
    NATURALLEFTOUTERJOIN(
        _RelationshipIndexStorages,
        _RelationshipStorages
    )

VAR _CombinedTable2 = 
    NATURALLEFTOUTERJOIN(
        _CombinedTable1,
        _Relationships
    )

RETURN
    SELECTCOLUMNS(
        _CombinedTable2,
        "Relationship Name", [Relationship Name],
        "Storage Name", [Storage Name],
        "Index Type", [Index Type],
        "Record Count", [Record Count],
        "Secondary Record Count", [Secondary Record Count]
    )
ORDER BY [Relationship Name]
```

## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
