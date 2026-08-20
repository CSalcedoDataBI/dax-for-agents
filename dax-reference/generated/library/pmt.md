---
name: PMT
category: [financial]
primaryCategory: financial
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/pmt-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# PMT

Calculates the payment for a loan based on constant payments and a constant interest rate.

## Syntax

```dax
PMT(<rate>, <nper>, <pv>[, <fv>[, <type>]])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`rate`|The interest rate for the loan.|
|`nper`|The total number of payments for the loan.|
|`pv`|The present value, or the total amount that a series of future payments is worth now; also known as the principal.|
|`fv`|(Optional) The future value, or a cash balance you want to attain after the last payment is made. If fv is omitted, it is assumed to be BLANK.|
|`type`|(Optional) The number 0 or 1 which indicates when payments are due. If type is omitted, it is assumed to be 0. The accepted values are listed below this table.|

The `type` parameter accepts the following values:

| **Set `type` equal to** | **If payments are due**        |
| --------------------- | ------------------------------ |
| 0 or omitted          | At the end of the period       |
| 1                     | At the beginning of the period |

**Note:** For a more complete description of the arguments in PMT, see the PV function.

## Return Value

The amount of a single loan payment.

## Remarks

- The payment returned by PMT includes principal and interest but no taxes, reserve payments, or fees sometimes associated with loans.

- Make sure that you are consistent about the units you use for specifying rate and nper. If you make monthly payments on a four-year loan at an annual interest rate of 12 percent, use 0.12/12 for rate and 4*12 for nper. If you make annual payments on the same loan, use 0.12 for rate and 4 for nper.

- `type` is rounded to the nearest integer.

- An error is returned if:
  - `nper < 1`

**Tip**: To find the total amount paid over the duration of the loan, multiply the returned PMT value by nper.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

### Example 1

| **Data** | **Description**              |
| -------- | ---------------------------- |
| 8%       | Annual interest rate         |
| 10       | Number of months of payments |
| \\$10,000  | Amount of loan               |

The following DAX query:

```dax
EVALUATE
{
  PMT(0.08/12, 10, 10000, 0, 1)
}
```

Returns the monthly payment amount, paid at the beginning of the month, for a loan with the terms specified above.

| **[Value]**      |
| ------------------ |
| -1030.16432717797 |

**Note:** 1030.16432717797 is the payment per period. As a result, the total amount paid over the duration of the loan is approximately 1030.16 * 10 = \\$10,301.60. In other words, approximately \\$301.60 of interest is paid.

### Example 2

| **Data** | **Description**             |
| -------- | --------------------------- |
| 6%       | Annual interest rate        |
| 18       | Number of years of payments |
| \\$50,000  | Amount of loan              |

The following DAX query:

```dax
EVALUATE
{
  PMT(0.06/12, 18*12, 0, 50000)
}
```

| **[Value]**      |
| ------------------ |
| -129.081160867991 |

Returns the amount to save each month to have \\$50,000 at the end of 18 years, using the terms specified above.
