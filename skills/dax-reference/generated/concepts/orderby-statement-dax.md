---
title: ORDER BY keyword (DAX)
topic: reference
summary: "Learn more about: ORDER BY"
source: query-languages/dax/orderby-statement-dax.md@323524c
sourceDate: 
---
# ORDER BY

Introduces a statement that defines sort order of query results returned by an EVALUATE statement in a [DAX query](https://learn.microsoft.com/en-us/dax/dax-queries).

## Syntax

```dax
[ORDER BY {<expression> [{ASC | DESC}]}[, …]]
```

### Parameters

|Term|Definition|
|--------|--------------|
|`expression`|Any DAX expression that returns a single scalar value.|
|`ASC`|(default) Ascending sort order.|
|`DESC`|Descending sort order.|

## Return value

The result of an EVALUATE statement in ascending (ASC) or descending (DESC) order.

## Remarks

To learn more about how ORDER BY statements are used, see [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries).

## Related content

- [START AT](https://learn.microsoft.com/en-us/dax/startat-statement-dax)
- [EVALUATE](https://learn.microsoft.com/en-us/dax/evaluate-statement-dax)
- [VAR](https://learn.microsoft.com/en-us/dax/var-dax)
- [DEFINE](https://learn.microsoft.com/en-us/dax/define-statement-dax)
- [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries)
