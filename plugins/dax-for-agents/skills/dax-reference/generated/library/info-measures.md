---
name: INFO.MEASURES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-measures-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.MEASURES

Returns a table with information about each measure in the semantic model, with columns that match the schema rowset for measure objects (for example, name, expression, and state).

## Syntax

```dax
INFO.MEASURES ( [<Restriction name>, <Restriction value>], ... )
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
| [ID] | Unique identifier for the measure |
| [TableID] | Identifier of the table containing the measure |
| [Name] | Name of the measure |
| [Description] | Description of the measure |
| [DataType] | Data type of the measure result |
| [Expression] | DAX expression defining the measure calculation |
| [FormatString] | Format string for displaying measure values |
| [IsHidden] | Boolean indicating if the measure is hidden from client tools |
| [State] | Current state of the measure (e.g., Ready, Processing, Error) |
| [ModifiedTime] | Timestamp of when the measure was last modified |
| [StructureModifiedTime] | Timestamp of when the measure structure was last modified |
| [KPIID] | Identifier of the KPI associated with this measure (if applicable) |
| [IsSimpleMeasure] | Boolean indicating if this is a simple measure |
| [ErrorMessage] | Error message if the measure is in an error state |
| [DisplayFolder] | Display folder for organizing measures in client tools |
| [DetailRowsDefinitionID] | Identifier of the detail rows definition for this measure |
| [DataCategory] | Data category classification for the measure |
| [LineageTag] | Lineage tag for tracking data lineage |
| [SourceLineageTag] | Source lineage tag from the original data source |

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
	INFO.MEASURES()
```

## See also

- [INFO.CALCULATIONGROUPS](./info-calculationgroups.md)
- [INFO.CALCULATIONITEMS](./info-calculationitems.md)
- [INFO.KPIS](./info-kpis.md)
- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
