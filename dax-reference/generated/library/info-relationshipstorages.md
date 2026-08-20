---
name: INFO.RELATIONSHIPSTORAGES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-relationshipstorages-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.RELATIONSHIPSTORAGES

Returns a table with information about each relationship storage in the semantic model. This function provides metadata about how relationships are stored.

## Syntax

```dax
INFO.RELATIONSHIPSTORAGES ( [<Restriction name>, <Restriction value>], ... )
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

A table whose columns match the schema rowset for relationship storages in the current semantic model.

|Column|Description|
|---|---|
|ID|Unique identifier for the relationship storage|
|RelationshipID|Foreign key to the relationship using this storage|
|Name|Name of the relationship storage|
|DefinitionType|Type definition for the relationship storage|
|Cardinality|Cardinality characteristics of the relationship storage|
|Flags|Storage flags and configuration options|
|RelationshipIndexStorageID|Foreign key to the relationship index storage|

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
	INFO.RELATIONSHIPSTORAGES()
```

### Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
VAR _RelationshipStorages = 
    SELECTCOLUMNS(
        INFO.RELATIONSHIPSTORAGES(),
        "RelationshipID", [RelationshipID],
        "Storage Name", [Name],
        "Definition Type", [DefinitionType],
        "Cardinality", [Cardinality],
        "Flags", [Flags]
    )

VAR _Relationships = 
    SELECTCOLUMNS(
        INFO.RELATIONSHIPS(),
        "RelationshipID", [ID],
        "Relationship Name", [Name],
        "Is Active", [IsActive],
        "Type", [Type]
    )

VAR _CombinedTable = 
    NATURALLEFTOUTERJOIN(
        _RelationshipStorages,
        _Relationships
    )

RETURN
    SELECTCOLUMNS(
        _CombinedTable,
        "Relationship Name", [Relationship Name],
        "Storage Name", [Storage Name],
        "Is Active", [Is Active],
        "Type", [Type],
        "Definition Type", [Definition Type],
        "Cardinality", [Cardinality]
    )
ORDER BY [Relationship Name]
```
## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
