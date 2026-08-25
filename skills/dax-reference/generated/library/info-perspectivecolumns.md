---
name: INFO.PERSPECTIVECOLUMNS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-perspectivecolumns-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.PERSPECTIVECOLUMNS

Returns a table with information about each perspective column in the semantic model. This function provides metadata about columns included in perspectives.

## Syntax

```dax
INFO.PERSPECTIVECOLUMNS ( [<Restriction name>, <Restriction value>], ... )
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
| [ID] | Unique identifier for the perspective column |
| [PerspectiveTableID] | Identifier of the perspective table containing this column |
| [ColumnID] | Identifier of the column included in the perspective |
| [ModifiedTime] | Timestamp of when the perspective column was last modified |

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
	INFO.PERSPECTIVECOLUMNS()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _PerspectiveColumns =
		SELECTCOLUMNS(
			INFO.PERSPECTIVECOLUMNS(),
			"PerspectiveColumnID", [ID],
			"PerspectiveTableID", [PerspectiveTableID],
			"ColumnID", [ColumnID]
		)
	VAR _Columns = 
		SELECTCOLUMNS(
			INFO.COLUMNS(),
			"ColumnID", [ID],
			"Column Name", [ExplicitName],
			"TableID", [TableID]
		)
	VAR _Tables = 
		SELECTCOLUMNS(
			INFO.TABLES(),
			"TableID", [ID],
			"Table Name", [Name]
		)
	VAR _CombinedTable1 =
		NATURALLEFTOUTERJOIN(
			_PerspectiveColumns,
			_Columns
		)
	VAR _CombinedTable2 =
		NATURALLEFTOUTERJOIN(
			_CombinedTable1,
			_Tables
		)
	RETURN
		SELECTCOLUMNS(
			_CombinedTable2,
			"Table Name", [Table Name],
			"Column Name", [Column Name]
		)
	ORDER BY [Table Name], [Column Name]
```

## See also

- [INFO.PERSPECTIVES](./info-perspectives.md)
- [INFO.PERSPECTIVEHIERARCHIES](./info-perspectivehierarchies.md)
- [INFO.PERSPECTIVEMEASURES](./info-perspectivemeasures.md)
- [INFO.PERSPECTIVETABLES](./info-perspectivetables.md)
- [INFO.TABLES](./info-tables.md)
