---
name: BITOR
category: [logical]
primaryCategory: logical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/bitor-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# BITOR

Returns a bitwise OR of two numbers.

## Syntax

```dax
BITOR(<number>, <number>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Number`|Any scalar expression that returns number. If not an integer, it is truncated.|

## Return value

A bitwise OR of two numbers.

## Remarks

- This function supports both positive and negative numbers.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/logical/bitor.md`](../../examples/logical/bitor.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query:

```dax
EVALUATE 
    { BITOR(9, 10) }
```

Returns 11.

## Related content

- [BITAND](./bitand.md)
- [BITXOR](./bitxor.md)
- [BITLSHIFT](./bitlshift.md)
- [BITRSHIFT](./bitrshift.md)
