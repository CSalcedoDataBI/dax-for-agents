---
name: INFO.DELTATABLEMETADATASTORAGES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-deltatablemetadatastorages-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.DELTATABLEMETADATASTORAGES

Returns a table with information about each delta table metadata storage in the semantic model. This function provides metadata about delta table storage characteristics.

## Syntax

```dax
INFO.DELTATABLEMETADATASTORAGES ( [<Restriction name>, <Restriction value>], ... )
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
| [ID] | Integer | Unique identifier for the delta table metadata storage |
| [PartitionStorageID] | Integer | Identifier of the partition storage |
| [DataSourceReference] | String | Reference to the data source |
| [TableName] | String | Name of the delta table |
| [RootLocation] | String | Root location of the delta table |
| [CurrentVersion] | Integer | Current version of the delta table |
| [TableObjectID] | String | Object identifier for the table |
| [DatamartObjectID] | String | Object identifier for the datamart |
| [FramedSchemaName] | String | Name of the framed schema |
| [FallbackReason] | String | Reason for fallback behavior |
| [DeltaColumnMappingMode] | String | Column mapping mode for the delta table |
| [DeltaLogETag] | String | ETag for the delta log |
| [ArtifactObjectId] | String | Object identifier for the artifact |
| [ArtifactSecurityVersion] | String | Security version of the artifact |

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
	INFO.DELTATABLEMETADATASTORAGES()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _DeltaTableMetadataStorages =
		INFO.DELTATABLEMETADATASTORAGES()

	VAR _PartitionStorages = 
		SELECTCOLUMNS(
			INFO.PARTITIONSTORAGES(),
			"PartitionStorageID", [ID],
			"Partition Storage Name", [Name]
		)

	VAR _CombinedTable =
		NATURALLEFTOUTERJOIN(
			_DeltaTableMetadataStorages,
			_PartitionStorages
		)

	RETURN
		SELECTCOLUMNS(
			_CombinedTable,
			"Table Name", [TableName],
			"Partition Storage Name", [Partition Storage Name],
			"Current Version", [CurrentVersion],
			"Root Location", [RootLocation],
			"Fallback Reason", [FallbackReason]
		)
	ORDER BY [Table Name]
```
## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
