---
name: IFERROR
category: [logical]
primaryCategory: logical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/iferror-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# IFERROR

Evaluates an expression and returns a specified value if the expression returns an error; otherwise returns the value of the expression itself.

## Syntax

```dax
IFERROR(value, value_if_error)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`value`|Any value or expression.|
|`value_if_error`|Any value or expression.|

## Return value

A scalar of the same type as `value`

## Remarks

- You can use the IFERROR function to trap and handle errors in an expression.

- If `value` or `value_if_error` is an empty cell, IFERROR treats it as an empty string value ("").

- The IFERROR function is based on the IF function, and uses the same error messages, but has fewer arguments. The relationship between the IFERROR function and the IF function as follows:

  `IFERROR(A,B) := IF(ISERROR(A), B, A)`

  Values that are returned for A and B must be of the same data type; therefore, the column or expression used for `value` and the value returned for `value_if_error` must be the same data type.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

- For best practices when using IFERROR, see [Appropriate use of error functions](https://learn.microsoft.com/en-us/dax/best-practices/dax-error-functions).

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/logical/iferror.md`](../../examples/logical/iferror.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example returns 9999 if the expression 25/0 evaluates to an error. If the expression returns a value other than error, that value is passed to the invoking expression.

```dax
= IFERROR(25/0,9999)
```

## Related content

- [Logical functions](https://learn.microsoft.com/en-us/dax/logical-functions-dax)
