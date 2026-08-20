---
name: INFO.CALCDEPENDENCY
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-calcdependency-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.CALCDEPENDENCY

Returns a table with information about each calculation dependency in the semantic model. This information helps you understand the model.

## Syntax

```dax
INFO.CALCDEPENDENCY ( [<Restriction name>, <Restriction value>], ... )
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
|---|---|
| [DATABASE_NAME] | The name of the semantic model. |
| [OBJECT_TYPE] | The type of object. |
| [TABLE] | The object's table name. |
| [OBJECT] | The name of the object. |
| [EXPRESSION] | The DAX formula of the object. |
| [REFERENCED_OBJECT_TYPE] | The type of object this object references. The "Object" is dependent on this object. |
| [REFERENCED_TABLE] | The referenced object's table name. |
| [REFERENCED_OBJECT] | The referenced object's name. | 
| [REFERENCED_EXPRESSION] | The referenced object's DAX formula. |
| [QUERY] | The query, if specified as a restriction. |

## Remarks

Can only be run by users with write permission on the semantic model and not when live connected to the semantic model in Power BI Desktop. This function can be used in [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries), and can't be used in calculations.

You can also call this DAX function with INFO.DEPENDENCIES.

## Example 1 - DAX query

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	INFO.CALCDEPENDENCY()
```

This DAX query returns a table with all of the columns of this DAX function.

## Example 2 - DAX query with restriction

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view) and limits the results to the Total Sales measure:

```dax
EVALUATE
	INFO.CALCDEPENDENCY("Query", "EVALUATE { [Total Sales] }")
```

If a restriction has double-quotes they can be escaped with another double-quote and you can optionally use a VAR to hold the value.

```dax
EVALUATE
	VAR _query =
		"EVALUATE
		SELECTCOLUMNS(
			'Date',
			""Date"", [Date]
		)"
	RETURN
		INFO.CALCDEPENDENCY(
			"Query",
			_query
		)
```
## See also

- [INFO.DEPENDENCIES](./info-dependencies.md)
- [INFO.RELATEDCOLUMNDETAILS](./info-relatedcolumndetails.md)
- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
