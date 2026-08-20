---
title: Use SELECTEDVALUE instead of VALUES in DAX
topic: best-practice
summary: Best practices for using the SELECTEDVALUE functions.
source: query-languages/dax/best-practices/dax-selectedvalue.md@323524c
sourceDate: 08/25/2021
---
# Use SELECTEDVALUE instead of VALUES

As a data modeler, sometimes you might need to write a DAX expression that tests whether a column is filtered by a specific value.

In earlier versions of DAX, this requirement was safely achieved by using a pattern involving three DAX functions; [IF](../library/if.md), [HASONEVALUE](../library/hasonevalue.md) and [VALUES](../library/values.md). The following measure definition presents an example. It calculates the sales tax amount, but only for sales made to Australian customers.

```dax
Australian Sales Tax =
IF(
    HASONEVALUE(Customer[Country-Region]),
    IF(
        VALUES(Customer[Country-Region]) = "Australia",
        [Sales] * 0.10
    )
)
```

In the example, the HASONEVALUE function returns TRUE only when a single value of the **Country-Region** column is visible in the current filter context. When it's TRUE, the VALUES function is compared to the literal text "Australia". When the VALUES function returns TRUE, the **Sales** measure is multiplied by 0.10 (representing 10%). If the HASONEVALUE function returns FALSE—because more than one value filters the column—the first IF function returns BLANK.

The use of the HASONEVALUE is a defensive technique. It's required because it's possible that multiple values filter the **Country-Region** column. In this case, the VALUES function returns a table of multiple rows. Comparing a table of multiple rows to a scalar value results in an error.

## Recommendation

It's recommended that you use the [SELECTEDVALUE](../library/selectedvalue.md) function. It achieves the same outcome as the pattern described in this article, yet more efficiently and elegantly.

Using the SELECTEDVALUE function, the example measure definition is now rewritten.

```dax
Australian Sales Tax =
IF(
    SELECTEDVALUE(Customer[Country-Region]) = "Australia",
    [Sales] * 0.10
)
```

> [!TIP]
> It's possible to pass an _alternate result_ value into the SELECTEDVALUE function. The alternate result value is returned when either no filters—or multiple filters—are applied to the column.

## Related content

- Learning path: [Use DAX in Power BI Desktop](https://learn.microsoft.com/en-us/training/paths/dax-power-bi/)
- Questions? [Try asking the Power BI Community](https://community.powerbi.com/)
- Suggestions? [Contribute ideas to improve Power BI](https://ideas.powerbi.com)
