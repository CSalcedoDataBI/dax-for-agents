---
name: INFO.COLUMNPERMISSIONS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-columnpermissions-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.COLUMNPERMISSIONS

Returns a table with information about each column permission in the semantic model. This function provides metadata about column-level security settings.

## Syntax

```dax
INFO.COLUMNPERMISSIONS ( [<Restriction name>, <Restriction value>], ... )
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
| [ID] | Integer | The unique identifier of the column permission |
| [TablePermissionID] | Integer | The identifier of the table permission this column permission belongs to |
| [ColumnID] | Integer | The identifier of the column |
| [ModifiedTime] | DateTime | The date and time when the column permission was last modified |
| [MetadataPermission] | Integer | The metadata permission level for the column |

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
	INFO.COLUMNPERMISSIONS()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _ColumnPermissions =
		INFO.COLUMNPERMISSIONS()

	VAR _TablePermissions = 
		SELECTCOLUMNS(
			INFO.TABLEPERMISSIONS(),
			"TablePermissionID", [ID],
			"Table Permission Name", [Name],
			"RoleID", [RoleID],
			"TableID", [TableID]
		)

	VAR _Roles = 
		SELECTCOLUMNS(
			INFO.ROLES(),
			"RoleID", [ID],
			"Role Name", [Name]
		)

	VAR _Tables = 
		SELECTCOLUMNS(
			INFO.TABLES(),
			"TableID", [ID],
			"Table Name", [Name]
		)

	VAR _Columns = 
		SELECTCOLUMNS(
			INFO.COLUMNS(),
			"ColumnID", [ID],
			"Column Name", [ExplicitName]
		)

	VAR _CombinedWithTablePermissions =
		NATURALLEFTOUTERJOIN(
			_ColumnPermissions,
			_TablePermissions
		)

	VAR _CombinedWithRoles =
		NATURALLEFTOUTERJOIN(
			_CombinedWithTablePermissions,
			_Roles
		)

	VAR _CombinedWithTables =
		NATURALLEFTOUTERJOIN(
			_CombinedWithRoles,
			_Tables
		)

	VAR _CombinedWithColumns =
		NATURALLEFTOUTERJOIN(
			_CombinedWithTables,
			_Columns
		)

	RETURN
		SELECTCOLUMNS(
			_CombinedWithColumns,
			"Role Name", [Role Name],
			"Table Name", [Table Name],
			"Column Name", [Column Name],
			"Metadata Permission", [MetadataPermission],
			"Modified Time", [ModifiedTime]
		)
	ORDER BY [Role Name], [Table Name], [Column Name]
```
## See also

- [INFO.ROLES](./info-roles.md)
- [INFO.ROLEMEMBERSHIPS](./info-rolememberships.md)
- [INFO.TABLEPERMISSIONS](./info-tablepermissions.md)
- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
