# DAX Reference — catálogo de funciones (índice generado)

> Fuente: `MicrosoftDocs/query-docs@323524c` · commit 2026-08-13T16:02:28Z
> 479 funciones · generado por `scripts/sync_query_docs.py`
> **No editar a mano.** ⛔ = Microsoft la desaconseja **en cálculos visuales** (dice que probablemente devuelve resultados sin sentido); en una medida o columna calculada no dice nada · ★ = tiene nota propia · ▶ = tiene ejemplos ejecutables en este repositorio.
> Ret `modifier` = ni escalar ni tabla: solo sirve como argumento de filtro de `CALCULATE`/`CALCULATETABLE` y no devuelve nada utilizable (Microsoft: *can only be used to clear filters but not to return a table*).

| Función | Cat | Ret | Aplica | Resumen | ⚑ | Ficha |
|---|---|---|---|---|---|---|
| ABS | math-and-trig | scalar | M C T V | Returns the absolute value of a number. | ▶ | `functions-math-and-trig:5-67` |
| ACCRINT | financial | scalar | M C T V | Returns the accrued interest for a security that pays periodic interest. |  | `functions-financial:5-134` |
| ACCRINTM | financial | scalar | M C T V | Returns the accrued interest for a security that pays interest at maturity. |  | `functions-financial:136-239` |
| ACOS | math-and-trig | scalar | M C T V | Returns the arccosine, or inverse cosine, of a number. | ▶ | `functions-math-and-trig:69-125` |
| ACOSH | math-and-trig | scalar | M C T V | Returns the inverse hyperbolic cosine of a number. | ▶ | `functions-math-and-trig:127-184` |
| ACOT | math-and-trig | scalar | M C T V | Returns the arccotangent, or inverse cotangent, of a number. | ▶ | `functions-math-and-trig:186-226` |
| ACOTH | math-and-trig | scalar | M C T V | Returns the inverse hyperbolic cotangent of a number. | ▶ | `functions-math-and-trig:228-272` |
| ADDCOLUMNS | table-manipulation | table | M C T V | Adds calculated columns to the given table or table expression. |  | `functions-table-manipulation:5-68` |
| ADDMISSINGITEMS | table-manipulation | table | M C T | Adds combinations of items from multiple columns to a table if they do not already exist. |  | `functions-table-manipulation:70-159` |
| ALL | filter | table | M C T V | Returns all the rows in a table, or all the values in a column, ignoring any filters that might have been applied. | ★ | `functions-filter:5-152` |
| ALLCROSSFILTERED | filter | modifier | M C T V | Clear all filters which are applied to a table. |  | `functions-filter:154-233` |
| ALLEXCEPT | filter | table | M C T | Removes all context filters in the table except filters that have been applied to the specified columns. | ★ | `functions-filter:235-306` |
| ALLNOBLANKROW | filter | table | M C T V | From the parent table of a relationship, returns all rows but the blank row, or all distinct values of a column but the blank row, and disregards any context filters that might exist. |  | `functions-filter:308-447` |
| ALLSELECTED | filter | table | M C T V | Removes context filters from columns and rows in the current query, while retaining all other context filters or explicit filters. | ★ | `functions-filter:449-585` |
| ALLSELECTEDAPPLY |  | table | M C T | Modifies how filters are applied while evaluating a GROUPCROSSAPPLY or GROUPCROSSAPPLYTABLE function. |  | `functions-uncategorized:5-50` |
| ALLSELECTEDREMOVE |  | table | M C T | Modifies how filters are applied while evaluating a GROUPCROSSAPPLY or GROUPCROSSAPPLYTABLE function. |  | `functions-uncategorized:52-100` |
| ALWAYSAPPLY |  | table | M C T | Modifies how filters are applied while evaluating a GROUPCROSSAPPLY or GROUPCROSSAPPLYTABLE function. |  | `functions-uncategorized:102-147` |
| AMORDEGRC | financial | scalar | M C T V | Returns the depreciation for each accounting period. Similar to AMORLINC, except a depreciation coefficient is applied depending on the life of the assets. |  | `functions-financial:241-351` |
| AMORLINC | financial | scalar | M C T V | Returns the depreciation for each accounting period. |  | `functions-financial:353-450` |
| AND | logical | scalar | M C T V | Checks whether both arguments are `TRUE`, and returns `TRUE` if both arguments are `TRUE`. | ▶ | `functions-logical:5-122` |
| APPROXIMATEDISTINCTCOUNT | aggregation | scalar | M C T | Returns an *estimated* count of unique values in a column. |  | `functions-aggregation:5-42` |
| ASIN | math-and-trig | scalar | M C T V | Returns the arcsine, or inverse sine, of a number. | ▶ | `functions-math-and-trig:274-331` |
| ASINH | math-and-trig | scalar | M C T V | Returns the inverse hyperbolic sine of a number. | ▶ | `functions-math-and-trig:333-389` |
| ATAN | math-and-trig | scalar | M C T V | Returns the arctangent, or inverse tangent, of a number. | ▶ | `functions-math-and-trig:391-447` |
| ATANH | math-and-trig | scalar | M C T V | Returns the inverse hyperbolic tangent of a number. | ▶ | `functions-math-and-trig:449-509` |
| AVERAGE | aggregation | scalar | M C T V | Returns the average (arithmetic mean) of all the numbers in a column. |  | `functions-aggregation:44-111` |
| AVERAGEA | aggregation | scalar | M C T V | Returns the average (arithmetic mean) of the values in a column. |  | `functions-aggregation:113-188` |
| AVERAGEX | aggregation | scalar | M C T V | Calculates the average (arithmetic mean) of a set of expressions evaluated over a table. | ★ | `functions-aggregation:190-255` |
| BETA.DIST | statistical | scalar | M C T V | Returns the beta distribution. |  | `functions-statistical:5-56` |
| BETA.INV | statistical | scalar | M C T V | Returns the inverse of the beta cumulative probability density function (BETA.DIST). |  | `functions-statistical:58-111` |
| BITAND | logical | scalar | M C T V | Returns a bitwise 'AND' of two numbers. | ▶ | `functions-logical:124-190` |
| BITLSHIFT | logical | scalar | M C T V | Returns a number shifted left by the specified number of bits. | ▶ | `functions-logical:192-294` |
| BITOR | logical | scalar | M C T V | Returns a bitwise 'OR' of two numbers. | ▶ | `functions-logical:296-363` |
| BITRSHIFT | logical | scalar | M C T V | Returns a number shifted right by the specified number of bits. | ▶ | `functions-logical:365-467` |
| BITXOR | logical | scalar | M C T V | Returns a bitwise 'XOR' of two numbers. | ▶ | `functions-logical:469-535` |
| BLANK | other | scalar | M C T V | Returns a blank. | ★ | `functions-other:5-74` |
| CALCULATE | filter | scalar | M C T V | Evaluates an expression in a modified filter context. | ★ | `functions-filter:587-757` |
| CALCULATETABLE | filter | table | M C T V | Evaluates a table expression in a modified filter context. |  | `functions-filter:759-884` |
| CALENDAR | date-and-time | table | M C T V | Returns a table with a single column named "Date" that contains a contiguous set of dates. |  | `functions-date-and-time:5-64` |
| CALENDARAUTO | date-and-time | table | M C T V | Returns a table with a single column named "Date" that contains a contiguous set of dates. | ⛔ | `functions-date-and-time:66-134` |
| CEILING | math-and-trig | scalar | M C T V | Rounds a number up, to the nearest integer or to the nearest multiple of significance. | ▶ | `functions-math-and-trig:511-590` |
| CHISQ.DIST | statistical | scalar | M C T V | Returns the chi-squared distribution. |  | `functions-statistical:113-181` |
| CHISQ.DIST.RT | statistical | scalar | M C T V | Returns the right-tailed probability of the chi-squared distribution. |  | `functions-statistical:183-250` |
| CHISQ.INV | statistical | scalar | M C T V | Returns the inverse of the left-tailed probability of the chi-squared distribution. |  | `functions-statistical:252-312` |
| CHISQ.INV.RT | statistical | scalar | M C T V | Returns the inverse of the right-tailed probability of the chi-squared distribution. |  | `functions-statistical:314-364` |
| CLOSINGBALANCEMONTH | time-intelligence | scalar | M C T V | Evaluates the expression at the last date of the month in the current context. | ⛔ | `functions-time-intelligence:5-98` |
| CLOSINGBALANCEQUARTER | time-intelligence | scalar | M C T V | Evaluates the expression at the last date of the quarter in the current context. | ⛔ | `functions-time-intelligence:100-193` |
| CLOSINGBALANCEWEEK | time-intelligence | scalar | M C T V | Evaluates the expression at the last date of the week in the current context. | ⛔ | `functions-time-intelligence:195-259` |
| CLOSINGBALANCEYEAR | time-intelligence | scalar | M C T V | Evaluates the expression at the last date of the year in the current context. | ⛔ | `functions-time-intelligence:261-359` |
| COALESCE | logical | scalar | M C T V | Returns the first expression that does not evaluate to BLANK. | ▶ | `functions-logical:537-602` |
| COLLAPSE |  | scalar | V | Retrieves a context at a higher level compared to the current context. If an expression is provided, returns its value in the new context, allowing for navigation in hierarchies and calculation at a higher level. |  | `functions-uncategorized:149-230` |
| COLLAPSEALL |  | scalar | V | Retrieves a context at the highest level compared to the current context. If an expression is provided, returns its value in the new context, allowing for navigation in hierarchies and calculation at the highest level. |  | `functions-uncategorized:232-303` |
| COLUMNSTATISTICS | information | table | M C T V | Returns a table of statistics regarding every column in every table in the model. | ⛔ | `functions-information:5-94` |
| COMBIN | statistical | scalar | M C T V | Returns the number of combinations for a given number of items. |  | `functions-statistical:366-431` |
| COMBINA | statistical | scalar | M C T V | Returns the number of combinations (with repetitions) for a given number of items. |  | `functions-statistical:433-491` |
| COMBINEVALUES | text | scalar | M C T V | Joins two or more text strings into one text string. | ▶ | `functions-text:5-122` |
| CONCATENATE | text | scalar | M C T V | Joins two text strings into one text string. | ▶ | `functions-text:124-224` |
| CONCATENATEX | text | scalar | M C T V | Concatenates the result of an expression evaluated for each row in a table. | ★▶ | `functions-text:226-308` |
| CONFIDENCE.NORM | statistical | scalar | M C T V | The confidence interval is a range of values. |  | `functions-statistical:493-546` |
| CONFIDENCE.T | statistical | scalar | M C T V | Returns the confidence interval for a population mean, using a Student's t distribution. |  | `functions-statistical:548-608` |
| CONTAINS | information | scalar | M C T | Returns true if values for all referred columns exist, or are contained, in those columns; otherwise, the function returns false. | ▶ | `functions-information:96-161` |
| CONTAINSROW | information | scalar | M C T V | Returns `TRUE` if a row of values exists or contained in a table, otherwise returns `FALSE`. | ▶ | `functions-information:163-294` |
| CONTAINSSTRING | information | scalar | M C T V | Returns `TRUE` or `FALSE` indicating whether one string contains another string. | ▶ | `functions-information:296-368` |
| CONTAINSSTRINGEXACT | information | scalar | M C T V | Returns `TRUE` or `FALSE` indicating whether one string contains another string. | ▶ | `functions-information:370-441` |
| CONVERT | math-and-trig | scalar | M C T V | Converts an expression of one data type to another. | ▶ | `functions-math-and-trig:592-671` |
| COS | math-and-trig | scalar | M C T V | Returns the cosine of the given angle. | ▶ | `functions-math-and-trig:673-730` |
| COSH | math-and-trig | scalar | M C T V | Returns the hyperbolic cosine of a number. | ▶ | `functions-math-and-trig:732-792` |
| COT | math-and-trig | scalar | M C T V | Returns the cotangent of an angle specified in radians. | ▶ | `functions-math-and-trig:794-861` |
| COTH | math-and-trig | scalar | M C T V | Returns the hyperbolic cotangent of a hyperbolic angle. | ▶ | `functions-math-and-trig:863-938` |
| COUNT | aggregation | scalar | M C T V | Counts the number of rows in the specified column that contain non-blank values. Does not support Boolean values. | ★ | `functions-aggregation:257-330` |
| COUNTA | aggregation | scalar | M C T V | Counts the number of rows in the specified column that contain non-blank values. Supports Boolean values. |  | `functions-aggregation:332-392` |
| COUNTAX | aggregation | scalar | M C T V | Counts non-blank results when evaluating the result of an expression over a table. |  | `functions-aggregation:394-456` |
| COUNTBLANK | aggregation | scalar | M C T V | Counts the number of blank cells in a column. |  | `functions-aggregation:458-524` |
| COUNTROWS | aggregation | scalar | M C T V | Counts the number of rows in the specified table, or in a table defined by an expression. | ★ | `functions-aggregation:526-603` |
| COUNTX | aggregation | scalar | M C T V | Counts the number of rows that contain a number or an expression that evaluates to a number, when evaluating an expression over a table. |  | `functions-aggregation:605-672` |
| COUPDAYBS | financial | scalar | M C T V | Returns the number of days from the beginning of a coupon period until its settlement date. |  | `functions-financial:452-545` |
| COUPDAYS | financial | scalar | M C T V | Returns the number of days in the coupon period that contains the settlement date. |  | `functions-financial:547-640` |
| COUPDAYSNC | financial | scalar | M C T V | Returns the number of days from the settlement date to the next coupon date. |  | `functions-financial:642-735` |
| COUPNCD | financial | scalar | M C T V | Returns the next coupon date after the settlement date. |  | `functions-financial:737-830` |
| COUPNUM | financial | scalar | M C T V | Returns the number of coupons payable between the settlement date and maturity date, rounded up to the nearest whole coupon. |  | `functions-financial:832-925` |
| COUPPCD | financial | scalar | M C T V | Returns the previous coupon date before the settlement date. |  | `functions-financial:927-1020` |
| CROSSFILTER | relationship | scalar | M C T | Specifies the cross-filtering direction to be used in a calculation for a relationship that exists between two columns. |  | `functions-relationship:5-88` |
| CROSSJOIN | table-manipulation | table | M C T V | Returns a table that contains the Cartesian product of all rows from all tables in the arguments. |  | `functions-table-manipulation:161-243` |
| CUMIPMT | financial | scalar | M C T V | Returns the cumulative interest paid on a loan between start_period and end_period. |  | `functions-financial:1022-1130` |
| CUMPRINC | financial | scalar | M C T V | Returns the cumulative principal paid on a loan between start_period and end_period. |  | `functions-financial:1132-1240` |
| CURRENCY | math-and-trig | scalar | M C T V | Evaluates the argument and returns the result as currency data type. | ▶ | `functions-math-and-trig:940-1005` |
| CURRENTGROUP | table-manipulation | table | M C T V | Returns a set of rows from the table argument of a GROUPBY expression. | ⛔ | `functions-table-manipulation:245-291` |
| CUSTOMDATA | information | scalar | M C T V | Returns the content of the CustomData property in the connection string. |  | `functions-information:443-489` |
| DATATABLE | table-manipulation | table | M C T V | Provides a mechanism for declaring an inline set of data values. |  | `functions-table-manipulation:293-354` |
| DATE | date-and-time | scalar | M C T V | Returns the specified date in datetime format. |  | `functions-date-and-time:136-245` |
| DATEADD | time-intelligence | table | M C T V | Returns a table that contains a column of dates, shifted either forward or backward in time by the specified number of intervals from the dates in the current context. | ⛔★ | `functions-time-intelligence:361-498` |
| DATEDIFF | date-and-time | scalar | M C T V | Returns the number of interval boundaries between two dates. |  | `functions-date-and-time:247-323` |
| DATESBETWEEN | time-intelligence | table | M C T V | Returns a table that contains a column of dates that begins with a specified start date and continues until a specified end date. | ⛔ | `functions-time-intelligence:500-603` |
| DATESINPERIOD | time-intelligence | table | M C T V | Returns a table that contains a column of dates that begins with a specified start date and continues for the specified number and type of date intervals. | ⛔ | `functions-time-intelligence:605-741` |
| DATESMTD | time-intelligence | table | M C T V | Returns a table that contains a column of the dates for the month to date, in the current context. | ⛔ | `functions-time-intelligence:743-829` |
| DATESQTD | time-intelligence | table | M C T V | Returns a table that contains a column of the dates for the quarter to date, in the current context. | ⛔ | `functions-time-intelligence:831-916` |
| DATESWTD | time-intelligence | table | M C T V | Returns a table that contains a column of the dates for the week to date, in the current context. | ⛔ | `functions-time-intelligence:918-978` |
| DATESYTD | time-intelligence | table | M C T V | Returns a table that contains a column of the dates for the year to date, in the current context. | ⛔★ | `functions-time-intelligence:980-1082` |
| DATEVALUE | date-and-time | scalar | M C T V | Converts a date in the form of text to a date in datetime format. |  | `functions-date-and-time:325-391` |
| DAY | date-and-time | scalar | M C T V | Returns the day of the month, a number from 1 to 31. |  | `functions-date-and-time:393-465` |
| DB | financial | scalar | M C T V | Returns the depreciation of an asset for a specified period using the fixed-declining balance method. |  | `functions-financial:1242-1355` |
| DDB | financial | scalar | M C T V | Returns the depreciation of an asset for a specified period using the double-declining balance method or some other method you specify. |  | `functions-financial:1357-1461` |
| DEGREES | math-and-trig | scalar | M C T V | Converts radians into degrees. | ▶ | `functions-math-and-trig:1007-1054` |
| DEPENDON |  | scalar | M C T | Change the table expression to be dependent on outer columns, based on the table data. |  | `functions-uncategorized:305-362` |
| DETAILROWS | table-manipulation | table | M C T | Evaluates a Detail Rows Expression defined for a measure and returns the data. |  | `functions-table-manipulation:356-389` |
| DISC | financial | scalar | M C T V | Returns the discount rate for a security. |  | `functions-financial:1463-1569` |
| DISTINCT | table-manipulation | table | M C T V | Returns a one-column table that contains the distinct values from the specified column. |  | `functions-table-manipulation:391-471` |
| DISTINCT | table-manipulation | table | M C T V | Returns a table by removing duplicate rows from another table or expression. |  | `functions-table-manipulation:473-538` |
| DISTINCTCOUNT | aggregation | scalar | M C T V | Counts the number of distinct values in a column. |  | `functions-aggregation:674-763` |
| DISTINCTCOUNTNOBLANK | aggregation | scalar | M C T V | Counts the number of distinct values in a column. |  | `functions-aggregation:765-835` |
| DIVIDE | math-and-trig | scalar | M C T V | Performs division and returns alternate result or BLANK() on division by 0. | ★▶ | `functions-math-and-trig:1056-1138` |
| DOLLARDE | financial | scalar | M C T V | Converts a dollar price expressed as an integer part and a fraction part, such as 1.02, into a dollar price expressed as a decimal number. |  | `functions-financial:1571-1634` |
| DOLLARFR | financial | scalar | M C T V | Converts a dollar price expressed as an integer part and a fraction part, such as 1.02, into a dollar price expressed as a decimal number. |  | `functions-financial:1636-1697` |
| DURATION | financial | scalar | M C T V | Returns the Macauley duration for an assumed par value of $100. |  | `functions-financial:1699-1798` |
| EARLIER | filter | scalar | M C T | Returns the current value of the specified column in an outer evaluation pass of the mentioned column. | ★ | `functions-filter:886-1021` |
| EARLIEST | filter | table | M C T | Returns the current value of the specified column in an outer evaluation pass of the specified column. |  | `functions-filter:1023-1080` |
| EDATE | date-and-time | scalar | M C T V | Returns the date that is the indicated number of months before or after the start date. |  | `functions-date-and-time:467-533` |
| EFFECT | financial | scalar | M C T V | Returns the effective annual interest rate, given the nominal annual interest rate and the number of compounding periods per year. |  | `functions-financial:1800-1875` |
| ENDOFMONTH | time-intelligence | table | M C T V | Returns the last date of the month in the current context for the specified column of dates. | ⛔ | `functions-time-intelligence:1084-1160` |
| ENDOFQUARTER | time-intelligence | table | M C T V | Returns the last date of the quarter in the current context for the specified column of dates. | ⛔ | `functions-time-intelligence:1162-1237` |
| ENDOFWEEK | time-intelligence | table | M C T V | Returns the last date of the week in the current context for the specified column of dates. | ⛔ | `functions-time-intelligence:1239-1298` |
| ENDOFYEAR | time-intelligence | table | M C T V | Returns the last date of the year in the current context for the specified column of dates. | ⛔ | `functions-time-intelligence:1300-1380` |
| EOMONTH | date-and-time | scalar | M C T V | Returns the date in datetime format of the last day of the month, before or after a specified number of months. |  | `functions-date-and-time:535-601` |
| ERROR | other | scalar | M C T V | Raises an error with an error message. |  | `functions-other:76-166` |
| EVALUATEANDLOG | other | scalar | M C T V | Returns the value of the first argument and logs it in a DAX Evaluation Log profiler event. |  | `functions-other:168-322` |
| EVEN | math-and-trig | scalar | M C T V | Returns number rounded up to the nearest even integer. | ▶ | `functions-math-and-trig:1140-1202` |
| EXACT | text | scalar | M C T V | Compares two text strings and returns ``TRUE`` if they are exactly the same, `FALSE` otherwise. | ▶ | `functions-text:310-371` |
| EXCEPT | table-manipulation | table | M C T V | Returns the rows of one table which do not appear in another table. |  | `functions-table-manipulation:540-637` |
| EXP | math-and-trig | scalar | M C T V | Returns e raised to the power of a given number. | ▶ | `functions-math-and-trig:1204-1273` |
| EXPAND |  | scalar | V | Retrieves a context with added levels of detail compared to the current context. If an expression is provided, returns its value in the new context, allowing for navigation in hierarchies and calculation at a more detailed level. |  | `functions-uncategorized:364-446` |
| EXPANDALL |  | scalar | V | Retrieves a context at the most detailed level. If an expression is provided, returns its value in the new context, allowing for navigation in hierarchies and calculation at the most detailed level. |  | `functions-uncategorized:448-520` |
| EXPON.DIST | statistical | scalar | M C T V | Returns the exponential distribution. |  | `functions-statistical:610-665` |
| EXTERNALMEASURE | other | scalar | M C T | Invokes a measure defined in a remote model and returns its result. |  | `functions-other:324-385` |
| FACT | math-and-trig | scalar | M C T V | Returns the factorial of a number, equal to the series 1*2\*3\*...\* , ending in the given number. | ▶ | `functions-math-and-trig:1275-1351` |
| FALSE | logical | scalar | M C T V | Returns the logical value `FALSE`. | ▶ | `functions-logical:604-672` |
| FILTER | filter | table | M C T V | Returns a table that represents a subset of another table or expression. | ★ | `functions-filter:1082-1182` |
| FILTERCLUSTER |  | table | M C T | Returns a correlated join table over a set of groups. |  | `functions-uncategorized:522-570` |
| FILTERS | table-manipulation | table | M C T V | Returns a table of values directly applied as filters to `columnName`. |  | `functions-table-manipulation:639-691` |
| FIND | text | scalar | M C T V | Returns the starting position of one text string within another text string. | ★▶ | `functions-text:373-471` |
| FIRST | filter | scalar | V | Used in visual calculations only. Retrieves a value in the visual matrix from the first row of an axis. |  | `functions-filter:1184-1250` |
| FIRSTDATE | time-intelligence | table | M C T V | Returns the first date in the current context for the specified column of dates. | ⛔ | `functions-time-intelligence:1382-1462` |
| FIRSTNONBLANK | filter | table | M C T V | Returns the first value in the column, `<column>`, filtered by the current context, where the expression is not blank. | ⛔ | `functions-filter:1252-1305` |
| FIRSTNONBLANKVALUE | filter | scalar | M C T V | Evaluates an expression filtered by the sorted values of a column and returns the first value of the expression that is not blank. | ⛔ | `functions-filter:1307-1381` |
| FIXED | text | scalar | M C T V | Rounds a number to the specified number of decimals and returns the result as text. | ▶ | `functions-text:473-553` |
| FLOOR | math-and-trig | scalar | M C T V | Rounds a number down, toward zero, to the nearest multiple of significance. | ▶ | `functions-math-and-trig:1353-1429` |
| FORMAT | text | scalar | M C T V | Converts a value to text according to the specified format. | ★▶ | `functions-text:555-813` |
| FV | financial | scalar | M C T V | Calculates the future value of an investment based on a constant interest rate. |  | `functions-financial:1877-1966` |
| GCD | math-and-trig | scalar | M C T V | Returns the greatest common divisor of two or more integers. | ▶ | `functions-math-and-trig:1431-1498` |
| GENERATE | table-manipulation | table | M C T V | Returns a table with the Cartesian product between each row in *table1* and the table that results from evaluating *table2* in the context of the current row from *table1*. |  | `functions-table-manipulation:693-791` |
| GENERATEALL | table-manipulation | table | M C T V | Returns a table with the Cartesian product between each row in *table1* and the table that results from evaluating *table2* in the context of the current row from *table1*. |  | `functions-table-manipulation:793-895` |
| GENERATESERIES | table-manipulation | table | M C T V | Returns a single column table containing the values of an arithmetic series. |  | `functions-table-manipulation:897-995` |
| GEOMEAN | statistical | scalar | M C T V | Returns the geometric mean of the numbers in a column. |  | `functions-statistical:667-727` |
| GEOMEANX | statistical | scalar | M C T V | Returns the geometric mean of an expression evaluated for each row in a table. |  | `functions-statistical:729-790` |
| GROUPBY | table-manipulation | table | M C T V | Similar to the SUMMARIZE function, GROUPBY does not do an implicit CALCULATE for any extension columns that it adds. | ⛔ | `functions-table-manipulation:997-1087` |
| GROUPCROSSAPPLY |  | table | M C T | Returns a summary table over a set of groups. |  | `functions-uncategorized:572-637` |
| GROUPCROSSAPPLYTABLE |  | table | M C T | Returns a summary table over a set of groups. |  | `functions-uncategorized:639-706` |
| HASONEFILTER | information | scalar | M C T V | Returns TRUE when the number of directly filtered values on `columnName` is one; otherwise returns `FALSE`. |  | `functions-information:491-543` |
| HASONEVALUE | information | scalar | M C T V | Returns `TRUE` when the context for `columnName` has been filtered down to one distinct value only. Otherwise is `FALSE`. |  | `functions-information:545-597` |
| HOUR | date-and-time | scalar | M C T V | Returns the hour as a number from 0 (12:00 A.M.) to 23 (11:00 P.M.). |  | `functions-date-and-time:603-665` |
| IF | logical | scalar | M C T V | Checks a condition, and returns one value when `TRUE`, otherwise it returns a second value. | ▶ | `functions-logical:674-769` |
| IF.EAGER | logical | scalar | M C T V | Checks a condition, and returns one value when `TRUE`, otherwise it returns a second value. Uses an *eager* execution plan which always executes the branch expressions regardless of the condition expression. | ▶ | `functions-logical:771-845` |
| IFERROR | logical | scalar | M C T V | Evaluates an expression and returns a specified value if the expression returns an error | ▶ | `functions-logical:847-921` |
| IGNORE | table-manipulation | scalar | M C T | Modifies SUMMARIZECOLUMNS by omitting specific expressions from the BLANK/NULL evaluation. |  | `functions-table-manipulation:1089-1141` |
| INDEX | filter | table | M C T V | Returns a row at an absolute position, specified by the position parameter, within the specified partition, sorted by the specified order or on the specified axis. |  | `functions-filter:1383-1545` |
| INFO.ALTERNATEOFDEFINITIONS | info | table | Q | Returns a table with information about each alternate of definition in the semantic model. This function provides metadata about alternate definitions for model objects. |  | `functions-info-1:5-133` |
| INFO.ANNOTATIONS | info | table | Q | Returns a table with information about each annotation in the semantic model. This information helps you understand the model. |  | `functions-info-1:135-413` |
| INFO.ATTRIBUTEHIERARCHIES | info | table | Q | Returns a table with information about each attribute hierarchy in the semantic model. This function provides metadata about the attribute hierarchies defined in the model. |  | `functions-info-1:415-489` |
| INFO.ATTRIBUTEHIERARCHYSTORAGES | info | table | Q | Returns a table with information about each attribute hierarchy storage in the semantic model. This function provides metadata about the storage characteristics of attribute hierarchies. |  | `functions-info-1:491-570` |
| INFO.CALCDEPENDENCY | info | table | Q | Returns a table with information about each calculation dependency in the semantic model. This information helps you understand the model. |  | `functions-info-1:572-675` |
| INFO.CALCULATIONGROUPS | info | table | Q | Returns a table with information about each calculation group in the semantic model. This function provides metadata about calculation groups and their properties. |  | `functions-info-1:677-784` |
| INFO.CALCULATIONITEMS | info | table | Q | Returns a table with information about each calculation item in the semantic model. This function provides metadata about calculation items within calculation groups. |  | `functions-info-1:786-899` |
| INFO.CALENDARCOLUMNGROUPS | info | table | Q | Returns a table with information about each calendar column group in the semantic model. Calendar column groups associate columns with categories within a calendar. |  | `functions-info-1:901-1039` |
| INFO.CALENDARCOLUMNREFERENCES | info | table | Q | Returns a table with information about each calendar column reference in the semantic model. Calendar column references associate columns to calendar column groups. |  | `functions-info-1:1041-1180` |
| INFO.CALENDARS | info | table | Q | Returns a table with information about each calendar in the semantic model. This function provides metadata about calendars defined on tables. |  | `functions-info-1:1182-1296` |
| INFO.CATALOGS | info | table | Q | Returns a table with information about each catalog in the semantic model. This function provides metadata about the catalogs available in the current context. |  | `functions-info-1:1298-1383` |
| INFO.CHANGEDPROPERTIES | info | table | Q | Returns a table with information about each changed property in the semantic model. This function provides metadata about properties that have been modified in the model. |  | `functions-info-1:1385-1499` |
| INFO.COLUMNPARTITIONSTORAGES | info | table | Q | Returns a table with information about each column partition storage in the semantic model. This function provides metadata about how column partitions are stored. |  | `functions-info-1:1501-1639` |
| INFO.COLUMNPERMISSIONS | info | table | Q | Returns a table with information about each column permission in the semantic model. This function provides metadata about column-level security settings. |  | `functions-info-1:1641-1790` |
| INFO.COLUMNS | info | table | Q | Returns a table with information about each column in the semantic model. This function provides metadata about all columns including their properties and characteristics. |  | `functions-info-1:1792-1935` |
| INFO.COLUMNSTORAGES | info | table | Q | Returns a table with information about each column storage in the semantic model. This function provides metadata about how columns are stored and their storage characteristics. |  | `functions-info-1:1937-2077` |
| INFO.CSDLMETADATA | info | table | Q | Returns a table with information about the CSDL metadata in the semantic model. This function provides metadata about the Conceptual Schema Definition Language representation of the model. |  | `functions-info-1:2079-2149` |
| INFO.CULTURES | info | table | Q | Returns a table with information about each culture in the semantic model. This function provides metadata about the cultures and locales supported by the model. |  | `functions-info-1:2151-2259` |
| INFO.DATACOVERAGEDEFINITIONS | info | table | Q | Returns a table with information about each data coverage definition in the semantic model. This function provides metadata about data coverage settings and definitions. |  | `functions-info-1:2261-2337` |
| INFO.DATASOURCES | info | table | Q | Returns a table with information about each data source in the semantic model. This function provides metadata about the data sources connected to the model. |  | `functions-info-1:2339-2459` |
| INFO.DELTATABLEMETADATASTORAGES | info | table | Q | Returns a table with information about each delta table metadata storage in the semantic model. This function provides metadata about delta table storage characteristics. |  | `functions-info-1:2461-2577` |
| INFO.DEPENDENCIES | info | table | Q | Returns a table with information about each dependency in the semantic model. This function provides metadata about object dependencies and relationships between model objects. |  | `functions-info-1:2579-2706` |
| INFO.DETAILROWSDEFINITIONS | info | table | Q | Returns a table with information about each detail rows definition in the semantic model. This function provides metadata about detail rows definitions for measures. |  | `functions-info-1:2708-2783` |
| INFO.DICTIONARYSTORAGES | info | table | Q | Returns a table with information about each dictionary storage in the semantic model. This function provides metadata about dictionary storage characteristics and compression. |  | `functions-info-1:2785-2931` |
| INFO.EXCLUDEDARTIFACTS | info | table | Q | Returns a table with information about each excluded artifact in the semantic model. This function provides metadata about artifacts that are excluded from the model. |  | `functions-info-1:2933-3011` |
| INFO.EXPRESSIONS | info | table | Q | Returns a table with information about each expression in the semantic model. This function provides metadata about expressions defined in the model. |  | `functions-info-1:3013-3095` |
| INFO.EXTENDEDPROPERTIES | info | table | Q | Returns a table with information about each extended property in the semantic model. This function provides metadata about extended properties defined for model objects. |  | `functions-info-1:3097-3173` |
| INFO.FORMATSTRINGDEFINITIONS | info | table | Q | Returns a table with information about each format string definition in the semantic model. This function provides metadata about format string definitions for measures and columns. |  | `functions-info-1:3175-3251` |
| INFO.FUNCTIONS | info | table | Q | Returns information about the functions currently available for use in DAX. This corresponds to the MDSCHEMA_FUNCTIONS schema rowset, but returns only DAX (and not MDX) functions by default. |  | `functions-info-1:3253-3356` |
| INFO.GENERALSEGMENTMAPSEGMENTMETADATASTORAGES | info | table | Q | Returns a table with information about each general segment map segment metadata storage in the semantic model. This function provides metadata about segment map storage characteristics. |  | `functions-info-1:3358-3443` |
| INFO.GROUPBYCOLUMNS | info | table | Q | Returns a table with information about each group by column in the semantic model. This function provides metadata about columns used in group by operations. |  | `functions-info-1:3445-3550` |
| INFO.HIERARCHIES | info | table | Q | Returns a table with information about each hierarchy in the semantic model. This function provides metadata about hierarchies and their properties. |  | `functions-info-1:3552-3665` |
| INFO.HIERARCHYSTORAGES | info | table | Q | Returns a table with information about each hierarchy storage in the semantic model. This function provides metadata about how hierarchies are stored. |  | `functions-info-1:3667-3778` |
| INFO.KPIS | info | table | Q | Returns a table with information about each KPI in the semantic model. This function provides metadata about Key Performance Indicators defined in the model. |  | `functions-info-1:3780-3898` |
| INFO.LEVELS | info | table | Q | Returns a table with information about each level in the semantic model. This function provides metadata about hierarchy levels and their properties. |  | `functions-info-1:3900-4014` |
| INFO.LINGUISTICMETADATA | info | table | Q | Returns a table with information about each linguistic metadata entry in the semantic model. This function provides metadata about linguistic metadata definitions. |  | `functions-info-1:4016-4125` |
| INFO.MEASURES | info | table | Q | Returns a table with information about each measure in the semantic model, with columns that match the schema rowset for measure objects (for example, name, expression, and state). |  | `functions-info-1:4127-4216` |
| INFO.MODEL | info | table | Q | Returns a table with information about the model in the semantic model. This function provides metadata about the model itself and its properties. |  | `functions-info-1:4218-4311` |
| INFO.OBJECTTRANSLATIONS | info | table | Q | Returns a table with information about each object translation in the semantic model. This function provides metadata about translations for model objects. |  | `functions-info-1:4313-4423` |
| INFO.PARQUETFILESTORAGES | info | table | Q | Returns a table with information about each Parquet file storage in the semantic model. This function provides metadata about Parquet file storage characteristics. |  | `functions-info-2:5-122` |
| INFO.PARTITIONS | info | table | Q | Returns a table with information about each partition in the semantic model. This function provides metadata about table partitions and their properties. |  | `functions-info-2:124-262` |
| INFO.PARTITIONSTORAGES | info | table | Q | Returns a table with information about each partition storage in the semantic model. This function provides metadata about how partitions are stored. |  | `functions-info-2:264-387` |
| INFO.PERSPECTIVECOLUMNS | info | table | Q | Returns a table with information about each perspective column in the semantic model. This function provides metadata about columns included in perspectives. |  | `functions-info-2:389-508` |
| INFO.PERSPECTIVEHIERARCHIES | info | table | Q | Returns a table with information about each perspective hierarchy in the semantic model. This function provides metadata about hierarchies included in perspectives. |  | `functions-info-2:510-649` |
| INFO.PERSPECTIVEMEASURES | info | table | Q | Returns a table with information about each perspective measure in the semantic model. This function provides metadata about measures included in perspectives. |  | `functions-info-2:651-790` |
| INFO.PERSPECTIVES | info | table | Q | Returns a table with information about each perspective in the semantic model. This function provides metadata about perspectives defined in the model. |  | `functions-info-2:792-921` |
| INFO.PERSPECTIVETABLES | info | table | Q | Returns a table with information about each perspective table in the semantic model. This function provides metadata about tables included in perspectives. |  | `functions-info-2:923-1052` |
| INFO.PROPERTIES | info | table | Q | Returns a table with information about each property in the semantic model. This function provides metadata about properties defined for model objects. |  | `functions-info-2:1054-1130` |
| INFO.QUERYGROUPS | info | table | Q | Returns a table with information about each query group in the semantic model. This function provides metadata about query groups defined in the model. |  | `functions-info-2:1132-1205` |
| INFO.REFRESHPOLICIES | info | table | Q | Returns a table with information about each refresh policy in the semantic model. This function provides metadata about refresh policies defined for tables. |  | `functions-info-2:1207-1332` |
| INFO.RELATEDCOLUMNDETAILS | info | table | Q | Returns a table with information about each related column detail in the semantic model. This function provides metadata about related column details for relationships. |  | `functions-info-2:1334-1459` |
| INFO.RELATIONSHIPINDEXSTORAGES | info | table | Q | Returns a table with information about each relationship index storage in the semantic model. This function provides metadata about relationship index storage characteristics. |  | `functions-info-2:1461-1595` |
| INFO.RELATIONSHIPS | info | table | Q | Returns a table with information about each relationship in the semantic model. This function provides metadata about relationships between tables. |  | `functions-info-2:1597-1772` |
| INFO.RELATIONSHIPSTORAGES | info | table | Q | Returns a table with information about each relationship storage in the semantic model. This function provides metadata about how relationships are stored. |  | `functions-info-2:1774-1893` |
| INFO.ROLEMEMBERSHIPS | info | table | Q | Returns a table with information about each role membership in the semantic model. This function provides metadata about role memberships and security settings. |  | `functions-info-2:1895-1972` |
| INFO.ROLES | info | table | Q | Returns a table with information about each role in the semantic model. This function provides metadata about security roles defined in the model. |  | `functions-info-2:1974-2093` |
| INFO.SEGMENTMAPSTORAGES | info | table | Q | Returns a table with information about each segment map storage in the semantic model. This function provides metadata about segment map storage characteristics. |  | `functions-info-2:2095-2240` |
| INFO.SEGMENTSTORAGES | info | table | Q | Returns a table with information about each segment storage in the semantic model. This function provides metadata about segment storage characteristics. |  | `functions-info-2:2242-2368` |
| INFO.STORAGEFILES | info | table | Q | Returns a table with information about each storage file in the semantic model. This function provides metadata about storage files and their characteristics. |  | `functions-info-2:2370-2484` |
| INFO.STORAGEFOLDERS | info | table | Q | Returns a table with information about all table storage in the semantic model. This information helps you understand the model. |  | `functions-info-2:2486-2552` |
| INFO.STORAGETABLECOLUMNS | info | table | Q | Returns a table with information about all table storage in the semantic model. This information helps you understand the model. |  | `functions-info-2:2554-2635` |
| INFO.STORAGETABLECOLUMNSEGMENTS | info | table | Q | Returns a table with information about all table storage in the semantic model. This information helps you understand the model. |  | `functions-info-2:2637-2719` |
| INFO.STORAGETABLES | info | table | Q | Returns a table with information about all table storage in the semantic model. This information helps you understand the model. |  | `functions-info-2:2721-2793` |
| INFO.TABLEPERMISSIONS | info | table | Q | Returns a table with information about all table storage in the semantic model. This information helps you understand the model. |  | `functions-info-2:2795-2995` |
| INFO.TABLES | info | table | Q | Returns a table with information about each table in the semantic model, with columns that match the schema rowset for table objects (for example, name, description, and visibility). |  | `functions-info-2:2997-3143` |
| INFO.TABLESTORAGES | info | table | Q | Returns a table with information about all table storage in the semantic model. This information helps you understand the model. |  | `functions-info-2:3145-3266` |
| INFO.USERDEFINEDFUNCTIONS | info | table | Q | Returns a table with information about each user-defined function in the semantic model, with columns that match the schema rowset for user-defined function objects (for example, name, expression, and state). |  | `functions-info-2:3268-3347` |
| INFO.VARIATIONS | info | table | Q | Returns a table with information about all variations in the semantic model. This information helps you understand the model. |  | `functions-info-2:3349-3494` |
| INFO.VIEW.COLUMNS | info | table | M C T V | Returns a table with information about each column in the semantic model, such as name, description, and format string. This information helps you understand the model and to self-document the model when used in calculated tables. |  | `functions-info-2:3496-3669` |
| INFO.VIEW.MEASURES | info | table | M C T V | Returns a table with information about each measure in the semantic model, such as name, description, and DAX formula. This information helps you understand the model and to self-document the model when used in calculated tables. |  | `functions-info-2:3671-3809` |
| INFO.VIEW.RELATIONSHIPS | info | table | M C T V | Returns a table with information about each [relationship](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-create-and-manage-relationships) in the semantic model, such as name, cardinality, and cross-filtering behavior. This information helps you understand the model and to self-document the model when used in calculated tables. |  | `functions-info-2:3811-3942` |
| INFO.VIEW.TABLES | info | table | M C T V | Returns a table with information about each table in the semantic model, such as table name, description, and storage mode. This information helps you understand the model and to self-document the model when used in calculated tables. |  | `functions-info-2:3944-4111` |
| INT | math-and-trig | scalar | M C T V | Rounds a number down to the nearest integer. | ▶ | `functions-math-and-trig:1500-1565` |
| INTERSECT | table-manipulation | table | M C T V | Returns the row intersection of two tables, retaining duplicates. |  | `functions-table-manipulation:1143-1246` |
| INTRATE | financial | scalar | M C T V | Returns the interest rate for a fully invested security. |  | `functions-financial:1968-2073` |
| IPMT | financial | scalar | M C T V | Returns the interest payment for a given period for an investment based on periodic, constant payments and a constant interest rate. |  | `functions-financial:2075-2181` |
| ISAFTER | information | scalar | M C T V | A boolean function that emulates the behavior of a Start At clause and returns true for a row that meets all of the condition parameters. |  | `functions-information:599-681` |
| ISATLEVEL |  | scalar | V | Reports whether the column is present at the current level. |  | `functions-uncategorized:708-779` |
| ISBLANK | information | scalar | M C T V | Checks whether a value is blank, and returns `TRUE` or `FALSE`. | ▶ | `functions-information:683-759` |
| ISBOOLEAN | information | scalar | M C T V | Checks whether a value is a logical value, (`TRUE` or `FALSE`), and returns `TRUE` or `FALSE`. Alias of [ISLOGICAL](https://learn.microsoft.com/en-us/dax/islogical-function-dax). |  | `functions-information:761-821` |
| ISCROSSFILTERED | information | scalar | M C T V | Returns `TRUE` when `columnName` or another column in the same or related table is being filtered. |  | `functions-information:823-871` |
| ISCURRENCY | information | scalar | M C T V | Checks whether a value is a decimal number, and returns `TRUE` or `FALSE`. Alias of [ISDECIMAL](https://learn.microsoft.com/en-us/dax/isdecimal-function-dax). |  | `functions-information:873-935` |
| ISDATETIME | information | scalar | M C T V | Checks whether a value is a date / time, and returns `TRUE` or `FALSE`. | ▶ | `functions-information:937-1005` |
| ISDECIMAL | information | scalar | M C T V | Checks whether a value is a decimal number, and returns `TRUE` or `FALSE`. Alias of [ISCURRENCY](https://learn.microsoft.com/en-us/dax/iscurrency-function-dax). |  | `functions-information:1007-1069` |
| ISDOUBLE | information | scalar | M C T V | Checks whether a value is a floating-point number, and returns `TRUE` or `FALSE`. |  | `functions-information:1071-1131` |
| ISEMPTY | information | scalar | M C T V | Checks if a table is empty. |  | `functions-information:1133-1194` |
| ISERROR | information | scalar | M C T V | Checks whether a value is an error, and returns `TRUE` or `FALSE`. | ▶ | `functions-information:1196-1268` |
| ISEVEN | information | scalar | M C T V | Returns `TRUE` if number is even, or `FALSE` if number is odd. | ▶ | `functions-information:1270-1316` |
| ISFILTERED | information | scalar | M C T V | Returns `TRUE` when `columnName` is being filtered directly. |  | `functions-information:1318-1366` |
| ISINSCOPE | information | scalar | M C T V | Returns true when the specified column is the level in a hierarchy of levels. |  | `functions-information:1368-1469` |
| ISINT64 | information | scalar | M C T V | Checks whether a value is a whole number, and returns `TRUE` or `FALSE`. Alias of [ISINTEGER](https://learn.microsoft.com/en-us/dax/isinteger-function-dax). |  | `functions-information:1471-1533` |
| ISINTEGER | information | scalar | M C T V | Checks whether a value is a whole number, and returns `TRUE` or `FALSE`. Alias of [ISINT64](https://learn.microsoft.com/en-us/dax/isint64-function-dax). |  | `functions-information:1535-1597` |
| ISLOGICAL | information | scalar | M C T V | Checks whether a value is a logical value, (`TRUE` or `FALSE`), and returns `TRUE` or `FALSE`. Alias of [ISBOOLEAN](https://learn.microsoft.com/en-us/dax/isboolean-function-dax). |  | `functions-information:1599-1659` |
| ISNONTEXT | information | scalar | M C T V | Checks if a value is not text (blank cells are not text), and returns `TRUE` or `FALSE`. | ▶ | `functions-information:1661-1728` |
| ISNUMBER | information | scalar | M C T V | Checks whether a value is a number, and returns `TRUE` or `FALSE`. Alias of [ISNUMERIC](https://learn.microsoft.com/en-us/dax/isnumeric-function-dax). | ▶ | `functions-information:1730-1798` |
| ISNUMERIC | information | scalar | M C T V | Checks whether a value is a number, and returns `TRUE` or `FALSE`. Alias of [ISNUMBER](https://learn.microsoft.com/en-us/dax/isnumber-function-dax). | ▶ | `functions-information:1800-1868` |
| ISO.CEILING | math-and-trig | scalar | M C T V | Rounds a number up, to the nearest integer or to the nearest multiple of significance. | ▶ | `functions-math-and-trig:1567-1651` |
| ISODD | information | scalar | M C T V | Returns `TRUE` if number is odd, or `FALSE` if number is even. | ▶ | `functions-information:1870-1916` |
| ISONORAFTER | information | scalar | M C T V | A boolean function that emulates the behavior of a Start At clause and returns true for a row that meets all of the condition parameters. |  | `functions-information:1918-2001` |
| ISPMT | financial | scalar | M C T V | Calculates the interest paid (or received) for the specified period of a loan (or investment) with even principal payments. |  | `functions-financial:2183-2282` |
| ISSELECTEDMEASURE | information | scalar | M C T | Used by expressions for calculation items to determine the measure that is in context is one of those specified in a list of measures. |  | `functions-information:2003-2065` |
| ISSTRING | information | scalar | M C T V | Checks if a value is text, and returns `TRUE` or `FALSE`. Alias of [ISTEXT](https://learn.microsoft.com/en-us/dax/istext-function-dax). | ▶ | `functions-information:2067-2137` |
| ISSUBTOTAL | information | scalar | M C T | Creates another column in a SUMMARIZE expression that returns True if the row contains subtotal values for the column given as argument, otherwise returns False. |  | `functions-information:2139-2193` |
| ISTEXT | information | scalar | M C T V | Checks if a value is text, and returns `TRUE` or `FALSE`. Alias of [ISSTRING](https://learn.microsoft.com/en-us/dax/isstring-function-dax). | ▶ | `functions-information:2195-2264` |
| KEEPFILTERS | filter | table | M C T V | Modifies how filters are applied while evaluating a CALCULATE or CALCULATETABLE function. | ★ | `functions-filter:1547-1672` |
| LAST | filter | scalar | V | Used in visual calculations only. Retrieves a value in the visual matrix from the last row of an axis. |  | `functions-filter:1674-1740` |
| LASTDATE | time-intelligence | table | M C T V | Returns the last date in the current context for the specified column of dates. | ⛔ | `functions-time-intelligence:1464-1544` |
| LASTNONBLANK | filter | table | M C T V | Returns the last value in the column, `column`, filtered by the current context, where the expression is not blank. | ⛔ | `functions-filter:1742-1794` |
| LASTNONBLANKVALUE | filter | scalar | M C T V | Evaluates an expression filtered by the sorted values of a column and returns the last value of the expression that is not blank. | ⛔ | `functions-filter:1796-1870` |
| LCM | math-and-trig | scalar | M C T V | Returns the least common multiple of integers. | ▶ | `functions-math-and-trig:1653-1715` |
| LEFT | text | scalar | M C T V | Returns the specified number of characters from the start of a text string. | ▶ | `functions-text:815-889` |
| LEN | text | scalar | M C T V | Returns the number of characters in a text string. | ▶ | `functions-text:891-952` |
| LINEST | statistical | scalar | M C T V | Uses the Least Squares method to calculate a straight line that best fits the given data. |  | `functions-statistical:792-914` |
| LINESTX | statistical | scalar | M C T V | Uses the Least Squares method to calculate a straight line that best fits the given data. The data result from expressions evaluated for each row in a table. |  | `functions-statistical:916-1044` |
| LN | math-and-trig | scalar | M C T V | Returns the natural logarithm of a number. | ▶ | `functions-math-and-trig:1717-1779` |
| LOG | math-and-trig | scalar | M C T V | Returns the logarithm of a number to the base you specify. | ▶ | `functions-math-and-trig:1781-1850` |
| LOG10 | math-and-trig | scalar | M C T V | Returns the base-10 logarithm of a number. | ▶ | `functions-math-and-trig:1852-1919` |
| LOOKUP | filter | scalar | V | In visual calculation mode only. Look up the value when filters applied. |  | `functions-filter:1872-1940` |
| LOOKUPVALUE | filter | scalar | M C T | Returns the value for the row that meets all criteria specified by search conditions. The function can apply one or more search conditions. | ★ | `functions-filter:1942-2050` |
| LOOKUPWITHTOTALS | filter | scalar | V | In visual calculation mode only. Look up the value when filters applied. Filters not specified will not be inferred. |  | `functions-filter:2052-2119` |
| LOWER | text | scalar | M C T V | Converts all letters in a text string to lowercase. | ▶ | `functions-text:954-1015` |
| MATCHBY | filter | scalar | M C T V | In window functions, defines the columns that are used to determine how to match data and identify the *current row*. |  | `functions-filter:2121-2178` |
| MAX | aggregation | scalar | M C T V | Returns the largest numeric value in a column, or between two scalar expressions. |  | `functions-aggregation:837-903` |
| MAXA | aggregation | scalar | M C T V | Returns the largest value in a column. |  | `functions-aggregation:905-974` |
| MAXX | aggregation | scalar | M C T V | Evaluates an expression for each row of a table and returns the largest numeric value. | ★ | `functions-aggregation:976-1048` |
| MDURATION | financial | scalar | M C T V | Returns the modified Macauley duration for a security with an assumed par value of $100. |  | `functions-financial:2284-2387` |
| MEDIAN | statistical | scalar | M C T V | Returns the median of numbers in a column. |  | `functions-statistical:1046-1106` |
| MEDIANX | statistical | scalar | M C T V | Returns the median number of an expression evaluated for each row in a table. |  | `functions-statistical:1108-1173` |
| MID | text | scalar | M C T V | Returns a string of characters from the middle of a text string, given a starting position and length. | ▶ | `functions-text:1017-1091` |
| MIN | aggregation | scalar | M C T V | Returns the smallest numeric value in a column, or between two scalar expressions. |  | `functions-aggregation:1050-1130` |
| MINA | aggregation | scalar | M C T V | Returns the smallest value in a column, including any logical values and numbers represented as text. |  | `functions-aggregation:1132-1198` |
| MINUTE | date-and-time | scalar | M C T V | Returns the minute as a number from 0 to 59, given a date and time value. |  | `functions-date-and-time:667-729` |
| MINX | aggregation | scalar | M C T V | Returns the smallest numeric value that results from evaluating an expression for each row of a table. |  | `functions-aggregation:1200-1269` |
| MOD | math-and-trig | scalar | M C T V | Returns the remainder after a number is divided by a divisor. The result always has the same sign as the divisor. | ▶ | `functions-math-and-trig:1921-1993` |
| MONTH | date-and-time | scalar | M C T V | Returns the month as a number from 1 (January) to 12 (December). |  | `functions-date-and-time:731-798` |
| MOVINGAVERAGE | filter | scalar | V | Returns a moving average calculated along the given axis of the visual matrix. |  | `functions-filter:2180-2255` |
| MROUND | math-and-trig | scalar | M C T V | Returns a number rounded to the desired multiple. | ▶ | `functions-math-and-trig:1995-2073` |
| NAMEOF | information | scalar | M C T V | Returns the name of a table, column, measure, or calendar as a text string. |  | `functions-information:2266-2461` |
| NATURALINNERJOIN | table-manipulation | table | M C T V | Performs an inner join of a table with another table. |  | `functions-table-manipulation:1248-1300` |
| NATURALLEFTOUTERJOIN | table-manipulation | table | M C T V | Performs a join of the LeftTable with the RightTable. |  | `functions-table-manipulation:1302-1354` |
| NETWORKDAYS | date-and-time | scalar | M C T V | Returns the number of whole workdays between two dates. |  | `functions-date-and-time:800-874` |
| NEXT | filter | scalar | V | Used in visual calculations only. Retrieves a value in the next row of an axis in the visual matrix. |  | `functions-filter:2257-2324` |
| NEXTDAY | time-intelligence | table | M C T V | Returns a table that contains a column of all dates from the next day, based on the last date specified in the dates column in the current context. | ⛔ | `functions-time-intelligence:1546-1633` |
| NEXTMONTH | time-intelligence | table | M C T V | Returns a table that contains a column of all dates from the next month, based on the last date in the dates column in the current context. | ⛔ | `functions-time-intelligence:1635-1721` |
| NEXTQUARTER | time-intelligence | table | M C T V | Returns a table that contains a column of all dates in the next quarter, based on the last date specified in the dates column, in the current context. | ⛔ | `functions-time-intelligence:1723-1809` |
| NEXTWEEK | time-intelligence | table | M C T V | Returns a table that contains a column of all dates from the next week, based on the last date in the dates column in the current context. | ⛔ | `functions-time-intelligence:1811-1880` |
| NEXTYEAR | time-intelligence | table | M C T V | Returns a table that contains a column of all dates in the next year, based on the last date in the dates column, in the current context. | ⛔ | `functions-time-intelligence:1882-1971` |
| NOMINAL | financial | scalar | M C T V | Returns the nominal annual interest rate, given the effective rate and the number of compounding periods per year. |  | `functions-financial:2389-2464` |
| NONFILTER |  | table | M C T | Modifies how filters are applied while evaluating a GROUPCROSSAPPLY or GROUPCROSSAPPLYTABLE function. |  | `functions-uncategorized:781-826` |
| NONVISUAL | information | table | M C T | Marks a value filter in a SUMMARIZECOLUMNS expression as non-visual. |  | `functions-information:2463-2511` |
| NORM.DIST | statistical | scalar | M C T V | Returns the normal distribution for the specified mean and standard deviation. |  | `functions-statistical:1175-1238` |
| NORM.INV | statistical | scalar | M C T V | The inverse of the normal cumulative distribution for the specified mean and standard deviation. |  | `functions-statistical:1240-1303` |
| NORM.S.DIST | statistical | scalar | M C T V | Returns the standard normal distribution (has a mean of zero and a standard deviation of one). |  | `functions-statistical:1305-1366` |
| NORM.S.INV | statistical | scalar | M C T V | Returns the inverse of the standard normal cumulative distribution. |  | `functions-statistical:1368-1428` |
| NOT | logical | scalar | M C T V | Changes `FALSE` to `TRUE`, or `TRUE` to `FALSE`. | ▶ | `functions-logical:923-988` |
| NOW | date-and-time | scalar | M C T V | Returns the current date and time in datetime format. |  | `functions-date-and-time:876-931` |
| NPER | financial | scalar | M C T V | Returns the number of periods for an investment based on periodic, constant payments and a constant interest rate. |  | `functions-financial:2466-2546` |
| ODD | math-and-trig | scalar | M C T V | Returns number rounded up to the nearest odd integer. | ▶ | `functions-math-and-trig:2075-2138` |
| ODDFPRICE | financial | scalar | M C T V | Returns the price per \$100 face value of a security having an odd (short or long) first period. |  | `functions-financial:2548-2683` |
| ODDFYIELD | financial | scalar | M C T V | Returns the yield of a security that has an odd (short or long) first period. |  | `functions-financial:2685-2793` |
| ODDLPRICE | financial | scalar | M C T V | Returns the price per $100 face value of a security having an odd (short or long) last coupon period. |  | `functions-financial:2795-2899` |
| ODDLYIELD | financial | scalar | M C T V | Returns the yield of a security that has an odd (short or long) last period. |  | `functions-financial:2901-3016` |
| OFFSET | filter | table | M C T V | Returns a single row that is positioned either before or after the *current row* within the same table, by a given offset. |  | `functions-filter:2326-2492` |
| OPENINGBALANCEMONTH | time-intelligence | scalar | M C T V | Evaluates the expression at the first date of the month in the current context. | ⛔ | `functions-time-intelligence:1973-2063` |
| OPENINGBALANCEQUARTER | time-intelligence | scalar | M C T V | Evaluates the expression at the first date of the quarter, in the current context. | ⛔ | `functions-time-intelligence:2065-2156` |
| OPENINGBALANCEWEEK | time-intelligence | scalar | M C T V | Evaluates the expression at the first date of the week in the current context. | ⛔ | `functions-time-intelligence:2158-2228` |
| OPENINGBALANCEYEAR | time-intelligence | scalar | M C T V | Evaluates the expression at the first date of the year in the current context. | ⛔ | `functions-time-intelligence:2230-2326` |
| OR | logical | scalar | M C T V | Checks whether one of the arguments is `TRUE` to return `TRUE`. | ▶ | `functions-logical:990-1081` |
| ORDERBY | filter | scalar | M C T V | Defines the columns that determine the sort order within each of a window function’s partitions. |  | `functions-filter:2494-2553` |
| PARALLELPERIOD | time-intelligence | table | M C T V | Returns a table that contains a column of dates that represents a period parallel to the dates in the specified dates column, in the current context, with the dates shifted a number of intervals either forward in time or back in time. | ⛔ | `functions-time-intelligence:2328-2420` |
| PARTITIONBY | filter | scalar | M C T V | Defines the columns that are used to partition a window function’s `relation` parameter. |  | `functions-filter:2555-2612` |
| PATH | parent-and-child | scalar | M C T V | Returns a delimited text string with the identifiers of all the parents of the current identifier. |  | `functions-parent-and-child:5-67` |
| PATHCONTAINS | parent-and-child | scalar | M C T V | Returns `TRUE` if the specified `item` exists within the specified `path`. |  | `functions-parent-and-child:69-122` |
| PATHITEM | parent-and-child | scalar | M C T V | Returns the item at the specified `position` from a string resulting from evaluation of a PATH function. |  | `functions-parent-and-child:124-189` |
| PATHITEMREVERSE | parent-and-child | scalar | M C T V | Returns the item at the specified `position` from a string resulting from evaluation of a PATH function. |  | `functions-parent-and-child:191-258` |
| PATHLENGTH | parent-and-child | scalar | M C T V | Returns the number of parents to the specified item in a given PATH result, including self. |  | `functions-parent-and-child:260-310` |
| PDURATION | financial | scalar | M C T V | Returns the number of periods required by an investment to reach a specified value. |  | `functions-financial:3018-3100` |
| PERCENTILE.EXC | statistical | scalar | M C T V | Returns the k-th percentile of values in a range, where k is in the range 0..1, exclusive. |  | `functions-statistical:1430-1484` |
| PERCENTILE.INC | statistical | scalar | M C T V | Returns the k-th percentile of values in a range, where k is in the range 0..1, inclusive. |  | `functions-statistical:1486-1540` |
| PERCENTILEX.EXC | statistical | scalar | M C T V | Returns the percentile number of an expression evaluated for each row in a table. |  | `functions-statistical:1542-1595` |
| PERCENTILEX.INC | statistical | scalar | M C T V | Returns the percentile number of an expression evaluated for each row in a table. |  | `functions-statistical:1597-1650` |
| PERMUT | statistical | scalar | M C T V | Returns the number of permutations for a given number of objects that can be selected from number objects. |  | `functions-statistical:1652-1719` |
| PI | math-and-trig | scalar | M C T V | Returns the value of Pi, 3.14159265358979, accurate to 15 digits. | ▶ | `functions-math-and-trig:2140-2195` |
| PMT | financial | scalar | M C T V | Calculates the payment for a loan based on constant payments and a constant interest rate. |  | `functions-financial:3102-3218` |
| POISSON.DIST | statistical | scalar | M C T V | Returns the Poisson distribution. |  | `functions-statistical:1721-1778` |
| POWER | math-and-trig | scalar | M C T V | Returns the result of a number raised to a power. | ▶ | `functions-math-and-trig:2197-2255` |
| PPMT | financial | scalar | M C T V | Returns the payment on the principal for a given period for an investment based on periodic, constant payments and a constant interest rate. |  | `functions-financial:3220-3325` |
| PREVIOUS | filter | scalar | V | Used in visual calculations only. Retrieves a value in the previous row of an axis in the visual matrix. |  | `functions-filter:2614-2681` |
| PREVIOUSDAY | time-intelligence | table | M C T V | Returns a table that contains a column of all dates representing the day that is previous to the first date in the dates column, in the current context. | ⛔ | `functions-time-intelligence:2422-2508` |
| PREVIOUSMONTH | time-intelligence | table | M C T V | Returns a table that contains a column of all dates from the previous month, based on the first date in the dates column, in the current context. | ⛔★ | `functions-time-intelligence:2510-2592` |
| PREVIOUSQUARTER | time-intelligence | table | M C T V | Returns a table that contains a column of all dates from the previous quarter, based on the first date in the dates column, in the current context. | ⛔ | `functions-time-intelligence:2594-2679` |
| PREVIOUSWEEK | time-intelligence | table | M C T V | Returns a table that contains a column of all dates representing the week that is previous to the first date in the dates column, in the current context. | ⛔ | `functions-time-intelligence:2681-2745` |
| PREVIOUSYEAR | time-intelligence | table | M C T V | Returns a table that contains a column of all dates from the previous year, based on the first date in the dates column, in the current context. | ⛔ | `functions-time-intelligence:2747-2837` |
| PRICE | financial | scalar | M C T V | Returns the price per \$100 face value of a security that pays periodic interest. |  | `functions-financial:3327-3453` |
| PRICEDISC | financial | scalar | M C T V | Returns the price per \$100 face value of a discounted security. |  | `functions-financial:3455-3560` |
| PRICEMAT | financial | scalar | M C T V | Returns the price per $100 face value of a security that pays interest at maturity. |  | `functions-financial:3562-3671` |
| PRODUCT | aggregation | scalar | M C T V | Returns the product of the numbers in a column. |  | `functions-aggregation:1271-1331` |
| PRODUCTX | aggregation | scalar | M C T V | Returns the product of an expression evaluated for each row in a table. |  | `functions-aggregation:1333-1394` |
| PV | financial | scalar | M C T V | Calculates the present value of a loan or an investment, based on a constant interest rate. |  | `functions-financial:3673-3781` |
| QUARTER | date-and-time | scalar | M C T V | Returns the quarter as a number from 1 to 4. |  | `functions-date-and-time:933-1016` |
| QUOTIENT | math-and-trig | scalar | M C T V | Performs division and returns only the integer portion of the division result. | ▶ | `functions-math-and-trig:2257-2325` |
| RADIANS | math-and-trig | scalar | M C T V | Converts degrees to radians. | ▶ | `functions-math-and-trig:2327-2374` |
| RAND | math-and-trig | scalar | M C T V | Returns a random number greater than or equal to 0 and less than 1, evenly distributed. | ▶ | `functions-math-and-trig:2376-2461` |
| RANDBETWEEN | math-and-trig | scalar | M C T V | Returns a random number in the range between two numbers you specify. | ▶ | `functions-math-and-trig:2463-2526` |
| RANGE | filter | table | V | Returns an interval of rows within the given axis, relative to the current row. A shortcut for WINDOW. |  | `functions-filter:2683-2756` |
| RANK | filter | scalar | M C T V | Returns the ranking of a row within the given interval. |  | `functions-filter:2758-2860` |
| RANK.EQ | statistical | scalar | M C T V | Returns the ranking of a number in a list of numbers. |  | `functions-statistical:1780-1848` |
| RANKX | statistical | scalar | M C T V | Returns the ranking of a number in a list of numbers for each row in the `table` argument. | ★ | `functions-statistical:1850-1931` |
| RATE | financial | scalar | M C T V | Returns the interest rate per period of an annuity. |  | `functions-financial:3783-3887` |
| RECEIVED | financial | scalar | M C T V | Returns the amount received at maturity for a fully invested security. |  | `functions-financial:3889-3994` |
| RELATED | relationship | scalar | M C T | Returns a related value from another table. | ★ | `functions-relationship:90-197` |
| RELATEDTABLE | relationship | table | M C T | Evaluates a table expression in a context modified by the given filters. | ★ | `functions-relationship:199-270` |
| REMOVEFILTERS | filter | modifier | M C T V | Clears filters from the specified tables or columns. | ★ | `functions-filter:2862-2973` |
| REPLACE | text | scalar | M C T V | REPLACE replaces part of a text string, based on the number of characters you specify, with a different text string. | ▶ | `functions-text:1093-1162` |
| REPT | text | scalar | M C T V | Repeats text a given number of times. | ▶ | `functions-text:1164-1239` |
| RIGHT | text | scalar | M C T V | RIGHT returns the last character or characters in a text string, based on the number of characters you specify. | ▶ | `functions-text:1241-1312` |
| ROLLUP | table-manipulation | scalar | M C T | Modifies the behavior of SUMMARIZE by adding rollup rows to the result on columns defined by the groupBy_columnName parameter. |  | `functions-table-manipulation:1356-1408` |
| ROLLUPADDISSUBTOTAL | table-manipulation | scalar | M C T | Modifies the behavior of SUMMARIZECOLUMNS by adding rollup/subtotal rows to the result based on the groupBy_columnName columns. |  | `functions-table-manipulation:1410-1459` |
| ROLLUPGROUP | table-manipulation | scalar | M C T | Modifies the behavior of SUMMARIZE and SUMMARIZECOLUMNS by adding rollup rows to the result on columns defined by the the groupBy_columnName parameter. |  | `functions-table-manipulation:1461-1507` |
| ROLLUPISSUBTOTAL | table-manipulation | scalar | M C T | Pairs rollup groups with the column added by ROLLUPADDISSUBTOTAL within an ADDMISSINGITEMS expression. |  | `functions-table-manipulation:1509-1549` |
| ROUND | math-and-trig | scalar | M C T V | Rounds a number to the specified number of digits. | ▶ | `functions-math-and-trig:2528-2613` |
| ROUNDDOWN | math-and-trig | scalar | M C T V | Rounds a number down, toward zero. | ▶ | `functions-math-and-trig:2615-2691` |
| ROUNDUP | math-and-trig | scalar | M C T V | Rounds a number up, away from 0 (zero). | ▶ | `functions-math-and-trig:2693-2791` |
| ROW | table-manipulation | scalar | M C T V | Returns a table with a single row containing values that result from the expressions given to each column. |  | `functions-table-manipulation:1551-1605` |
| ROWNUMBER | filter | scalar | M C T V | Returns the unique ranking of a row within the given interval. |  | `functions-filter:2975-3083` |
| RRI | financial | scalar | M C T V | Returns an equivalent interest rate for the growth of an investment. |  | `functions-financial:3996-4070` |
| RUNNINGSUM | filter | scalar | V | Returns a running sum calculated along the given axis of the visual matrix. |  | `functions-filter:3085-3155` |
| SAMEPERIODLASTYEAR | time-intelligence | scalar | M C T V | Returns a table that contains a column of dates shifted one year back in time from the dates in the specified dates column, in the current context. | ⛔★ | `functions-time-intelligence:2839-2930` |
| SAMPLE | statistical | table | M C T V | Returns a sample of N rows from the specified table. |  | `functions-statistical:1933-1977` |
| SAMPLEAXISWITHLOCALMINMAX |  | scalar | M C T V | Returns a sample subset from a Table that is obtained by binning the primary X-axis into equal-sized bins and preserving the local min/max for each bin across different series. |  | `functions-uncategorized:828-899` |
| SAMPLECARTESIANPOINTSBYCOVER | statistical | scalar | M C T V | Returns a sample subset from a Table that is obtained by plotting the rows as points in 2D space and removing overlapping points. |  | `functions-statistical:1979-2047` |
| SEARCH | text | scalar | M C T V | Returns the number of the character at which a specific character or text string is first found, reading left to right. | ★▶ | `functions-text:1314-1417` |
| SECOND | date-and-time | scalar | M C T V | Returns the seconds of a time value, as a number from 0 to 59. |  | `functions-date-and-time:1018-1084` |
| SELECTCOLUMNS | table-manipulation | table | M C T V | Adds calculated columns to the given table or table expression. |  | `functions-table-manipulation:1607-1679` |
| SELECTEDMEASURE | information | scalar | M C T | Used by expressions for calculation items to reference the measure that is in context. |  | `functions-information:2513-2579` |
| SELECTEDMEASUREFORMATSTRING | information | scalar | M C T | Used by expressions for calculation items to retrieve the format string of the measure that is in context. |  | `functions-information:2581-2636` |
| SELECTEDMEASURENAME | information | scalar | M C T | Used by expressions for calculation items to determine the measure that is in context by name. |  | `functions-information:2638-2697` |
| SELECTEDVALUE | filter | scalar | M C T V | Returns the value when the context for columnName has been filtered down to one distinct value only. Otherwise returns alternateResult. | ★ | `functions-filter:3157-3234` |
| SHADOWCLUSTER |  | table | M C T | Modifies how filters are applied while evaluating a GROUPCROSSAPPLY or GROUPCROSSAPPLYTABLE function. |  | `functions-uncategorized:901-947` |
| SIGN | math-and-trig | scalar | M C T V | Determines the sign of a number, the result of a calculation, or a value in a column. | ▶ | `functions-math-and-trig:2793-2856` |
| SIN | math-and-trig | scalar | M C T V | Returns the sine of the given angle. | ▶ | `functions-math-and-trig:2858-2916` |
| SINH | math-and-trig | scalar | M C T V | Returns the hyperbolic sine of a number. | ▶ | `functions-math-and-trig:2918-2981` |
| SLN | financial | scalar | M C T V | Returns the straight-line depreciation of an asset for one period. |  | `functions-financial:4072-4142` |
| SQRT | math-and-trig | scalar | M C T V | Returns the square root of a number. | ▶ | `functions-math-and-trig:2983-3044` |
| SQRTPI | math-and-trig | scalar | M C T V | Returns the square root of (number * pi). | ▶ | `functions-math-and-trig:3046-3098` |
| STARTOFMONTH | time-intelligence | table | M C T V | Returns the first date of the month in the current context for the specified column of dates. | ⛔ | `functions-time-intelligence:2932-3007` |
| STARTOFQUARTER | time-intelligence | table | M C T V | Returns the first date of the quarter in the current context for the specified column of dates. | ⛔ | `functions-time-intelligence:3009-3083` |
| STARTOFWEEK | time-intelligence | table | M C T V | Returns the first date of the week in the current context for the specified column of dates. | ⛔ | `functions-time-intelligence:3085-3144` |
| STARTOFYEAR | time-intelligence | table | M C T V | Returns the first date of the year in the current context for the specified column of dates. | ⛔ | `functions-time-intelligence:3146-3224` |
| STDEV.P | statistical | scalar | M C T V | Returns the standard deviation of the entire population. |  | `functions-statistical:2049-2111` |
| STDEV.S | statistical | scalar | M C T V | Returns the standard deviation of a sample population. |  | `functions-statistical:2113-2177` |
| STDEVX.P | statistical | scalar | M C T V | Returns the standard deviation of the entire population. |  | `functions-statistical:2179-2242` |
| STDEVX.S | statistical | scalar | M C T V | Returns the standard deviation of a sample population. |  | `functions-statistical:2244-2309` |
| SUBSTITUTE | text | scalar | M C T V | Replaces existing text with new text in a text string. | ▶ | `functions-text:1419-1483` |
| SUBSTITUTEWITHINDEX | table-manipulation | table | M C T | Returns a table which represents a left semijoin of the two tables supplied as arguments. |  | `functions-table-manipulation:1681-1728` |
| SUM | aggregation | scalar | M C T V | Adds all the numbers in a column. |  | `functions-aggregation:1396-1450` |
| SUMMARIZE | table-manipulation | table | M C T V | Returns a summary table for the requested totals over a set of groups. |  | `functions-table-manipulation:1730-1947` |
| SUMMARIZECOLUMNS | table-manipulation | table | M C T | Returns a summary table over a set of groups. |  | `functions-table-manipulation:1949-2322` |
| SUMX | aggregation | scalar | M C T V | Returns the sum of an expression evaluated for each row in a table. | ★ | `functions-aggregation:1452-1518` |
| SWITCH | logical | scalar | M C T V | Evaluates an expression against a list of values and returns one of multiple possible result expressions. | ▶ | `functions-logical:1083-1198` |
| SYD | financial | scalar | M C T V | Returns the sum-of-years' digits depreciation of an asset for a specified period. |  | `functions-financial:4144-4239` |
| T.DIST | statistical | scalar | M C T V | Returns the Student's left-tailed t-distribution. |  | `functions-statistical:2311-2375` |
| T.DIST.2T | statistical | scalar | M C T V | Returns the two-tailed Student's t-distribution. |  | `functions-statistical:2377-2440` |
| T.DIST.RT | statistical | scalar | M C T V | Returns the right-tailed Student's t-distribution. |  | `functions-statistical:2442-2504` |
| T.INV | statistical | scalar | M C T V | Returns the left-tailed inverse of the Student's t-distribution. |  | `functions-statistical:2506-2568` |
| T.INV.2T | statistical | scalar | M C T V | Returns the two-tailed inverse of the Student's t-distribution. |  | `functions-statistical:2570-2632` |
| TABLEOF | information | table | M C T | Returns a reference to the table associated with a specified column, measure, or calendar. |  | `functions-information:2699-2800` |
| TAN | math-and-trig | scalar | M C T V | Returns the tangent of the given angle. | ▶ | `functions-math-and-trig:3100-3157` |
| TANH | math-and-trig | scalar | M C T V | Returns the hyperbolic tangent of a number. | ▶ | `functions-math-and-trig:3159-3220` |
| TBILLEQ | financial | scalar | M C T V | Returns the bond-equivalent yield for a Treasury bill. |  | `functions-financial:4241-4325` |
| TBILLPRICE | financial | scalar | M C T V | Returns the price per $100 face value for a Treasury bill. |  | `functions-financial:4327-4411` |
| TBILLYIELD | financial | scalar | M C T V | Returns the yield for a Treasury bill. |  | `functions-financial:4413-4497` |
| TIME | date-and-time | scalar | M C T V | Converts hours, minutes, and seconds given as numbers to a time in datetime format. |  | `functions-date-and-time:1086-1170` |
| TIMEVALUE | date-and-time | scalar | M C T V | Converts a time in text format to a time in datetime format. |  | `functions-date-and-time:1172-1228` |
| TOCSV | other | scalar | M C T V | Returns a table as a string in CSV format. |  | `functions-other:387-459` |
| TODAY | date-and-time | scalar | M C T V | Returns the current date. |  | `functions-date-and-time:1230-1285` |
| TOJSON | other | scalar | M C T V | Returns a table as a string in JSON format. |  | `functions-other:461-535` |
| TOPN | table-manipulation | table | M C T V | Returns the top N rows of the specified table. | ★ | `functions-table-manipulation:2324-2395` |
| TOPNSKIP |  | table | M C T V | Returns the top N rows of the specified table, skipping a number of rows. |  | `functions-uncategorized:949-1032` |
| TOTALMTD | time-intelligence | scalar | M C T V | Evaluates the value of the expression for the month to date, in the current context. | ⛔ | `functions-time-intelligence:3226-3303` |
| TOTALQTD | time-intelligence | scalar | M C T V | Evaluates the value of the expression for the dates in the quarter to date, in the current context. | ⛔ | `functions-time-intelligence:3305-3382` |
| TOTALWTD | time-intelligence | scalar | M C T V | Evaluates the value of the expression for the week to date, in the current context. | ⛔ | `functions-time-intelligence:3384-3447` |
| TOTALYTD | time-intelligence | scalar | M C T V | Evaluates the year-to-date value of the expression in the current context. | ⛔ | `functions-time-intelligence:3449-3538` |
| TREATAS | table-manipulation | table | M C T V | Applies the result of a table expression as filters to columns from an unrelated table. |  | `functions-table-manipulation:2397-2466` |
| TRIM | text | scalar | M C T V | Removes all spaces from text except for single spaces between words. | ▶ | `functions-text:1485-1556` |
| TRUE | logical | scalar | M C T V | Returns the logical value `TRUE`. | ▶ | `functions-logical:1200-1268` |
| TRUNC | math-and-trig | scalar | M C T V | Truncates a number to an integer by removing the decimal, or fractional, part of the number. | ▶ | `functions-math-and-trig:3222-3292` |
| UNICHAR | text | scalar | M C T V | Returns the Unicode character referenced by the numeric value. | ▶ | `functions-text:1558-1635` |
| UNICODE | text | scalar | M C T V | Returns the numeric code corresponding to the first character of the text string. | ▶ | `functions-text:1637-1677` |
| UNION | table-manipulation | table | M C T V | Creates a union (join) table from a pair of tables. |  | `functions-table-manipulation:2468-2557` |
| UPPER | text | scalar | M C T V | Converts a text string to all uppercase letters. | ▶ | `functions-text:1679-1737` |
| USERCULTURE | information | scalar | M C T V | Returns the locale for the current user. |  | `functions-information:2802-2880` |
| USERELATIONSHIP | relationship | scalar | M C T | Specifies the relationship to be used in a specific calculation as the one that exists between columnName1 and columnName2. |  | `functions-relationship:272-343` |
| USERNAME | information | scalar | M C T V | Returns the domain name and username from the credentials given to the system at connection time. |  | `functions-information:2882-2926` |
| USEROBJECTID | information | scalar | M C T V | Returns the current user's Object ID or SID. |  | `functions-information:2928-2959` |
| USERPRINCIPALNAME | information | scalar | M C T V | Returns the user principal name. |  | `functions-information:2961-2992` |
| UTCNOW | date-and-time | scalar | M C T V | Returns the current UTC date and time |  | `functions-date-and-time:1287-1342` |
| UTCTODAY | date-and-time | scalar | M C T V | Returns the current UTC date. |  | `functions-date-and-time:1344-1401` |
| VALUE | text | scalar | M C T V | Converts a text string that represents a number to a number. | ▶ | `functions-text:1739-1804` |
| VALUES | table-manipulation | table | M C T V | Returns a one-column table that contains the distinct values from the specified table or column. | ★ | `functions-table-manipulation:2559-2650` |
| VAR.P | statistical | scalar | M C T V | Returns the variance of the entire population. |  | `functions-statistical:2634-2698` |
| VAR.S | statistical | scalar | M C T V | Returns the variance of a sample population. |  | `functions-statistical:2700-2764` |
| VARX.P | statistical | scalar | M C T V | Returns the variance of the entire population. |  | `functions-statistical:2766-2831` |
| VARX.S | statistical | scalar | M C T V | Returns the variance of a sample population. |  | `functions-statistical:2833-2898` |
| VDB | financial | scalar | M C T V | Returns the depreciation of an asset for any period you specify, including partial periods, using the double-declining balance method or some other method you specify. |  | `functions-financial:4499-4615` |
| WEEKDAY | date-and-time | scalar | M C T V | Returns a number from 1 to 7 identifying the day of the week of a date. |  | `functions-date-and-time:1403-1464` |
| WEEKNUM | date-and-time | scalar | M C T V | Returns the week number for the given date and year according to the return_type value. |  | `functions-date-and-time:1466-1545` |
| WINDOW | filter | table | M C T V | Returns multiple rows which are positioned within the given interval. | ★ | `functions-filter:3236-3434` |
| XIRR | financial | scalar | M C T V | Returns the internal rate of return for a schedule of cash flows that is not necessarily periodic. |  | `functions-financial:4617-4701` |
| XNPV | financial | scalar | M C T V | Returns the present value for a schedule of cash flows that is not necessarily periodic. |  | `functions-financial:4703-4778` |
| YEAR | date-and-time | scalar | M C T V | Returns the year of a date as a four digit integer in the range 1900-9999. |  | `functions-date-and-time:1547-1621` |
| YEARFRAC | date-and-time | scalar | M C T V | Calculates the fraction of the year represented by the number of whole days between two dates. |  | `functions-date-and-time:1623-1693` |
| YIELD | financial | scalar | M C T V | Returns the yield on a security that pays periodic interest. |  | `functions-financial:4780-4894` |
| YIELDDISC | financial | scalar | M C T V | Returns the annual yield for a discounted security. |  | `functions-financial:4896-4992` |
| YIELDMAT | financial | scalar | M C T V | Returns the annual yield of a security that pays interest at maturity. |  | `functions-financial:4994-5092` |
