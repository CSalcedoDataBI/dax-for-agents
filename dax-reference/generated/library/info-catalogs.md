---
name: INFO.CATALOGS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-catalogs-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.CATALOGS

Returns a table with information about each catalog in the semantic model. This function provides metadata about the catalogs available in the current context.

## Syntax

```dax
INFO.CATALOGS ( [<Restriction name>, <Restriction value>], ... )
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
|-------------|-----------|-------------|
| [CATALOG_NAME] | String | The name of the catalog |
| [DESCRIPTION] | String | The description of the catalog |
| [ROLES] | String | The roles associated with the catalog |
| [DATE_MODIFIED] | DateTime | The date and time when the catalog was last modified |
| [COMPATIBILITY_LEVEL] | Integer | The compatibility level of the catalog |
| [TYPE] | Integer | The type of the catalog |
| [VERSION] | Integer | The version of the catalog |
| [DATABASE_ID] | String | The unique identifier of the database |
| [DATABASE_GUID] | String | The GUID of the database |
| [DATE_QUERIED] | DateTime | The date and time when the catalog was queried |
| [CURRENTLY_USED] | Boolean | Whether the catalog is currently being used |
| [POPULARITY] | Double | The popularity score of the catalog |
| [WEIGHTEDPOPULARITY] | Double | The weighted popularity score of the catalog |
| [CLIENTCACHEREFRESHPOLICY] | Integer | The client cache refresh policy setting |
| [ENCRYPTION_LEVEL] | String | The encryption level used for the catalog |
| [CRYPTOKEY_UPDATED] | DateTime | The date and time when the encryption key was last updated |

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
	INFO.CATALOGS()
```
## See also

- [INFO.MODEL](./info-model.md)
- [INFO.PROPERTIES](./info-properties.md)
- [INFO.EXPRESSIONS](./info-expressions.md)
- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
