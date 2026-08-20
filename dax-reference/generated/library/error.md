---
name: ERROR
category: [other]
primaryCategory: other
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/error-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ERROR

Raises an error with an error message.

## Syntax

```dax
ERROR(<text>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`text`|A text string containing an error message.|

## Return value

None

## Remarks

- The ERROR function can be placed in a DAX expression anywhere a scalar value is expected.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Example 1

The following DAX query:

```dax
DEFINE
MEASURE DimProduct[Measure] =
        IF(
            SELECTEDVALUE(DimProduct[Color]) = "Red",
            ERROR("red color encountered"),
            SELECTEDVALUE(DimProduct[Color])
        )
EVALUATE SUMMARIZECOLUMNS(DimProduct[Color], "Measure", [Measure])
ORDER BY [Color]
```

Fails and raises and error message containing "red color encountered".

## Example 2

The following DAX query:

```dax
DEFINE
MEASURE DimProduct[Measure] =
        IF(
            SELECTEDVALUE(DimProduct[Color]) = "Magenta",
            ERROR("magenta color encountered"),
            SELECTEDVALUE(DimProduct[Color])
        )
EVALUATE SUMMARIZECOLUMNS(DimProduct[Color], "Measure", [Measure])
ORDER BY [Color]
```

Returns the following table:

DimProduct[Color]  |[Measure]
---------|---------
Black     |        Black
Blue     |       Blue
Grey     |      Grey
Multi     |    Multi
NA     |        NA
Red     |     Red
Silver     |     Silver
Silver\Black     |   Silver\Black
White    |       White
Yellow    |        Yellow

Because Magenta is not one of the product colors, the ERROR function is not executed.
