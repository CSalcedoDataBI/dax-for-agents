---
name: EXTERNALMEASURE
category: [other]
primaryCategory: other
returns: scalar
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/externalmeasure-function-dax.md@323524c
sourceDate: 06/29/2026
notes: false
examples: 0
---
# EXTERNALMEASURE

Invokes a measure defined in a remote model and returns its result with the specified `datatype`.

## Syntax

```dax
EXTERNALMEASURE(<measurename>, <datatype>, <connection>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`measurename`|Name of the measure as defined in the remote model.|
|`datatype`|An enumeration that includes: BOOLEAN/LOGICAL, CURRENCY/DECIMAL, DATETIME, DOUBLE, INTEGER/INT64, STRING/TEXT, VARIANT.|
|`connection`|The name of the connection to the remote model.|

## Return value

Result of the remote measure with the datatype specified in `datatype`.

## Remarks

- You can only use this function in [composite models that have a remote model connection](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-composite-models#composite-models-on-power-bi-semantic-models-and-analysis-services).

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

If the remote model connection is called **DirectQuery to AS - Adventure Works DW 2020** and the remote model defines a measure called **Total Sales** you can invoke that measure and return its result as **currency** using:

```dax
Total Sales Remote =
EXTERNALMEASURE (
    "Total Sales",
    CURRENCY,
    "DirectQuery to AS - Adventure Works DW 2020"
)
```

## Related content

- [Composite models](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-composite-models)
