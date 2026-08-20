---
name: INFO.TABLES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-tables-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.TABLES

Returns a table with information about each table in the semantic model, with columns that match the schema rowset for table objects (for example, name, description, and visibility).

## Syntax

```dax
INFO.TABLES ( [<Restriction name>, <Restriction value>], ... )
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

A table whose columns match the schema rowset for table objects in the current semantic model.

|Column|Description|
|---|---|
|ID|Unique identifier for the table|
|ModelID|Foreign key to the model containing this table|
|Name|Name of the table|
|DataCategory|Data category classification for the table|
|Description|Description of the table|
|IsHidden|Boolean indicating whether the table is hidden from client applications|
|TableStorageID|Foreign key to the table storage information|
|ModifiedTime|Date and time when the table was last modified|
|StructureModifiedTime|Date and time when the table structure was last modified|
|SystemFlags|System flags for internal table management|
|ShowAsVariationsOnly|Boolean indicating whether the table should only show variations|
|IsPrivate|Boolean indicating whether the table is private|
|DefaultDetailRowsDefinitionID|Foreign key to the default detail rows definition|
|AlternateSourcePrecedence|Precedence order for alternate data sources|
|RefreshPolicyID|Foreign key to the refresh policy for incremental refresh|
|CalculationGroupID|Foreign key to the calculation group if this table is a calculation group|
|ExcludeFromModelRefresh|Boolean indicating whether to exclude this table from model refresh|
|LineageTag|Lineage tag for tracking table lineage|
|SourceLineageTag|Source lineage tag from the original data source|
|SystemManaged|Boolean indicating whether the table is system-managed|

## Remarks

- Useful for documentation and governance scenarios.
- Permissions required depend on the host. Querying full metadata may require model admin permissions.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	INFO.TABLES()
```

### Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
VAR _Tables = 
    SELECTCOLUMNS(
        INFO.TABLES(),
        "TableID", [ID],
        "Table Name", [Name],
        "Description", [Description],
        "Is Hidden", [IsHidden],
        "Calculation Group ID", [CalculationGroupID],
        "Refresh Policy ID", [RefreshPolicyID]
    )

VAR _CalculationGroups = 
    SELECTCOLUMNS(
        INFO.CALCULATIONGROUPS(),
        "CalculationGroupID", [ID],
        "Calculation Group Name", [Name]
    )

VAR _RefreshPolicies = 
    SELECTCOLUMNS(
        INFO.REFRESHPOLICIES(),
        "RefreshPolicyID", [ID],
        "Policy Type", [PolicyType],
        "Incremental Periods", [IncrementalPeriods]
    )

VAR _CombinedTable1 = 
    NATURALLEFTOUTERJOIN(
        _Tables,
        _CalculationGroups
    )

VAR _CombinedTable2 = 
    NATURALLEFTOUTERJOIN(
        _CombinedTable1,
        _RefreshPolicies
    )

RETURN
    SELECTCOLUMNS(
        _CombinedTable2,
        "Table Name", [Table Name],
        "Description", [Description],
        "Is Hidden", [Is Hidden],
        "Calculation Group", [Calculation Group Name],
        "Policy Type", [Policy Type],
        "Incremental Periods", [Incremental Periods]
    )
ORDER BY [Table Name]
```

## See also

- [INFO.COLUMNS](./info-columns.md)
- [INFO.PARTITIONS](./info-partitions.md)
- [INFO.RELATIONSHIPS](./info-relationships.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
