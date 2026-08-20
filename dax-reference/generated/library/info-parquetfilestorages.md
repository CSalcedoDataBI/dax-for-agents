---
name: INFO.PARQUETFILESTORAGES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-parquetfilestorages-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.PARQUETFILESTORAGES

Returns a table with information about each Parquet file storage in the semantic model. This function provides metadata about Parquet file storage characteristics.

## Syntax

```dax
INFO.PARQUETFILESTORAGES ( [<Restriction name>, <Restriction value>], ... )
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

| Column | Data Type | Description |
|--------|-----------|-------------|
| [ID] | Integer | Unique identifier for the Parquet file storage |
| [DeltaTableMetadataStorageID] | Integer | ID of the associated delta table metadata storage |
| [Size] | Integer | Size of the Parquet file in bytes |
| [Location] | String | Location path of the Parquet file |
| [CreatedVersion] | Integer | Version when the file was created |
| [DeletedVersion] | Integer | Version when the file was deleted, if applicable |
| [RowgroupCount] | Integer | Number of row groups in the Parquet file |
| [Ordinal] | Integer | Ordinal position of the file |
| [ETag] | String | Entity tag for file versioning and caching |
| [DeletionVectorFileLocation] | String | Location of the deletion vector file |
| [DeletionVectorBitmapOffset] | Integer | Offset for the deletion vector bitmap |
| [DeletionVectorBitmapSize] | Integer | Size of the deletion vector bitmap |
| [DeletionVectorFileETag] | String | Entity tag for the deletion vector file |

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
	INFO.PARQUETFILESTORAGES()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _ParquetFileStorages =
		INFO.PARQUETFILESTORAGES()

	VAR _DeltaTableMetadataStorages = 
		SELECTCOLUMNS(
			INFO.DELTATABLEMETADATASTORAGES(),
			"DeltaTableMetadataStorageID", [ID],
			"Table Name", [TableName],
			"Root Location", [RootLocation]
		)

	VAR _CombinedTable =
		NATURALLEFTOUTERJOIN(
			_ParquetFileStorages,
			_DeltaTableMetadataStorages
		)

	RETURN
		SELECTCOLUMNS(
			_CombinedTable,
			"Table Name", [Table Name],
			"File Location", [Location],
			"File Size", [Size],
			"Rowgroup Count", [RowgroupCount],
			"Created Version", [CreatedVersion],
			"Deleted Version", [DeletedVersion]
		)
	ORDER BY [Table Name], [Created Version]
```
## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
