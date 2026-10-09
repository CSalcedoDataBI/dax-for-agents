---
title: Virtual Column (DAX) | Microsoft Docs
topic: reference
summary: "Learn more about: Virtual Column"
source: query-languages/dax/virtual-column-statement-dax.md@323524c
sourceDate: 
---
# Virtual Column

Introduces a virtual column definition in a DEFINE statement of a [DAX query](https://learn.microsoft.com/en-us/dax/dax-queries).

## Syntax

```dax
[DEFINE 
    (
      COLUMN <table name>[<column name>] = <scalar expression>
    ) + 
]

(EVALUATE <table expression>) +
```

### Parameters

Scalar expression defines the content of virtual column. The expression is evaluated row by row on the table. The virtual column is only defined in the scope of current query.

## Return value

A virtual column is defined

## Remarks

- Virtual column is computed on-demand even for import model. This behavior is different from calculated column which is processed during refresh time.

- For DirectQuery table, the scalar expression is subject to data source capability. The limitation is the same as DirectQuery calculated column.

- Please carefully evaluate performance impact when defining a virtual column on a table with huge number of rows.

- When defining virtual column over a virtual table with visual shape, this virtual column is considered a visual calculation, and subject to visual calculation limitations.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Related content

- [DEFINE](https://learn.microsoft.com/en-us/dax/define-statement-dax)  
- [EVALUATE](https://learn.microsoft.com/en-us/dax/evaluate-statement-dax)  
- [VAR](https://learn.microsoft.com/en-us/dax/var-dax)  
- [Virtual Table](https://learn.microsoft.com/en-us/dax/virtual-table-statement-dax)
- [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries)  
