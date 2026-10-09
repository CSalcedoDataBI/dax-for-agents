---
name: COMBIN
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/combin-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# COMBIN

Returns the number of combinations for a given number of items. Use COMBIN to determine the total possible number of groups for a given number of items.

## Syntax

```dax
COMBIN(number, number_chosen)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The number of items.|
|`number_chosen`|The number of items in each combination.|

## Return value

Returns the number of combinations for a given number of items.

## Remarks

- Numeric arguments are truncated to integers.

- If either argument is nonnumeric, COMBIN returns the `#VALUE!` error value.

- If number &lt; 0, number_chosen &lt; 0, or number &lt; number_chosen, COMBIN returns the `#NUM!` error value.

- A combination is any set or subset of items, regardless of their internal order. Combinations are distinct from permutations, for which the internal order is significant.

- The number of combinations is as follows, where number = $n$ and number_chosen = $k$:

    $${n \choose k} = \frac{P\_{k,n}}{k!} = \frac{n!}{k!(n-k)!}$$

    Where

    $$P\_{k,n} = \frac{n!}{(n-k)!}$$

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= COMBIN(8,2)`|Possible two-person teams that can be formed from 8 candidates.|28|
