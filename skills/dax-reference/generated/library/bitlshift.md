---
name: BITLSHIFT
category: [logical]
primaryCategory: logical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/bitlshift-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# BITLSHIFT

Returns a number shifted left by the specified number of bits.

## Syntax

```dax
BITLSHIFT(<Number>, <Shift_Amount>) 
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Number`|Any DAX expression that returns an integer expression.|
|`Shift_Amount`|Any DAX expression that returns an integer expression.|

## Return value

An integer value.

## Remarks

- Be sure to understand the nature of bitshift operations and overflow/underflow of integers before using DAX bitshift functions.
- If Shift_Amount is negative, it will shift in the opposite direction.
- If absolute value of Shift_Amount is larger than 64, there will be no error but will result in overflow/underflow.
- There’s no limit on Number, but the result may overflow/underflow.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/logical/bitlshift.md`](../../examples/logical/bitlshift.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

### Example 1

The following DAX query:

```dax
EVALUATE 
    { BITLSHIFT(2, 3) }
```

Returns 16.

### Example 2

The following DAX query:

```dax
EVALUATE 
    { BITLSHIFT(128, -1) }
```

Returns 64.

### Example 3

The following DAX query:

```dax
Define 
    Measure Sales[LeftShift] = BITLSHIFT(SELECTEDVALUE(Sales[Amount]), 3)

EVALUATE 
SUMMARIZECOLUMNS(
    Sales[Amount],
    "LEFTSHIFT", 
    [LeftShift]
)
```

Shifts left each sales amount with 3 bits and returns the bit-shifted sales amount.

## Related content

- [BITRSHIFT](./bitrshift.md)
- [BITAND](./bitand.md)
- [BITOR](./bitor.md)
- [BITXOR](./bitxor.md)
