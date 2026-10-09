---
name: INFO.RELATIONSHIPS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-relationships-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.RELATIONSHIPS

Returns a table with information about each relationship in the semantic model. This function provides metadata about relationships between tables.

## Syntax

```dax
INFO.RELATIONSHIPS ( [<Restriction name>, <Restriction value>], ... )
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

A table whose columns match the schema rowset for relationships in the current semantic model.

|Column|Description|
|---|---|
|ID|Unique identifier for the relationship|
|ModelID|Foreign key to the model containing this relationship|
|Name|Name of the relationship|
|IsActive|Boolean indicating whether the relationship is active|
|Type|Type of relationship (e.g., OneToMany, ManyToOne)|
|CrossFilteringBehavior|Cross filtering behavior (e.g., OneDirection, BothDirections)|
|JoinOnDateBehavior|Behavior for date-based joins|
|RelyOnReferentialIntegrity|Boolean indicating whether to rely on referential integrity|
|FromTableID|Foreign key to the source table in the relationship|
|FromColumnID|Foreign key to the source column in the relationship|
|FromCardinality|Cardinality on the "from" side of the relationship|
|ToTableID|Foreign key to the target table in the relationship|
|ToColumnID|Foreign key to the target column in the relationship|
|ToCardinality|Cardinality on the "to" side of the relationship|
|State|Current state of the relationship|
|RelationshipStorageID|Foreign key to the relationship storage information|
|RelationshipStorage2ID|Foreign key to secondary relationship storage information|
|ModifiedTime|Date and time when the relationship was last modified|
|RefreshedTime|Date and time when the relationship was last refreshed|
|SecurityFilteringBehavior|Security filtering behavior for the relationship|

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
	INFO.RELATIONSHIPS()
```

### Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
VAR _Relationships = 
    SELECTCOLUMNS(
        INFO.RELATIONSHIPS(),
        "Relationship Name", [Name],
        "Is Active", [IsActive],
        "Type", [Type],
        "Cross Filtering", [CrossFilteringBehavior],
        "From Table ID", [FromTableID],
        "From Column ID", [FromColumnID],
        "To Table ID", [ToTableID],
        "To Column ID", [ToColumnID]
    )

VAR _FromTables = 
    SELECTCOLUMNS(
        INFO.TABLES(),
        "FromTableID", [ID],
        "From Table Name", [Name]
    )

VAR _ToTables = 
    SELECTCOLUMNS(
        INFO.TABLES(),
        "ToTableID", [ID],
        "To Table Name", [Name]
    )

VAR _FromColumns = 
    SELECTCOLUMNS(
        INFO.COLUMNS(),
        "FromColumnID", [ID],
        "From Column Name", [Name]
    )

VAR _ToColumns = 
    SELECTCOLUMNS(
        INFO.COLUMNS(),
        "ToColumnID", [ID],
        "To Column Name", [Name]
    )

VAR _CombinedTable1 = 
    NATURALLEFTOUTERJOIN(
        _Relationships,
        _FromTables
    )

VAR _CombinedTable2 = 
    NATURALLEFTOUTERJOIN(
        _CombinedTable1,
        _ToTables
    )

VAR _CombinedTable3 = 
    NATURALLEFTOUTERJOIN(
        _CombinedTable2,
        _FromColumns
    )

VAR _CombinedTable4 = 
    NATURALLEFTOUTERJOIN(
        _CombinedTable3,
        _ToColumns
    )

RETURN
    SELECTCOLUMNS(
        _CombinedTable4,
        "Relationship Name", [Relationship Name],
        "From Table", [From Table Name],
        "From Column", [From Column Name],
        "To Table", [To Table Name],
        "To Column", [To Column Name],
        "Is Active", [Is Active],
        "Type", [Type],
        "Cross Filtering", [Cross Filtering]
    )
ORDER BY [Relationship Name]
```

## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.PARTITIONS](./info-partitions.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
