---
name: CALCULATE
category: [filter]
primaryCategory: filter
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/calculate-function-dax.md@323524c
sourceDate: 06/29/2026
notes: true
examples: 0
---
# CALCULATE

Evaluates an expression in a modified filter context.

> [!NOTE]
> There's also the [CALCULATETABLE](./calculatetable.md) function. It performs exactly the same functionality, except it modifies the [filter context](https://learn.microsoft.com/en-us/dax/dax-overview#filter-context) applied to an expression that returns a _table object_.
>

## Syntax

```dax
CALCULATE(<expression>[, <filter1> [, <filter2> [, …]]])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`expression`|The expression to evaluate.|
|`filter1, filter2,…`|(Optional) Boolean expressions or table expressions that defines filters, or filter modifier functions.|

The expression you use as the first parameter works like a measure.

Filters can be:

- Boolean filter expressions
- Table filter expressions
- Filter modification functions

When you use multiple filters, you can evaluate them by using the AND (`&&`) logical operator, which means all conditions must be `TRUE`, or by the OR (`||`) logical operator, which means either condition can be true. For more information, see [DAX operators > logical operators](https://learn.microsoft.com/en-us/dax/dax-operator-reference#logical-operators).

#### Boolean filter expressions

A Boolean expression filter is an expression that evaluates to `TRUE` or `FALSE`. It must follow several rules:

- It can reference columns from a single table.
- It can't reference measures.
- It can't use a nested CALCULATE function.
- It can't use functions that scan or return a table unless you pass them as arguments to aggregation functions.
- It can contain an aggregation function that returns a scalar value. For example:

  ```dax
  Total sales on the last selected date =
  CALCULATE (
      SUM ( Sales[Sales Amount] ),
      'Sales'[OrderDateKey] = MAX ( 'Sales'[OrderDateKey] )
  )
  ```

#### Table filter expression

A table expression filter applies a table object as a filter. It could be a reference to a model table, but more likely it's a function that returns a table object. You can use the [FILTER](./filter.md) function to apply complex filter conditions, including those that you can't define by a Boolean filter expression.

#### Filter modifier functions

Filter modifier functions let you do more than simply add filters. They give you extra control when modifying filter context.

|Function|Purpose|
|--------|--------------|
|[REMOVEFILTERS](./removefilters.md)|Remove all filters, or filters from one or more columns of a table, or from all columns of a single table.|
|[ALL](./all.md) <sup>1</sup>, [ALLEXCEPT](./allexcept.md), [ALLNOBLANKROW](./allnoblankrow.md)|Remove filters from one or more columns, or from all columns of a single table.|
|[KEEPFILTERS](./keepfilters.md)|Add filter without removing existing filters on the same columns.|
|[USERELATIONSHIP](./userelationship.md)|Engage an inactive relationship between related columns, in which case the active relationship automatically becomes inactive.|
|[CROSSFILTER](./crossfilter.md)|Modify filter direction (from both to single, or from single to both) or disable a relationship.|

<sup>1</sup> The ALL function and its variants behave as both filter modifiers and as functions that return table objects. If your tool supports the REMOVEFILTERS function, use it to remove filters.

## Return value

The value that results from the expression.

## Remarks

- When you provide filter expressions, the CALCULATE function modifies the filter context to evaluate the expression. For each filter expression, two standard outcomes exist when the filter expression isn't wrapped in the KEEPFILTERS function:
  - If the columns or tables aren't in the filter context, new filters are added to the filter context to evaluate the expression.
  - If the columns or tables are already in the filter context, the existing filters are overwritten by the new filters to evaluate the CALCULATE expression.

- Using the CALCULATE function _without filters_ achieves a specific requirement. It transitions row context to filter context. This transition is required when an expression (not a model measure) that summarizes model data needs to be evaluated in row context. This scenario can happen in a calculated column formula or when an expression in an iterator function is evaluated. When you use a model measure in row context, context transition is automatic.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

_Examples in this article can be used with the sample Adventure Works DW 2020 Power BI Desktop model. To get the model, see [DAX sample model](https://aka.ms/dax-docs-samples)._

The following **Sales** table measure definition produces a revenue result, but only for products that have the color blue.

```dax
Blue Revenue =
CALCULATE ( SUM ( Sales[Sales Amount] ), 'Product'[Color] = "Blue" )
```

|Category|Sales Amount|Blue Revenue|
|--------|------------|------------|
|Accessories|$1,272,057.89|$165,406.62|
|Bikes|$94,620,526.21|$8,374,313.88|
|Clothing|$2,117,613.45|$259,488.37|
|Components|$11,799,076.66|$803,642.10|
|**Total**|**$109,809,274.20**|**$9,602,850.97**|

The CALCULATE function evaluates the sum of the **Sales** table **Sales Amount** column in a modified filter context. A new filter is added to the **Product** table **Color** column—or, the filter overwrites any filter that's already applied to the column.

The following **Sales** table measure definition produces a ratio of sales over sales for all sales channels.

```dax
Revenue % Total Channel =
DIVIDE (
    SUM ( Sales[Sales Amount] ),
    CALCULATE (
        SUM ( Sales[Sales Amount] ),
        REMOVEFILTERS ( 'Sales Order'[Channel] )
    )
)
```

|Channel|Sales Amount|Revenue % Total Channel|
|-------|------------|-----------------------|
|Internet|$29,358,677.22|26.74%|
|Reseller|$80,450,596.98|73.26%|
|**Total**|**$109,809,274.20**|**100.00%**|

The [DIVIDE](./divide.md) function divides an expression that sums of the **Sales** table **Sales Amount** column value (in the filter context) by the same expression in a modified filter context. It's the CALCULATE function that modifies the filter context by using the REMOVEFILTERS function, which is a filter modifier function. It removes filters from the **Sales Order** table **Channel** column.

The following **Customer** table calculated column definition classifies customers into a loyalty class.  It's a very simple scenario: When the revenue produced by the customer is less than $2500, they're classified as _Low_; otherwise they're _High_.

```dax
Customer Segment =
IF (
    CALCULATE (
        SUM ( Sales[Sales Amount] ),
        ALLEXCEPT ( Customer, Customer[CustomerKey] )
    ) < 2500,
    "Low",
    "High"
)
```

|Customer Segment|Customer Count|Sales Amount|
|----------------|--------------|------------|
|High|4,637|$102,670,663.09|
|Low|13,848|$7,138,611.11|
|**Total**|**18,485**|**$109,809,274.20**|

In this example, row context is converted to the filter context. It's known as _context transition_. The [ALLEXCEPT](./allexcept.md) function removes filters from all **Customer** table columns except the **CustomerKey** column.

## Related content

- [Filter context](https://learn.microsoft.com/en-us/dax/dax-overview#filter-context)
- [Row context](https://learn.microsoft.com/en-us/dax/dax-overview#row-context)
- [CALCULATETABLE function](./calculatetable.md)
- [Filter functions](https://learn.microsoft.com/en-us/dax/filter-functions-dax)
