---
name: ISBLANK
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/isblank-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# ISBLANK

Checks whether a value is blank, and returns `TRUE` or `FALSE`.

## Syntax

```dax
ISBLANK(<value>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`value`|The value or expression you want to test.|

## Return value

A Boolean value of `TRUE` if the value is blank; otherwise `FALSE`.

## Remarks

To learn more about best practices when working with BLANKS, see [Avoid converting BLANKs to values in DAX](https://learn.microsoft.com/en-us/dax/best-practices/dax-avoid-converting-blank).

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/information/isblank.md`](../../examples/information/isblank.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

This formula computes the increase or decrease ratio in sales compared to the previous year. The example uses the IF function to check the value for the previous year's sales in order to avoid a divide by zero error.

```dax
//Sales to Previous Year Ratio

= IF( ISBLANK('CalculatedMeasures'[PreviousYearTotalSales])
   , BLANK()
   , ( 'CalculatedMeasures'[Total Sales]-'CalculatedMeasures'[PreviousYearTotalSales] )
      /'CalculatedMeasures'[PreviousYearTotalSales])
```

Result,

|Row Labels|Total Sales|Total Sales Previous Year|Sales to Previous Year Ratio|
|--------------|---------------|-----------------------------|--------------------------------|
|2005|$10,209,985.08|||
|2006|$28,553,348.43|$10,209,985.08|179.66%|
|2007|$39,248,847.52|$28,553,348.43|37.46%|
|2008|$24,542,444.68|$39,248,847.52|-37.47%|
|Grand Total|$102,554,625.71|||

## Related content

- [Information functions](https://learn.microsoft.com/en-us/dax/information-functions-dax)
