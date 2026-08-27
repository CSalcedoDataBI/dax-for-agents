---
name: CONTAINSROW
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/containsrow-function-dax.md@323524c
sourceDate: 06/29/2026
notes: false
examples: 6
---
# CONTAINSROW function

Returns `TRUE` if there exists at least one row where all columns have specified values.

## Syntax

```dax
CONTAINSROW(<Table>, <Value> [, <Value> [, …] ] ) 
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Table`|A table to test.|
|`Value`|Any valid DAX expression that returns a scalar value.|

## Return value

 `TRUE`  or `FALSE`.

## Remarks

- Other than syntax, the `IN` operator and CONTAINSROW function are functionally equivalent.

    ```dax
    <scalarExpr> IN <tableExpr> 
    ( <scalarExpr1>, <scalarExpr2>, … ) IN <tableExpr>
    ```

  - The number of scalarExprN must match the number of columns in tableExpr.
  - NOT IN isn't an operator in DAX. To perform the logical negation of the IN operator, put NOT in front of the entire expression. For example, NOT [Color] IN { "Red", "Yellow", "Blue" }.

- Unlike the = operator, the IN operator and the CONTAINSROW function perform strict comparison. For example, the BLANK value doesn't match 0.

## Ejemplos ejecutables

**6** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/information/containsrow.md`](../../examples/information/containsrow.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

_Examples in this article can be used with the sample Adventure Works DW 2020 Power BI Desktop model. To get the model, see [DAX sample model](https://aka.ms/dax-docs-samples)._

### Example 1

The following DAX queries:

```dax
EVALUATE
FILTER ( ALL ( Product[Color] ), ( [Color] ) IN { "Red", "Yellow", "Blue" } )
ORDER BY [Color]
```

and

```dax
EVALUATE
FILTER (
    ALL ( Product[Color] ),
    CONTAINSROW ( { "Red", "Yellow", "Blue" }, [Color] )
)
ORDER BY [Color]
```

Return the following table with a single column:

[Color]  |
---------|---------
Blue     |
Red     |
Yellow  |

### Example 2

The following equivalent DAX queries:

```dax
EVALUATE
FILTER ( ALL ( Product[Color] ), NOT [Color] IN { "Red", "Yellow", "Blue" } )
ORDER BY [Color]
```

and

```dax
EVALUATE
FILTER (
    ALL ( Product[Color] ),
    NOT CONTAINSROW ( { "Red", "Yellow", "Blue" }, [Color] )
)
ORDER BY [Color]
```

Return the following table with a single column:

[Color]  |
---------|---------
Black     |
Grey     |
Multi  |
NA   |
Silver  |
Silver/Black  |
White |

## Related content

- [IN operator](https://learn.microsoft.com/en-us/dax/dax-operator-reference#logical-operators)
- [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries)
