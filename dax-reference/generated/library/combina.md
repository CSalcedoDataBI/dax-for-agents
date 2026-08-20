---
name: COMBINA
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/combina-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# COMBINA

Returns the number of combinations (with repetitions) for a given number of items.

## Syntax

```dax
COMBINA(number, number_chosen)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|Must be greater than or equal to 0, and greater than or equal to Number_chosen. Non-integer values are truncated.|
|`number_chosen`|Must be greater than or equal to 0. Non-integer values are truncated.|

## Return value

Returns the number of combinations (with repetitions) for a given number of items.

## Remarks

- If the value of either argument is outside of its constraints, COMBINA returns the `#NUM!` error value.

- If either argument is a non-numeric value, COMBINA returns the `#VALUE!` error value.

- The following equation is used, where $N$ is Number and $M$ is Number_chosen:

    $${N+M-1 \choose N-1}$$

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= COMBINA(4,3)`|Returns the number of combinations (with repetitions) for 4 and 3.|20|
|`= COMBINA(10,3)`|Returns the number of combinations (with repetitions) for 10 and 3.|220|
