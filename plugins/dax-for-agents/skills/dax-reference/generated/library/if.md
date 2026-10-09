---
name: IF
category: [logical]
primaryCategory: logical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/if-function-dax.md@323524c
sourceDate: 06/29/2026
notes: false
examples: 3
---
# IF

Checks a condition, and returns one value when it's `TRUE`, otherwise it returns a second value.

## Syntax

```dax
IF(<logical_test>, <value_if_true>[, <value_if_false>])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`logical_test`|Any value or expression that can be evaluated to `TRUE` or `FALSE`.|
|`value_if_true`|The value that's returned if the logical test is `TRUE`.|
|`value_if_false`|(Optional) The value that's returned if the logical test is `FALSE`. If omitted, BLANK is returned.|

## Return value

Either `value_if_true`, `value_if_false`, or `BLANK`.

## Remarks

- The IF function can return a variant data type if `value_if_true` and `value_if_false` are of different data types, but the function attempts to return a single data type if both `value_if_true` and `value_if_false` are of numeric data types. In the latter case, the IF function implicitly converts data types to accommodate both values.

    For example, the formula `IF(<condition>, TRUE(), 0)` returns `TRUE` or 0, but the formula `IF(<condition>, 1.0, 0)` returns only decimal values even though `value_if_false` is of the whole number data type. To learn more about implicit data type conversion, see [Data types](https://learn.microsoft.com/en-us/dax/dax-overview#data-types).

- To execute the branch expressions regardless of the condition expression, use [IF.EAGER](./if-eager.md) instead.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/logical/if.md`](../../examples/logical/if.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following **Product** table calculated column definitions use the IF function in different ways to classify each product based on its list price.

The first example tests whether the **List Price** column value is less than 500. When this condition is true, the function returns **Low**. Because there's no `value_if_false` value, the function returns BLANK.

_Examples in this article can be used with the sample Adventure Works DW 2020 Power BI Desktop model. To get the model, see [DAX sample model](https://aka.ms/dax-docs-samples)._

```dax
Price Group =
IF ( 'Product'[List Price] < 500, "Low" )
```

The second example uses the same test, but this time includes a `value_if_false` value. So, the formula classifies each product as either `Low` or `High`.

```dax
Price Group =
IF ( 'Product'[List Price] < 500, "Low", "High" )
```

The third example uses the same test, but this time nests an IF function to perform an additional test. So, the formula classifies each product as either `Low`, `Medium`, or `High`.

```dax
Price Group =
IF (
    'Product'[List Price] < 500,
    "Low",
    IF ( 'Product'[List Price] < 1500, "Medium", "High" )
)
```

> [!TIP]
> When you need to nest multiple IF functions, the [SWITCH](./switch.md) function might be a better option. This function provides a more elegant way to write an expression that returns more than two possible values.

## Related content

- [IF.EAGER function](./if-eager.md) 
- [SWITCH function (DAX)](./switch.md)
- [Logical functions](https://learn.microsoft.com/en-us/dax/logical-functions-dax)
