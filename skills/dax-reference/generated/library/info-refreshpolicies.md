---
name: INFO.REFRESHPOLICIES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-refreshpolicies-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.REFRESHPOLICIES

Returns a table with information about each refresh policy in the semantic model. This function provides metadata about refresh policies defined for tables.

## Syntax

```dax
INFO.REFRESHPOLICIES ( [<Restriction name>, <Restriction value>], ... )
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

A table whose columns match the schema rowset for refresh policies in the current semantic model.

|Column|Description|
|---|---|
|ID|Unique identifier for the refresh policy|
|TableID|Foreign key to the table this refresh policy applies to|
|PolicyType|Type of refresh policy (e.g., Incremental, Rolling Window)|
|RollingWindowGranularity|Granularity for rolling window refresh (e.g., Day, Month, Year)|
|RollingWindowPeriods|Number of periods to keep in rolling window|
|IncrementalGranularity|Granularity for incremental refresh (e.g., Day, Month, Year)|
|IncrementalPeriods|Number of periods for incremental refresh|
|IncrementalPeriodsOffset|Offset periods for incremental refresh timing|
|PollingExpression|DAX expression used for polling to detect changes|
|SourceExpression|DAX expression defining the source data for refresh|
|Mode|Refresh mode configuration|

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
	INFO.REFRESHPOLICIES()
```

### Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
VAR _RefreshPolicies = 
    SELECTCOLUMNS(
        INFO.REFRESHPOLICIES(),
        "TableID", [TableID],
        "Policy Type", [PolicyType],
        "Rolling Window Granularity", [RollingWindowGranularity],
        "Rolling Window Periods", [RollingWindowPeriods],
        "Incremental Granularity", [IncrementalGranularity],
        "Incremental Periods", [IncrementalPeriods]
    )

VAR _Tables = 
    SELECTCOLUMNS(
        INFO.TABLES(),
        "TableID", [ID],
        "Table Name", [Name],
        "Description", [Description]
    )

VAR _CombinedTable = 
    NATURALLEFTOUTERJOIN(
        _RefreshPolicies,
        _Tables
    )

RETURN
    SELECTCOLUMNS(
        _CombinedTable,
        "Table Name", [Table Name],
        "Description", [Description],
        "Policy Type", [Policy Type],
        "Rolling Window Granularity", [Rolling Window Granularity],
        "Rolling Window Periods", [Rolling Window Periods],
        "Incremental Granularity", [Incremental Granularity],
        "Incremental Periods", [Incremental Periods]
    )
ORDER BY [Table Name]
```

## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
