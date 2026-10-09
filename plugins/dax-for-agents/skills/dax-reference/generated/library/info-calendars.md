---
name: INFO.CALENDARS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-calendars-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.CALENDARS

Returns a table with information about each calendar in the semantic model. This function provides metadata about calendars defined on tables.

## Syntax

```dax
INFO.CALENDARS ( [<Restriction name>, <Restriction value>], ... )
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
|---|---|
| ID | Unique identifier for the calendar |
| TableID | ID of the table this calendar belongs to |
| Name | Name of the calendar |
| Description | Description of the calendar |
| LineageTag | Lineage tag for tracking calendar lineage |
| SourceLineageTag | Source lineage tag |
| ModifiedTime | When the calendar was last modified |

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
	INFO.CALENDARS()
```

### Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
VAR _Calendars = 
    SELECTCOLUMNS(
        INFO.CALENDARS(),
        "CalendarID", [ID],
        "Calendar Name", [Name],
        "Description", [Description],
        "TableID", [TableID]
    )

VAR _Tables = 
    SELECTCOLUMNS(
        INFO.TABLES(),
        "TableID", [ID],
        "Table Name", [Name]
    )

VAR _CombinedTable = 
    NATURALLEFTOUTERJOIN(
        _Calendars,
        _Tables
    )

RETURN
    SELECTCOLUMNS(
        _CombinedTable,
        "Table Name", [Table Name],
        "Calendar Name", [Calendar Name],
        "Description", [Description]
    )
ORDER BY [Table Name], [Calendar Name]
```

## See also

- [INFO.CALENDARCOLUMNGROUPS](./info-calendarcolumngroups.md)
- [INFO.CALENDARCOLUMNREFERENCES](./info-calendarcolumnreferences.md)
- [INFO.TABLES](./info-tables.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
