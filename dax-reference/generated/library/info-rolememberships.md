---
name: INFO.ROLEMEMBERSHIPS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-rolememberships-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.ROLEMEMBERSHIPS

Returns a table with information about each role membership in the semantic model. This function provides metadata about role memberships and security settings.

## Syntax

```dax
INFO.ROLEMEMBERSHIPS ( [<Restriction name>, <Restriction value>], ... )
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

A table whose columns match the schema rowset for role memberships in the current semantic model.

|Column|Description|
|---|---|
|ID|Unique identifier for the role membership|
|RoleID|Foreign key to the role containing this membership|
|MemberName|Name of the member (user or group)|
|MemberID|Unique identifier for the member|
|IdentityProvider|Identity provider for the member authentication|
|MemberType|Type of member (e.g., User, Group)|
|ModifiedTime|Date and time when the role membership was last modified|

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
	INFO.ROLEMEMBERSHIPS()
```

## See also

- [INFO.ROLES](./info-roles.md)
- [INFO.COLUMNPERMISSIONS](./info-columnpermissions.md)
- [INFO.TABLEPERMISSIONS](./info-tablepermissions.md)
- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
