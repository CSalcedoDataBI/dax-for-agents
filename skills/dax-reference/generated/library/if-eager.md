---
name: IF.EAGER
category: [logical]
primaryCategory: logical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/if-eager-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# IF.EAGER

Checks a condition, and returns one value when `TRUE`, otherwise it returns a second value. It uses an *eager* execution plan which always executes the branch expressions regardless of the condition expression.

## Syntax

```dax
IF.EAGER(<logical_test>, <value_if_true>[, <value_if_false>])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`logical_test`|Any value or expression that can be evaluated to `TRUE` or `FALSE`.|
|`value_if_true`|The value that's returned if the logical test is `TRUE`.|
|`value_if_false`|(Optional) The value that's returned if the logical test is `FALSE`. If omitted, `BLANK` is returned.|

## Return value

Either `value_if_true`, `value_if_false`, or `BLANK`.

## Remarks

- The IF.EAGER function can return a variant data type if value_if_true and value_if_false are of different data types, but the function attempts to return a single data type if both `value_if_true` and `value_if_false` are of numeric data types. In the latter case, the IF.EAGER function will implicitly convert data types to accommodate both values. 

    For example, the formula `IF.EAGER(<condition>, TRUE(), 0)` returns `TRUE` or 0, but the formula `IF.EAGER(<condition>, 1.0, 0)` returns only decimal values even though `value_if_false` is of the whole number data type. To learn more about implicit data type conversion, see [Data types](https://learn.microsoft.com/en-us/dax/dax-overview#data-types).

- IF.EAGER has the same functional behavior as the IF function, but performance may differ due to differences in execution plans. `IF.EAGER(<logical_test>, <value_if_true>, <value_if_false>)` has the same execution plan as the following DAX expression:

    ```dax
  
    VAR _value_if_true = <value_if_true>
    VAR _value_if_false = <value_if_false>
    RETURN
    IF (<logical_test>, _value_if_true, _value_if_false)
    ```

    Note: The two branch expressions are evaluated regardless of the condition expression.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/logical/if-eager.md`](../../examples/logical/if-eager.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

See [IF Examples](./if.md#examples).

## Related content

- [IF function](./if.md)
- [Logical functions](https://learn.microsoft.com/en-us/dax/logical-functions-dax)
