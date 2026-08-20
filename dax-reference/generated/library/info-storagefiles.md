---
name: INFO.STORAGEFILES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-storagefiles-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.STORAGEFILES

Returns a table with information about each storage file in the semantic model. This function provides metadata about storage files and their characteristics.

## Syntax

```dax
INFO.STORAGEFILES ( [<Restriction name>, <Restriction value>], ... )
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

A table whose columns match the schema rowset for storage files in the current semantic model.

|Column|Description|
|---|---|
|ID|Unique identifier for the storage file|
|OwnerID|Identifier of the object that owns this storage file|
|OwnerType|Type of the object that owns this storage file|
|StorageFolderID|Foreign key to the storage folder containing this file|
|FileName|Name of the storage file|

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
	INFO.STORAGEFILES()
```

### Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
VAR _StorageFiles = 
    SELECTCOLUMNS(
        INFO.STORAGEFILES(),
        "OwnerID", [OwnerID],
        "Owner Type", [OwnerType],
        "StorageFolderID", [StorageFolderID],
        "File Name", [FileName]
    )

VAR _StorageFolders = 
    SELECTCOLUMNS(
        INFO.STORAGEFOLDERS(),
        "StorageFolderID", [ID],
        "Folder Name", [Name]
    )

VAR _CombinedTable = 
    NATURALLEFTOUTERJOIN(
        _StorageFiles,
        _StorageFolders
    )

RETURN
    SELECTCOLUMNS(
        _CombinedTable,
        "Folder Name", [Folder Name],
        "File Name", [File Name],
        "Owner Type", [Owner Type],
        "Owner ID", [OwnerID]
    )
ORDER BY [Folder Name], [File Name]
```

## See also

- [INFO.COLUMNSTORAGES](./info-columnstorages.md)
- [INFO.COLUMNPARTITIONSTORAGES](./info-columnpartitionstorages.md)
- [INFO.DICTIONARYSTORAGES](./info-dictionarystorages.md)
- [INFO.SEGMENTSTORAGES](./info-segmentstorages.md)
- [INFO.TABLESTORAGES](./info-tablestorages.md)
