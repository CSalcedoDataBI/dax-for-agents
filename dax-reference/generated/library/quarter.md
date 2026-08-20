---
name: QUARTER
category: [date-and-time]
primaryCategory: date-and-time
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/quarter-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# QUARTER

Returns the quarter as a number from 1 (January – March) to 4 (October – December).

## Syntax

```dax
QUARTER(<date>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`date`|A date.|

## Return value

An integer number from 1 to 4.

## Remarks

- If the input value is BLANK, the output value is also BLANK.

- This function isn't available in Power Pivot in Excel.

## Example 1

The following DAX query:

```dax
EVALUATE { QUARTER(DATE(2019, 2, 1)), QUARTER(DATE(2018, 12, 31)) } 
```

Returns:

|[Value]  |
|---------|
|1    |
|4    |

## Example 2

The following DAX query:

```dax
EVALUATE
ADDCOLUMNS(
    FILTER(
        VALUES(
            FactInternetSales[OrderDate]), 
            [OrderDate] >= DATE(2008, 3, 31) && [OrderDate] <= DATE(2008, 4, 1)
        ), 
    "Quarter", QUARTER([OrderDate])
)
```

Returns:

|FactInternetSales[OrderDate]  | [Quarter]  |
|---------|---------|
|3/31/2008    |  1  |
|  4/1/2008  |  2   |

## Related content

- [YEAR](./year.md)
- [MONTH](./month.md)
- [DAY](./day.md)
