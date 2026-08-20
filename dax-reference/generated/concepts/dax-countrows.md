---
title: Use COUNTROWS instead of COUNT in DAX
topic: best-practice
summary: Best practices for using the COUNTROWS functions.
source: query-languages/dax/best-practices/dax-countrows.md@323524c
sourceDate: 08/25/2021
---
# Use COUNTROWS instead of COUNT

As a data modeler, sometimes you might need to write a DAX expression that counts table rows. The table could be a model table or an expression that returns a table.

Your requirement can be achieved in two ways. You can use the [COUNT](../library/count.md) function to count column values, or you can use the [COUNTROWS](../library/countrows.md) function to count table rows. Both functions will achieve the same result, providing that the counted column contains no BLANKs.

The following measure definition presents an example. It calculates the number of **OrderDate** column values.

```dax
Sales Orders =
COUNT(Sales[OrderDate])
```

Providing that the granularity of the **Sales** table is one row per sales order, and the **OrderDate** column does not contain BLANKs, then the measure will return a correct result.

However, the following measure definition is a better solution.

```dax
Sales Orders =
COUNTROWS(Sales)
```

There are three reasons why the second measure definition is better:

- It's more efficient, and so it will perform better.
- It doesn't consider BLANKs contained in any column of the table.
- The intention of formula is clearer, to the point of being self-describing.

## Recommendation

When it's your intention to count table rows, it's recommended you always use the COUNTROWS function.

## Related content

- Learning path: [Use DAX in Power BI Desktop](https://learn.microsoft.com/en-us/training/paths/dax-power-bi/)
- Questions? [Try asking the Power BI Community](https://community.powerbi.com/)
- Suggestions? [Contribute ideas to improve Power BI](https://ideas.powerbi.com)
