---
name: INFO.ROLES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-roles-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.ROLES

Returns a table with information about each role in the semantic model. This function provides metadata about security roles defined in the model.

## Syntax

```dax
INFO.ROLES ( [<Restriction name>, <Restriction value>], ... )
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

A table whose columns match the schema rowset for roles in the current semantic model.

|Column|Description|
|---|---|
|ID|Unique identifier for the role|
|ModelID|Foreign key to the model containing this role|
|Name|Name of the role|
|Description|Description of the role|
|ModelPermission|Permission level for the role (e.g., Read, ReadRefresh, Administrator)|
|ModifiedTime|Date and time when the role was last modified|

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
	INFO.ROLES()
```

### Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
VAR _Roles = 
    SELECTCOLUMNS(
        INFO.ROLES(),
        "RoleID", [ID],
        "Role Name", [Name],
        "Role Description", [Description],
        "Model Permission", [ModelPermission],
        "Modified", [ModifiedTime]
    )

VAR _RoleMemberships = 
    SELECTCOLUMNS(
        INFO.ROLEMEMBERSHIPS(),
        "RoleID", [RoleID],
        "Member Name", [MemberName],
        "Member Type", [MemberType]
    )

VAR _CombinedTable = 
    NATURALLEFTOUTERJOIN(
        _Roles,
        _RoleMemberships
    )

RETURN
    SELECTCOLUMNS(
        _CombinedTable,
        "Role Name", [Role Name],
        "Role Description", [Role Description],
        "Model Permission", [Model Permission],
        "Member Name", [Member Name],
        "Member Type", [Member Type],
        "Modified", [Modified]
    )
ORDER BY [Role Name], [Member Name]
```

## See also

- [INFO.ROLEMEMBERSHIPS](./info-rolememberships.md)
- [INFO.COLUMNPERMISSIONS](./info-columnpermissions.md)
- [INFO.TABLEPERMISSIONS](./info-tablepermissions.md)
- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
