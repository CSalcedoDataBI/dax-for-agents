---
title: EVALUATE keyword (DAX)
topic: reference
summary: "Learn more about: EVALUATE"
source: query-languages/dax/evaluate-statement-dax.md@323524c
sourceDate: 
---
# EVALUATE

Introduces a statement containing a table expression required in a [DAX query](https://learn.microsoft.com/en-us/dax/dax-queries).

## Syntax

```dax
EVALUATE <table>
```

## Parameters

|Term|Definition|
|--------|--------------|
|`table`|A table expression|

## Return value

The result of a table expression.

## Remarks

- A DAX query can contain multiple EVALUATE statements.

- To learn more about how EVALUATE statements are used, see [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries).

## Example

```dax
EVALUATE
    'Internet Sales'
```

Returns all rows and columns from the Internet Sales table, as a table.

## Related content

- [ORDER BY](https://learn.microsoft.com/en-us/dax/orderby-statement-dax)
- [START AT](https://learn.microsoft.com/en-us/dax/startat-statement-dax)
- [DEFINE](https://learn.microsoft.com/en-us/dax/define-statement-dax)
- [VAR](https://learn.microsoft.com/en-us/dax/var-dax)
- [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries)
