---
name: INFO.CALCULATIONITEMS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-calculationitems-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.CALCULATIONITEMS

Returns a table with information about each calculation item in the semantic model. This function provides metadata about calculation items within calculation groups.

## Syntax

```dax
INFO.CALCULATIONITEMS ( [<Restriction name>, <Restriction value>], ... )
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
| [ID] | Integer | The unique identifier of the calculation item |
| [CalculationGroupID] | Integer | The unique identifier of the calculation group that contains this calculation item |
| [FormatStringDefinition] | String | The format string definition for the calculation item |
| [Name] | String | The name of the calculation item |
| [Description] | String | The description of the calculation item |
| [ModifiedTime] | DateTime | The date and time when the calculation item was last modified |
| [State] | String | The state of the calculation item |
| [ErrorMessage] | String | Any error message associated with the calculation item |
| [Expression] | String | The DAX expression for the calculation item |
| [Ordinal] | Integer | The ordinal position of the calculation item within its calculation group |

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
	INFO.CALCULATIONITEMS()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _CalculationItems =
		INFO.CALCULATIONITEMS()

	VAR _CalculationGroups = 
		SELECTCOLUMNS(
			INFO.CALCULATIONGROUPS(),
			"CalculationGroupID", [ID],
			"Calculation Group Description", [Description]
		)

	VAR _CombinedTable =
		NATURALLEFTOUTERJOIN(
			_CalculationItems,
			_CalculationGroups
		)

	RETURN
		SELECTCOLUMNS(
			_CombinedTable,
			"Calculation Item Name", [Name],
			"Calculation Group Description", [Calculation Group Description],
			"Expression", [Expression],
			"Ordinal", [Ordinal]
		)
		
	ORDER BY [Calculation Group Description], [Ordinal]
```
## See also

- [INFO.CALCULATIONGROUPS](./info-calculationgroups.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO.KPIS](./info-kpis.md)
- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
