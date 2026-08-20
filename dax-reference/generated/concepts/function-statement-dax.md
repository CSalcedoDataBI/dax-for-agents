---
title: FUNCTION keyword (DAX)
topic: reference
summary: "Learn more about: FUNCTION"
source: query-languages/dax/function-statement-dax.md@323524c
sourceDate: 
---
# FUNCTION

Introduces a function definition in a DEFINE statement of a [DAX query](https://learn.microsoft.com/en-us/dax/dax-queries).

## Syntax

```dax
[DEFINE 
    (
      FUNCTION <function name> = ([<parameter name> [: [<type>] [<subtype>] [<passing mode>]] [= <default expression>], ...]) => <function body>
    ) + 
]

(EVALUATE <table expression>) +
```

### Parameters

|Term|Definition|
|---------|---------|
|`function name`| The name of a function.|
|`parameter name`| The name of the parameter. This cannot be a reserved keyword such as `measure`.|
|`type`| The parameter type. Can be one of the following: `ANYVAL`, `SCALAR`, `TABLE`, `ANYREF`, `CALENDARREF`, `COLUMNREF`, `MEASUREREF`, `TABLEREF`. `ANYVAL` is an abstract type for `SCALAR` or `TABLE`. `ANYREF` is an abstract type for all references.|
|`subtype`| The parameter subtype. Applies only to `parameter type` = `SCALAR`. Can be one of the following: `BOOLEAN`, `DATETIME`, `DECIMAL`, `DOUBLE`, `INT64`, `NUMERIC`, `STRING`, `VARIANT`.|
|`passing mode`| The parameter passing mode. Can be `VAL` (eagerly evaluated) or `EXPR` (lazily evaluated).|
|`default expression`| A DAX expression used when the argument is omitted by the caller. Makes the parameter optional.|
|`function body`| A DAX expression for the function.  |

## Return value

The calculated result of the function body.

## Remarks

- To learn more about DAX User Defined Functions, see [DAX User Defined Functions](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions).
- To learn more about how FUNCTION statements are used, see [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries).

## Related content

- [Working with DAX User Defined Functions](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions)
- [DEFINE](https://learn.microsoft.com/en-us/dax/define-statement-dax)
- [EVALUATE](https://learn.microsoft.com/en-us/dax/evaluate-statement-dax)
- [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries)
