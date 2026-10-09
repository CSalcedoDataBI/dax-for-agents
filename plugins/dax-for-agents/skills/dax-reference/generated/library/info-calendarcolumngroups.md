---
name: INFO.CALENDARCOLUMNGROUPS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-calendarcolumngroups-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.CALENDARCOLUMNGROUPS

Returns a table with information about each calendar column group in the semantic model. Calendar column groups associate columns with categories within a calendar.

## Syntax

```dax
INFO.CALENDARCOLUMNGROUPS ( [<Restriction name>, <Restriction value>], ... )
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
| ID | Unique identifier for the calendar column group |
| CalendarID | ID of the calendar this calendar column group belongs to |
| TimeUnit | The category associated with this column group (e.g. DayOfWeek) |
| ModifiedTime | When the calendar column group was last modified |

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
	INFO.CALENDARCOLUMNGROUPS()
```

### Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
VAR _CalendarColumnGroups = 
    SELECTCOLUMNS(
        INFO.CALENDARCOLUMNGROUPS(),
        "GroupID", [ID],
        "CalendarID", [CalendarID],
        "Category", [TimeUnit]
    )

VAR _CalendarColumnReferences = 
    SELECTCOLUMNS(
        INFO.CALENDARCOLUMNREFERENCES(),
        "GroupID", [CalendarColumnGroupID],
        "ColumnID", [ColumnID],
		"IsPrimaryColumn", [IsPrimaryColumn]
    )

VAR _Calendars = 
    SELECTCOLUMNS(
        INFO.CALENDARS(),
        "CalendarID", [ID],
        "Calendar Name", [Name]
    )

VAR _Columns = 
    SELECTCOLUMNS(
        INFO.COLUMNS(),
        "ColumnID", [ID],
        "Column Name", [ExplicitName]
    )

VAR _GroupsWithReferences = 
    NATURALLEFTOUTERJOIN(
        _CalendarColumnGroups,
        _CalendarColumnReferences
    )

VAR _WithCalendars = 
    NATURALLEFTOUTERJOIN(
        _GroupsWithReferences,
        _Calendars
    )

VAR _WithColumns = 
    NATURALLEFTOUTERJOIN(
        _WithCalendars,
        _Columns
    )

RETURN
    SELECTCOLUMNS(
        _WithColumns,
        "Calendar Name", [Calendar Name],
        "Category", [Category],
		"Is Primary Column", [IsPrimaryColumn],
        "Column Name", [Column Name]
    )
ORDER BY [Calendar Name], [Category], [Is Primary Column], [Column Name]
```

## See also

- [INFO.CALENDARS](./info-calendars.md)
- [INFO.CALENDARCOLUMNREFERENCES](./info-calendarcolumnreferences.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
