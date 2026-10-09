---
title: DEFINE keyword (DAX)
topic: reference
summary: "Learn more about: DEFINE"
source: query-languages/dax/define-statement-dax.md@323524c
sourceDate: 
---
# DEFINE

Introduces a statement with one or more entity definitions that can be applied to one or more EVALUATE statements of a [DAX query](https://learn.microsoft.com/en-us/dax/dax-queries).

## Syntax

```dax
[DEFINE 
    (
     (COLUMN <table name>[<column name>] = <scalar expression>) |
     (FUNCTION <function name> = ([parameter name]: [parameter type], ...) => <function body>) |
     (MEASURE <table name>[<measure name>] = <scalar expression>) | 
     (TABLE <table name> = <virtual table definition>) | 
     (VAR <var name> = <table or scalar expression>) |
    ) + 
]

(EVALUATE <table expression>) +
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Entity`|COLUMN<sup>[1](#not-rec)</sup>, FUNCTION, MEASURE, TABLE<sup>[1](#not-rec)</sup>, or VAR.|
|`name`|The name of a column, function, measure, table, or var definition. It cannot be an expression. The name does not have to be unique. The name exists only for the duration of the query.|
|`expression`|Any DAX expression that returns a table or scalar value. The expression can use any of the defined entities. If there is a need to convert a scalar expression into a table expression, wrap the expression inside a table constructor with curly braces `{}`, or use the `ROW()` function to return a single row table.|
|`parameter type`, `parameter name`, `function body`|See [FUNCTION statement](https://learn.microsoft.com/en-us/dax/function-statement-dax).|

<a name="not-rec">[1]</a> **Caution:** Query scoped TABLE and COLUMN definitions are meant for internal use only. While you can define TABLE and COLUMN expressions for a query without syntax error, they may produce runtime errors and are not recommended.

## Remarks

- A DAX query can have multiple EVALUATE statements, but can have only one DEFINE statement. Definitions in the DEFINE statement can apply to any EVALUATE statements in the query.

- At least one definition is required in a DEFINE statement.

- Measure definitions for a query override model measures of the same name.

- VAR names have unique restrictions. To learn more, see [VAR - Parameters](https://learn.microsoft.com/en-us/dax/var-dax#parameters).

- To learn more about how a DEFINE statement is used, see [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries).

- To learn more about virtual column, see [Virtual Column](https://learn.microsoft.com/en-us/dax/virtual-column-statement-dax)

- To learn more about virtual table, see [Virtual Table](https://learn.microsoft.com/en-us/dax/virtual-table-statement-dax)

- To learn more about DAX user defined functions, see [DAX User Defined Functions](https://learn.microsoft.com/en-us/dax/function-statement-dax)

## Related content

- [EVALUATE](https://learn.microsoft.com/en-us/dax/evaluate-statement-dax)  
- [FUNCTION](https://learn.microsoft.com/en-us/dax/function-statement-dax)
- [VAR](https://learn.microsoft.com/en-us/dax/var-dax)  
- [MEASURE](https://learn.microsoft.com/en-us/dax/measure-statement-dax)  
- [Virtual Column](https://learn.microsoft.com/en-us/dax/virtual-column-statement-dax)
- [Virtual Table](https://learn.microsoft.com/en-us/dax/virtual-table-statement-dax)
- [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries)
