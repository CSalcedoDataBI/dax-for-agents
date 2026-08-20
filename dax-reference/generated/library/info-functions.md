---
name: INFO.FUNCTIONS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-functions-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.FUNCTIONS

Returns information about the functions currently available for use in DAX. This corresponds to the MDSCHEMA_FUNCTIONS schema rowset, but returns only DAX (and not MDX) functions by default.

## Syntax

```dax
INFO.FUNCTIONS ( [<Restriction name>, <Restriction value>], ... )
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
| [FUNCTION_NAME] | The name of the DAX function |
| [DESCRIPTION] | A description of what the function does |
| [PARAMETER_LIST] | The list of parameters the function accepts |
| [RETURN_TYPE] | The data type that the function returns |
| [ORIGIN] | The origin or source of the function |
| [INTERFACE_NAME] | The interface name for the function |
| [LIBRARY_NAME] | The library containing the function |
| [DLL_NAME] | The DLL file containing the function implementation |
| [HELP_FILE] | The help file associated with the function |
| [HELP_CONTEXT] | The help context identifier |
| [OBJECT] | The object information for the function |
| [CAPTION] | The display caption for the function |
| [PARAMETERINFO] | Additional parameter information |
| [DIRECTQUERY_PUSHABLE] | Whether the function can be pushed down to DirectQuery sources |
| [VISUAL_CALCULATIONS_INFO] | Information about visual calculations support |

## Remarks

- The result can vary by engine version and compatibility level.
- Permissions required depend on the host. Querying full metadata may require model admin permissions.
- Possible values for [ORIGIN] are 1 (MSOLAP), 2 (UDF), 3 (RELATIONAL), 4 (SCALAR).
- If the [ORIGIN] restriction is not specified, it defaults to 3 (RELATIONAL) or 4 (SCALAR).

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	INFO.FUNCTIONS()
```

## Example 2 - DAX query with filters

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
    SELECTCOLUMNS(
        FILTER(
            INFO.FUNCTIONS(),
            CONTAINSSTRING([FUNCTION_NAME], "DATE")
        ),
        "Function Name", [FUNCTION_NAME],
        "Description", [DESCRIPTION],
        "Return Type", [RETURN_TYPE]
    )
ORDER BY [Function Name]
```
## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
