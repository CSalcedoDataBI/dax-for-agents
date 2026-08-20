---
title: START AT keyword (DAX)
topic: reference
summary: "Learn more about: START AT"
source: query-languages/dax/startat-statement-dax.md@323524c
sourceDate: 
---
# START AT

Introduces a statement that defines the starting value at which the query results of an ORDER BY clause in an EVALUATE statement in a [DAX query](https://learn.microsoft.com/en-us/dax/dax-queries) are returned.

## Syntax

```dax
[START AT {<value>|<parameter>} [, …]]
```

## Parameters

|Term  |Definition  |
|---------|---------|
|  `value`     |   A constant value. Cannot be an expression.  |
|  `parameter`     |   The name of a parameter in an XMLA statement prefixed with an `@` character.  |

## Remarks

- START AT arguments have a one-to-one correspondence with the columns in the ORDER BY statement. There can be as many arguments in the START AT statement as there are in the ORDER BY statement, but not more. The first argument in the START AT statement defines the starting value in column 1 of the ORDER BY columns. The second argument in the START AT statement defines the starting value in column 2 of the ORDER BY columns within the rows that meet the first value for column 1.

- To learn more about how START AT statements are used, see [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries).

## Related content

- [ORDER BY](https://learn.microsoft.com/en-us/dax/orderby-statement-dax)
- [EVALUATE](https://learn.microsoft.com/en-us/dax/evaluate-statement-dax)
- [VAR](https://learn.microsoft.com/en-us/dax/var-dax)
- [DEFINE](https://learn.microsoft.com/en-us/dax/define-statement-dax)
- [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries)
