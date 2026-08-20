---
name: INFO.MODEL
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-model-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.MODEL

Returns a table with information about the model in the semantic model. This function provides metadata about the model itself and its properties.

## Syntax

```dax
INFO.MODEL ( [<Restriction name>, <Restriction value>], ... )
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

| Column | Data Type | Description |
|--------|-----------|-------------|
| [ID] | Integer | Unique identifier for the model |
| [Name] | String | Name of the model |
| [Description] | String | Description of the model |
| [StorageLocation] | Integer | Storage location indicator |
| [DefaultMode] | Integer | Default processing mode for the model |
| [DefaultDataView] | Integer | Default data view setting |
| [Culture] | String | Culture identifier for the model (e.g., "en-US") |
| [Collation] | String | Collation setting for the model |
| [ModifiedTime] | DateTime | Date and time when the model was last modified |
| [StructureModifiedTime] | DateTime | Date and time when the model structure was last modified |
| [Version] | Integer | Version number of the model |
| [DataAccessOptions] | String | JSON object containing data access configuration options |
| [DefaultMeasureID] | Integer | ID of the default measure, if any |
| [DefaultPowerBIDataSourceVersion] | Integer | Default Power BI data source version |
| [ForceUniqueNames] | Boolean | Whether unique names are enforced |
| [DiscourageImplicitMeasures] | Boolean | Whether implicit measures are discouraged |
| [DataSourceVariablesOverrideBehavior] | Integer | Behavior for data source variable overrides |
| [DataSourceDefaultMaxConnections] | Integer | Default maximum connections for data sources |
| [SourceQueryCulture] | String | Culture used for source queries |
| [MAttributes] | String | Model attributes |
| [DiscourageCompositeModels] | Boolean | Whether composite models are discouraged |
| [AutomaticAggregationOptions] | String | Options for automatic aggregations |
| [DisableAutoExists] | Integer | Auto exists disable setting |
| [VersionMarker] | String | Version marker for the model |

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
	INFO.MODEL()
```
## See also

- [INFO.PROPERTIES](./info-properties.md)
- [INFO.EXPRESSIONS](./info-expressions.md)
- [INFO.CATALOGS](./info-catalogs.md)
- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
