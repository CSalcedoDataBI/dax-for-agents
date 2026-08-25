---
name: INFO.DATASOURCES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-datasources-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.DATASOURCES

Returns a table with information about each data source in the semantic model. This function provides metadata about the data sources connected to the model.

## Syntax

```dax
INFO.DATASOURCES ( [<Restriction name>, <Restriction value>], ... )
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
| [ID] | Integer | Unique identifier for the data source |
| [ModelID] | Integer | Identifier of the semantic model |
| [Name] | String | Name of the data source |
| [Description] | String | Description of the data source |
| [Type] | String | Type of the data source |
| [ConnectionString] | String | Connection string for the data source |
| [ImpersonationMode] | String | Impersonation mode used for the data source |
| [Account] | String | Account used for impersonation |
| [Password] | String | Password for the data source (typically masked) |
| [MaxConnections] | Integer | Maximum number of connections allowed |
| [Isolation] | String | Isolation level for the data source |
| [Timeout] | Integer | Timeout value for connections |
| [Provider] | String | Data provider for the data source |
| [ModifiedTime] | DateTime | Date and time when the data source was last modified |
| [ConnectionDetails] | String | Additional connection details |
| [Options] | String | Additional options for the data source |
| [Credential] | String | Credential information |
| [ContextExpression] | String | Context expression for the data source |

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
	INFO.DATASOURCES()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _DataSources =
		INFO.DATASOURCES()

	VAR _Model = 
		SELECTCOLUMNS(
			INFO.MODEL(),
			"ModelID", [ID],
			"Model Name", [Name]
		)

	VAR _CombinedTable =
		NATURALLEFTOUTERJOIN(
			_DataSources,
			_Model
		)

	RETURN
		SELECTCOLUMNS(
			_CombinedTable,
			"Model Name", [Model Name],
			"Data Source Name", [Name],
			"Data Source Type", [Type],
			"Max Connections", [MaxConnections],
			"Modified Time", [ModifiedTime]
		)
	ORDER BY [Data Source Name]
```
## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
