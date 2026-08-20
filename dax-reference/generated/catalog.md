# DAX Reference — catálogo de funciones (índice generado)

> Fuente: `MicrosoftDocs/query-docs@323524c` · commit 2026-08-13T16:02:28Z
> 479 funciones · generado por `scripts/sync_query_docs.py`
> **No editar a mano.** ⛔ = Microsoft la desaconseja **en cálculos visuales** (dice que probablemente devuelve resultados sin sentido); en una medida o columna calculada no dice nada · ★ = tiene nota propia.

| Función | Cat | Ret | Aplica | Resumen | ⚑ |
|---|---|---|---|---|---|
| ABS | math-and-trig | scalar | M C T V | Returns the absolute value of a number. |  |
| ACCRINT | financial | scalar | M C T V | Returns the accrued interest for a security that pays periodic interest. |  |
| ACCRINTM | financial | scalar | M C T V | Returns the accrued interest for a security that pays interest at maturity. |  |
| ACOS | math-and-trig | scalar | M C T V | Returns the arccosine, or inverse cosine, of a number. |  |
| ACOSH | math-and-trig | scalar | M C T V | Returns the inverse hyperbolic cosine of a number. |  |
| ACOT | math-and-trig | scalar | M C T V | Returns the arccotangent, or inverse cotangent, of a number. |  |
| ACOTH | math-and-trig | scalar | M C T V | Returns the inverse hyperbolic cotangent of a number. |  |
| ADDCOLUMNS | table-manipulation | table | M C T V | Adds calculated columns to the given table or table expression. |  |
| ADDMISSINGITEMS | table-manipulation | table | M C T | Adds combinations of items from multiple columns to a table if they do not already exist. |  |
| ALL | filter | table | M C T V | Returns all the rows in a table, or all the values in a column, ignoring any filters that might have been applied. | ★ |
| ALLCROSSFILTERED | filter | scalar | M C T V | Clear all filters which are applied to a table. |  |
| ALLEXCEPT | filter | table | M C T | Removes all context filters in the table except filters that have been applied to the specified columns. | ★ |
| ALLNOBLANKROW | filter | table | M C T V | From the parent table of a relationship, returns all rows but the blank row, or all distinct values of a column but the blank row, and disregards any context filters that might exist. |  |
| ALLSELECTED | filter | scalar | M C T V | Removes context filters from columns and rows in the current query, while retaining all other context filters or explicit filters. | ★ |
| ALLSELECTEDAPPLY |  | table | M C T | Modifies how filters are applied while evaluating a GROUPCROSSAPPLY or GROUPCROSSAPPLYTABLE function. |  |
| ALLSELECTEDREMOVE |  | table | M C T | Modifies how filters are applied while evaluating a GROUPCROSSAPPLY or GROUPCROSSAPPLYTABLE function. |  |
| ALWAYSAPPLY |  | table | M C T | Modifies how filters are applied while evaluating a GROUPCROSSAPPLY or GROUPCROSSAPPLYTABLE function. |  |
| AMORDEGRC | financial | scalar | M C T V | Returns the depreciation for each accounting period. Similar to AMORLINC, except a depreciation coefficient is applied depending on the life of the assets. |  |
| AMORLINC | financial | scalar | M C T V | Returns the depreciation for each accounting period. |  |
| AND | logical | scalar | M C T V | Checks whether both arguments are `TRUE`, and returns `TRUE` if both arguments are `TRUE`. |  |
| APPROXIMATEDISTINCTCOUNT | aggregation | scalar | M C T | Returns an *estimated* count of unique values in a column. |  |
| ASIN | math-and-trig | scalar | M C T V | Returns the arcsine, or inverse sine, of a number. |  |
| ASINH | math-and-trig | scalar | M C T V | Returns the inverse hyperbolic sine of a number. |  |
| ATAN | math-and-trig | scalar | M C T V | Returns the arctangent, or inverse tangent, of a number. |  |
| ATANH | math-and-trig | scalar | M C T V | Returns the inverse hyperbolic tangent of a number. |  |
| AVERAGE | aggregation | scalar | M C T V | Returns the average (arithmetic mean) of all the numbers in a column. |  |
| AVERAGEA | aggregation | scalar | M C T V | Returns the average (arithmetic mean) of the values in a column. |  |
| AVERAGEX | aggregation | scalar | M C T V | Calculates the average (arithmetic mean) of a set of expressions evaluated over a table. | ★ |
| BETA.DIST | statistical | scalar | M C T V | Returns the beta distribution. |  |
| BETA.INV | statistical | scalar | M C T V | Returns the inverse of the beta cumulative probability density function (BETA.DIST). |  |
| BITAND | logical | scalar | M C T V | Returns a bitwise 'AND' of two numbers. |  |
| BITLSHIFT | logical | scalar | M C T V | Returns a number shifted left by the specified number of bits. |  |
| BITOR | logical | scalar | M C T V | Returns a bitwise 'OR' of two numbers. |  |
| BITRSHIFT | logical | scalar | M C T V | Returns a number shifted right by the specified number of bits. |  |
| BITXOR | logical | scalar | M C T V | Returns a bitwise 'XOR' of two numbers. |  |
| BLANK | other | scalar | M C T V | Returns a blank. | ★ |
| CALCULATE | filter | scalar | M C T V | Evaluates an expression in a modified filter context. | ★ |
| CALCULATETABLE | filter | table | M C T V | Evaluates a table expression in a modified filter context. |  |
| CALENDAR | date-and-time | table | M C T V | Returns a table with a single column named "Date" that contains a contiguous set of dates. |  |
| CALENDARAUTO | date-and-time | table | M C T V | Returns a table with a single column named "Date" that contains a contiguous set of dates. | ⛔ |
| CEILING | math-and-trig | scalar | M C T V | Rounds a number up, to the nearest integer or to the nearest multiple of significance. |  |
| CHISQ.DIST | statistical | scalar | M C T V | Returns the chi-squared distribution. |  |
| CHISQ.DIST.RT | statistical | scalar | M C T V | Returns the right-tailed probability of the chi-squared distribution. |  |
| CHISQ.INV | statistical | scalar | M C T V | Returns the inverse of the left-tailed probability of the chi-squared distribution. |  |
| CHISQ.INV.RT | statistical | scalar | M C T V | Returns the inverse of the right-tailed probability of the chi-squared distribution. |  |
| CLOSINGBALANCEMONTH | time-intelligence | scalar | M C T V | Evaluates the expression at the last date of the month in the current context. | ⛔ |
| CLOSINGBALANCEQUARTER | time-intelligence | scalar | M C T V | Evaluates the expression at the last date of the quarter in the current context. | ⛔ |
| CLOSINGBALANCEWEEK | time-intelligence | scalar | M C T V | Evaluates the expression at the last date of the week in the current context. | ⛔ |
| CLOSINGBALANCEYEAR | time-intelligence | scalar | M C T V | Evaluates the expression at the last date of the year in the current context. | ⛔ |
| COALESCE | logical | scalar | M C T V | Returns the first expression that does not evaluate to BLANK. |  |
| COLLAPSE |  | scalar | V | Retrieves a context at a higher level compared to the current context. If an expression is provided, returns its value in the new context, allowing for navigation in hierarchies and calculation at a higher level. |  |
| COLLAPSEALL |  | scalar | V | Retrieves a context at the highest level compared to the current context. If an expression is provided, returns its value in the new context, allowing for navigation in hierarchies and calculation at the highest level. |  |
| COLUMNSTATISTICS | information | table | M C T V | Returns a table of statistics regarding every column in every table in the model. | ⛔ |
| COMBIN | statistical | scalar | M C T V | Returns the number of combinations for a given number of items. |  |
| COMBINA | statistical | scalar | M C T V | Returns the number of combinations (with repetitions) for a given number of items. |  |
| COMBINEVALUES | text | scalar | M C T V | Joins two or more text strings into one text string. |  |
| CONCATENATE | text | scalar | M C T V | Joins two text strings into one text string. |  |
| CONCATENATEX | text | scalar | M C T V | Concatenates the result of an expression evaluated for each row in a table. | ★ |
| CONFIDENCE.NORM | statistical | scalar | M C T V | The confidence interval is a range of values. |  |
| CONFIDENCE.T | statistical | scalar | M C T V | Returns the confidence interval for a population mean, using a Student's t distribution. |  |
| CONTAINS | information | scalar | M C T | Returns true if values for all referred columns exist, or are contained, in those columns; otherwise, the function returns false. |  |
| CONTAINSROW | information | scalar | M C T V | Returns `TRUE` if a row of values exists or contained in a table, otherwise returns `FALSE`. |  |
| CONTAINSSTRING | information | scalar | M C T V | Returns `TRUE` or `FALSE` indicating whether one string contains another string. |  |
| CONTAINSSTRINGEXACT | information | scalar | M C T V | Returns `TRUE` or `FALSE` indicating whether one string contains another string. |  |
| CONVERT | math-and-trig | scalar | M C T V | Converts an expression of one data type to another. |  |
| COS | math-and-trig | scalar | M C T V | Returns the cosine of the given angle. |  |
| COSH | math-and-trig | scalar | M C T V | Returns the hyperbolic cosine of a number. |  |
| COT | math-and-trig | scalar | M C T V | Returns the cotangent of an angle specified in radians. |  |
| COTH | math-and-trig | scalar | M C T V | Returns the hyperbolic cotangent of a hyperbolic angle. |  |
| COUNT | aggregation | scalar | M C T V | Counts the number of rows in the specified column that contain non-blank values. Does not support Boolean values. | ★ |
| COUNTA | aggregation | scalar | M C T V | Counts the number of rows in the specified column that contain non-blank values. Supports Boolean values. |  |
| COUNTAX | aggregation | scalar | M C T V | Counts non-blank results when evaluating the result of an expression over a table. |  |
| COUNTBLANK | aggregation | scalar | M C T V | Counts the number of blank cells in a column. |  |
| COUNTROWS | aggregation | scalar | M C T V | Counts the number of rows in the specified table, or in a table defined by an expression. | ★ |
| COUNTX | aggregation | scalar | M C T V | Counts the number of rows that contain a number or an expression that evaluates to a number, when evaluating an expression over a table. |  |
| COUPDAYBS | financial | scalar | M C T V | Returns the number of days from the beginning of a coupon period until its settlement date. |  |
| COUPDAYS | financial | scalar | M C T V | Returns the number of days in the coupon period that contains the settlement date. |  |
| COUPDAYSNC | financial | scalar | M C T V | Returns the number of days from the settlement date to the next coupon date. |  |
| COUPNCD | financial | scalar | M C T V | Returns the next coupon date after the settlement date. |  |
| COUPNUM | financial | scalar | M C T V | Returns the number of coupons payable between the settlement date and maturity date, rounded up to the nearest whole coupon. |  |
| COUPPCD | financial | scalar | M C T V | Returns the previous coupon date before the settlement date. |  |
| CROSSFILTER | relationship | scalar | M C T | Specifies the cross-filtering direction to be used in a calculation for a relationship that exists between two columns. |  |
| CROSSJOIN | table-manipulation | table | M C T V | Returns a table that contains the Cartesian product of all rows from all tables in the arguments. |  |
| CUMIPMT | financial | scalar | M C T V | Returns the cumulative interest paid on a loan between start_period and end_period. |  |
| CUMPRINC | financial | scalar | M C T V | Returns the cumulative principal paid on a loan between start_period and end_period. |  |
| CURRENCY | math-and-trig | scalar | M C T V | Evaluates the argument and returns the result as currency data type. |  |
| CURRENTGROUP | table-manipulation | scalar | M C T V | Returns a set of rows from the table argument of a GROUPBY expression. | ⛔ |
| CUSTOMDATA | information | scalar | M C T V | Returns the content of the CustomData property in the connection string. |  |
| DATATABLE | table-manipulation | table | M C T V | Provides a mechanism for declaring an inline set of data values. |  |
| DATE | date-and-time | scalar | M C T V | Returns the specified date in datetime format. |  |
| DATEADD | time-intelligence | table | M C T V | Returns a table that contains a column of dates, shifted either forward or backward in time by the specified number of intervals from the dates in the current context. | ⛔★ |
| DATEDIFF | date-and-time | scalar | M C T V | Returns the number of interval boundaries between two dates. |  |
| DATESBETWEEN | time-intelligence | table | M C T V | Returns a table that contains a column of dates that begins with a specified start date and continues until a specified end date. | ⛔ |
| DATESINPERIOD | time-intelligence | table | M C T V | Returns a table that contains a column of dates that begins with a specified start date and continues for the specified number and type of date intervals. | ⛔ |
| DATESMTD | time-intelligence | table | M C T V | Returns a table that contains a column of the dates for the month to date, in the current context. | ⛔ |
| DATESQTD | time-intelligence | table | M C T V | Returns a table that contains a column of the dates for the quarter to date, in the current context. | ⛔ |
| DATESWTD | time-intelligence | table | M C T V | Returns a table that contains a column of the dates for the week to date, in the current context. | ⛔ |
| DATESYTD | time-intelligence | table | M C T V | Returns a table that contains a column of the dates for the year to date, in the current context. | ⛔★ |
| DATEVALUE | date-and-time | scalar | M C T V | Converts a date in the form of text to a date in datetime format. |  |
| DAY | date-and-time | scalar | M C T V | Returns the day of the month, a number from 1 to 31. |  |
| DB | financial | scalar | M C T V | Returns the depreciation of an asset for a specified period using the fixed-declining balance method. |  |
| DDB | financial | scalar | M C T V | Returns the depreciation of an asset for a specified period using the double-declining balance method or some other method you specify. |  |
| DEGREES | math-and-trig | scalar | M C T V | Converts radians into degrees. |  |
| DEPENDON |  | scalar | M C T | Change the table expression to be dependent on outer columns, based on the table data. |  |
| DETAILROWS | table-manipulation | table | M C T | Evaluates a Detail Rows Expression defined for a measure and returns the data. |  |
| DISC | financial | scalar | M C T V | Returns the discount rate for a security. |  |
| DISTINCT column | table-manipulation | table | M C T V | Returns a one-column table that contains the distinct values from the specified column. |  |
| DISTINCT table | table-manipulation | table | M C T V | Returns a table by removing duplicate rows from another table or expression. |  |
| DISTINCTCOUNT | aggregation | scalar | M C T V | Counts the number of distinct values in a column. |  |
| DISTINCTCOUNTNOBLANK | aggregation | scalar | M C T V | Counts the number of distinct values in a column. |  |
| DIVIDE | math-and-trig | scalar | M C T V | Performs division and returns alternate result or BLANK() on division by 0. | ★ |
| DOLLARDE | financial | scalar | M C T V | Converts a dollar price expressed as an integer part and a fraction part, such as 1.02, into a dollar price expressed as a decimal number. |  |
| DOLLARFR | financial | scalar | M C T V | Converts a dollar price expressed as an integer part and a fraction part, such as 1.02, into a dollar price expressed as a decimal number. |  |
| DURATION | financial | scalar | M C T V | Returns the Macauley duration for an assumed par value of $100. |  |
| EARLIER | filter | scalar | M C T | Returns the current value of the specified column in an outer evaluation pass of the mentioned column. | ★ |
| EARLIEST | filter | table | M C T | Returns the current value of the specified column in an outer evaluation pass of the specified column. |  |
| EDATE | date-and-time | scalar | M C T V | Returns the date that is the indicated number of months before or after the start date. |  |
| EFFECT | financial | scalar | M C T V | Returns the effective annual interest rate, given the nominal annual interest rate and the number of compounding periods per year. |  |
| ENDOFMONTH | time-intelligence | table | M C T V | Returns the last date of the month in the current context for the specified column of dates. | ⛔ |
| ENDOFQUARTER | time-intelligence | table | M C T V | Returns the last date of the quarter in the current context for the specified column of dates. | ⛔ |
| ENDOFWEEK | time-intelligence | table | M C T V | Returns the last date of the week in the current context for the specified column of dates. | ⛔ |
| ENDOFYEAR | time-intelligence | table | M C T V | Returns the last date of the year in the current context for the specified column of dates. | ⛔ |
| EOMONTH | date-and-time | scalar | M C T V | Returns the date in datetime format of the last day of the month, before or after a specified number of months. |  |
| ERROR | other | scalar | M C T V | Raises an error with an error message. |  |
| EVALUATEANDLOG | other | scalar | M C T V | Returns the value of the first argument and logs it in a DAX Evaluation Log profiler event. |  |
| EVEN | math-and-trig | scalar | M C T V | Returns number rounded up to the nearest even integer. |  |
| EXACT | text | scalar | M C T V | Compares two text strings and returns ``TRUE`` if they are exactly the same, `FALSE` otherwise. |  |
| EXCEPT | table-manipulation | table | M C T V | Returns the rows of one table which do not appear in another table. |  |
| EXP | math-and-trig | scalar | M C T V | Returns e raised to the power of a given number. |  |
| EXPAND |  | scalar | V | Retrieves a context with added levels of detail compared to the current context. If an expression is provided, returns its value in the new context, allowing for navigation in hierarchies and calculation at a more detailed level. |  |
| EXPANDALL |  | scalar | V | Retrieves a context at the most detailed level. If an expression is provided, returns its value in the new context, allowing for navigation in hierarchies and calculation at the most detailed level. |  |
| EXPON.DIST | statistical | scalar | M C T V | Returns the exponential distribution. |  |
| EXTERNALMEASURE | other | scalar | M C T | Invokes a measure defined in a remote model and returns its result. |  |
| FACT | math-and-trig | scalar | M C T V | Returns the factorial of a number, equal to the series 1*2\*3\*...\* , ending in the given number. |  |
| FALSE | logical | scalar | M C T V | Returns the logical value `FALSE`. |  |
| FILTER | filter | table | M C T V | Returns a table that represents a subset of another table or expression. | ★ |
| FILTERCLUSTER |  | table | M C T | Returns a correlated join table over a set of groups. |  |
| FILTERS | table-manipulation | scalar | M C T V | Returns a table of values directly applied as filters to `columnName`. |  |
| FIND | text | scalar | M C T V | Returns the starting position of one text string within another text string. | ★ |
| FIRST | filter | scalar | V | Used in visual calculations only. Retrieves a value in the visual matrix from the first row of an axis. |  |
| FIRSTDATE | time-intelligence | table | M C T V | Returns the first date in the current context for the specified column of dates. | ⛔ |
| FIRSTNONBLANK | filter | table | M C T V | Returns the first value in the column, `<column>`, filtered by the current context, where the expression is not blank. | ⛔ |
| FIRSTNONBLANKVALUE | filter | scalar | M C T V | Evaluates an expression filtered by the sorted values of a column and returns the first value of the expression that is not blank. | ⛔ |
| FIXED | text | scalar | M C T V | Rounds a number to the specified number of decimals and returns the result as text. |  |
| FLOOR | math-and-trig | scalar | M C T V | Rounds a number down, toward zero, to the nearest multiple of significance. |  |
| FORMAT | text | scalar | M C T V | Converts a value to text according to the specified format. | ★ |
| FV | financial | scalar | M C T V | Calculates the future value of an investment based on a constant interest rate. |  |
| GCD | math-and-trig | scalar | M C T V | Returns the greatest common divisor of two or more integers. |  |
| GENERATE | table-manipulation | table | M C T V | Returns a table with the Cartesian product between each row in *table1* and the table that results from evaluating *table2* in the context of the current row from *table1*. |  |
| GENERATEALL | table-manipulation | table | M C T V | Returns a table with the Cartesian product between each row in *table1* and the table that results from evaluating *table2* in the context of the current row from *table1*. |  |
| GENERATESERIES | table-manipulation | table | M C T V | Returns a single column table containing the values of an arithmetic series. |  |
| GEOMEAN | statistical | scalar | M C T V | Returns the geometric mean of the numbers in a column. |  |
| GEOMEANX | statistical | scalar | M C T V | Returns the geometric mean of an expression evaluated for each row in a table. |  |
| GROUPBY | table-manipulation | table | M C T V | Similar to the SUMMARIZE function, GROUPBY does not do an implicit CALCULATE for any extension columns that it adds. | ⛔ |
| GROUPCROSSAPPLY |  | table | M C T | Returns a summary table over a set of groups. |  |
| GROUPCROSSAPPLYTABLE |  | table | M C T | Returns a summary table over a set of groups. |  |
| HASONEFILTER | information | scalar | M C T V | Returns TRUE when the number of directly filtered values on `columnName` is one; otherwise returns `FALSE`. |  |
| HASONEVALUE | information | scalar | M C T V | Returns `TRUE` when the context for `columnName` has been filtered down to one distinct value only. Otherwise is `FALSE`. |  |
| HOUR | date-and-time | scalar | M C T V | Returns the hour as a number from 0 (12:00 A.M.) to 23 (11:00 P.M.). |  |
| IF | logical | scalar | M C T V | Checks a condition, and returns one value when `TRUE`, otherwise it returns a second value. |  |
| IF.EAGER | logical | scalar | M C T V | Checks a condition, and returns one value when `TRUE`, otherwise it returns a second value. Uses an *eager* execution plan which always executes the branch expressions regardless of the condition expression. |  |
| IFERROR | logical | scalar | M C T V | Evaluates an expression and returns a specified value if the expression returns an error |  |
| IGNORE | table-manipulation | scalar | M C T | Modifies SUMMARIZECOLUMNS by omitting specific expressions from the BLANK/NULL evaluation. |  |
| INDEX | filter | scalar | M C T V | Returns a row at an absolute position, specified by the position parameter, within the specified partition, sorted by the specified order or on the specified axis. |  |
| INFO.ALTERNATEOFDEFINITIONS | info | table | Q | Returns a table with information about each alternate of definition in the semantic model. This function provides metadata about alternate definitions for model objects. |  |
| INFO.ANNOTATIONS | info | table | Q | Returns a table with information about each annotation in the semantic model. This information helps you understand the model. |  |
| INFO.ATTRIBUTEHIERARCHIES | info | table | Q | Returns a table with information about each attribute hierarchy in the semantic model. This function provides metadata about the attribute hierarchies defined in the model. |  |
| INFO.ATTRIBUTEHIERARCHYSTORAGES | info | table | Q | Returns a table with information about each attribute hierarchy storage in the semantic model. This function provides metadata about the storage characteristics of attribute hierarchies. |  |
| INFO.CALCDEPENDENCY | info | table | Q | Returns a table with information about each calculation dependency in the semantic model. This information helps you understand the model. |  |
| INFO.CALCULATIONGROUPS | info | table | Q | Returns a table with information about each calculation group in the semantic model. This function provides metadata about calculation groups and their properties. |  |
| INFO.CALCULATIONITEMS | info | table | Q | Returns a table with information about each calculation item in the semantic model. This function provides metadata about calculation items within calculation groups. |  |
| INFO.CALENDARCOLUMNGROUPS | info | table | Q | Returns a table with information about each calendar column group in the semantic model. Calendar column groups associate columns with categories within a calendar. |  |
| INFO.CALENDARCOLUMNREFERENCES | info | table | Q | Returns a table with information about each calendar column reference in the semantic model. Calendar column references associate columns to calendar column groups. |  |
| INFO.CALENDARS | info | table | Q | Returns a table with information about each calendar in the semantic model. This function provides metadata about calendars defined on tables. |  |
| INFO.CATALOGS | info | table | Q | Returns a table with information about each catalog in the semantic model. This function provides metadata about the catalogs available in the current context. |  |
| INFO.CHANGEDPROPERTIES | info | table | Q | Returns a table with information about each changed property in the semantic model. This function provides metadata about properties that have been modified in the model. |  |
| INFO.COLUMNPARTITIONSTORAGES | info | table | Q | Returns a table with information about each column partition storage in the semantic model. This function provides metadata about how column partitions are stored. |  |
| INFO.COLUMNPERMISSIONS | info | table | Q | Returns a table with information about each column permission in the semantic model. This function provides metadata about column-level security settings. |  |
| INFO.COLUMNS | info | table | Q | Returns a table with information about each column in the semantic model. This function provides metadata about all columns including their properties and characteristics. |  |
| INFO.COLUMNSTORAGES | info | table | Q | Returns a table with information about each column storage in the semantic model. This function provides metadata about how columns are stored and their storage characteristics. |  |
| INFO.CSDLMETADATA | info | table | Q | Returns a table with information about the CSDL metadata in the semantic model. This function provides metadata about the Conceptual Schema Definition Language representation of the model. |  |
| INFO.CULTURES | info | table | Q | Returns a table with information about each culture in the semantic model. This function provides metadata about the cultures and locales supported by the model. |  |
| INFO.DATACOVERAGEDEFINITIONS | info | table | Q | Returns a table with information about each data coverage definition in the semantic model. This function provides metadata about data coverage settings and definitions. |  |
| INFO.DATASOURCES | info | table | Q | Returns a table with information about each data source in the semantic model. This function provides metadata about the data sources connected to the model. |  |
| INFO.DELTATABLEMETADATASTORAGES | info | table | Q | Returns a table with information about each delta table metadata storage in the semantic model. This function provides metadata about delta table storage characteristics. |  |
| INFO.DEPENDENCIES | info | table | Q | Returns a table with information about each dependency in the semantic model. This function provides metadata about object dependencies and relationships between model objects. |  |
| INFO.DETAILROWSDEFINITIONS | info | table | Q | Returns a table with information about each detail rows definition in the semantic model. This function provides metadata about detail rows definitions for measures. |  |
| INFO.DICTIONARYSTORAGES | info | table | Q | Returns a table with information about each dictionary storage in the semantic model. This function provides metadata about dictionary storage characteristics and compression. |  |
| INFO.EXCLUDEDARTIFACTS | info | table | Q | Returns a table with information about each excluded artifact in the semantic model. This function provides metadata about artifacts that are excluded from the model. |  |
| INFO.EXPRESSIONS | info | table | Q | Returns a table with information about each expression in the semantic model. This function provides metadata about expressions defined in the model. |  |
| INFO.EXTENDEDPROPERTIES | info | table | Q | Returns a table with information about each extended property in the semantic model. This function provides metadata about extended properties defined for model objects. |  |
| INFO.FORMATSTRINGDEFINITIONS | info | table | Q | Returns a table with information about each format string definition in the semantic model. This function provides metadata about format string definitions for measures and columns. |  |
| INFO.FUNCTIONS | info | table | Q | Returns information about the functions currently available for use in DAX. This corresponds to the MDSCHEMA_FUNCTIONS schema rowset, but returns only DAX (and not MDX) functions by default. |  |
| INFO.GENERALSEGMENTMAPSEGMENTMETADATASTORAGES | info | table | Q | Returns a table with information about each general segment map segment metadata storage in the semantic model. This function provides metadata about segment map storage characteristics. |  |
| INFO.GROUPBYCOLUMNS | info | table | Q | Returns a table with information about each group by column in the semantic model. This function provides metadata about columns used in group by operations. |  |
| INFO.HIERARCHIES | info | table | Q | Returns a table with information about each hierarchy in the semantic model. This function provides metadata about hierarchies and their properties. |  |
| INFO.HIERARCHYSTORAGES | info | table | Q | Returns a table with information about each hierarchy storage in the semantic model. This function provides metadata about how hierarchies are stored. |  |
| INFO.KPIS | info | table | Q | Returns a table with information about each KPI in the semantic model. This function provides metadata about Key Performance Indicators defined in the model. |  |
| INFO.LEVELS | info | table | Q | Returns a table with information about each level in the semantic model. This function provides metadata about hierarchy levels and their properties. |  |
| INFO.LINGUISTICMETADATA | info | table | Q | Returns a table with information about each linguistic metadata entry in the semantic model. This function provides metadata about linguistic metadata definitions. |  |
| INFO.MEASURES | info | table | Q | Returns a table with information about each measure in the semantic model, with columns that match the schema rowset for measure objects (for example, name, expression, and state). |  |
| INFO.MODEL | info | table | Q | Returns a table with information about the model in the semantic model. This function provides metadata about the model itself and its properties. |  |
| INFO.OBJECTTRANSLATIONS | info | table | Q | Returns a table with information about each object translation in the semantic model. This function provides metadata about translations for model objects. |  |
| INFO.PARQUETFILESTORAGES | info | table | Q | Returns a table with information about each Parquet file storage in the semantic model. This function provides metadata about Parquet file storage characteristics. |  |
| INFO.PARTITIONS | info | table | Q | Returns a table with information about each partition in the semantic model. This function provides metadata about table partitions and their properties. |  |
| INFO.PARTITIONSTORAGES | info | table | Q | Returns a table with information about each partition storage in the semantic model. This function provides metadata about how partitions are stored. |  |
| INFO.PERSPECTIVECOLUMNS | info | table | Q | Returns a table with information about each perspective column in the semantic model. This function provides metadata about columns included in perspectives. |  |
| INFO.PERSPECTIVEHIERARCHIES | info | table | Q | Returns a table with information about each perspective hierarchy in the semantic model. This function provides metadata about hierarchies included in perspectives. |  |
| INFO.PERSPECTIVEMEASURES | info | table | Q | Returns a table with information about each perspective measure in the semantic model. This function provides metadata about measures included in perspectives. |  |
| INFO.PERSPECTIVES | info | table | Q | Returns a table with information about each perspective in the semantic model. This function provides metadata about perspectives defined in the model. |  |
| INFO.PERSPECTIVETABLES | info | table | Q | Returns a table with information about each perspective table in the semantic model. This function provides metadata about tables included in perspectives. |  |
| INFO.PROPERTIES | info | table | Q | Returns a table with information about each property in the semantic model. This function provides metadata about properties defined for model objects. |  |
| INFO.QUERYGROUPS | info | table | Q | Returns a table with information about each query group in the semantic model. This function provides metadata about query groups defined in the model. |  |
| INFO.REFRESHPOLICIES | info | table | Q | Returns a table with information about each refresh policy in the semantic model. This function provides metadata about refresh policies defined for tables. |  |
| INFO.RELATEDCOLUMNDETAILS | info | table | Q | Returns a table with information about each related column detail in the semantic model. This function provides metadata about related column details for relationships. |  |
| INFO.RELATIONSHIPINDEXSTORAGES | info | table | Q | Returns a table with information about each relationship index storage in the semantic model. This function provides metadata about relationship index storage characteristics. |  |
| INFO.RELATIONSHIPS | info | table | Q | Returns a table with information about each relationship in the semantic model. This function provides metadata about relationships between tables. |  |
| INFO.RELATIONSHIPSTORAGES | info | table | Q | Returns a table with information about each relationship storage in the semantic model. This function provides metadata about how relationships are stored. |  |
| INFO.ROLEMEMBERSHIPS | info | table | Q | Returns a table with information about each role membership in the semantic model. This function provides metadata about role memberships and security settings. |  |
| INFO.ROLES | info | table | Q | Returns a table with information about each role in the semantic model. This function provides metadata about security roles defined in the model. |  |
| INFO.SEGMENTMAPSTORAGES | info | table | Q | Returns a table with information about each segment map storage in the semantic model. This function provides metadata about segment map storage characteristics. |  |
| INFO.SEGMENTSTORAGES | info | table | Q | Returns a table with information about each segment storage in the semantic model. This function provides metadata about segment storage characteristics. |  |
| INFO.STORAGEFILES | info | table | Q | Returns a table with information about each storage file in the semantic model. This function provides metadata about storage files and their characteristics. |  |
| INFO.STORAGEFOLDERS | info | table | Q | Returns a table with information about all table storage in the semantic model. This information helps you understand the model. |  |
| INFO.STORAGETABLECOLUMNS | info | table | Q | Returns a table with information about all table storage in the semantic model. This information helps you understand the model. |  |
| INFO.STORAGETABLECOLUMNSEGMENTS | info | table | Q | Returns a table with information about all table storage in the semantic model. This information helps you understand the model. |  |
| INFO.STORAGETABLES | info | table | Q | Returns a table with information about all table storage in the semantic model. This information helps you understand the model. |  |
| INFO.TABLEPERMISSIONS | info | table | Q | Returns a table with information about all table storage in the semantic model. This information helps you understand the model. |  |
| INFO.TABLES | info | table | Q | Returns a table with information about each table in the semantic model, with columns that match the schema rowset for table objects (for example, name, description, and visibility). |  |
| INFO.TABLESTORAGES | info | table | Q | Returns a table with information about all table storage in the semantic model. This information helps you understand the model. |  |
| INFO.USERDEFINEDFUNCTIONS | info | table | Q | Returns a table with information about each user-defined function in the semantic model, with columns that match the schema rowset for user-defined function objects (for example, name, expression, and state). |  |
| INFO.VARIATIONS | info | table | Q | Returns a table with information about all variations in the semantic model. This information helps you understand the model. |  |
| INFO.VIEW.COLUMNS | info | table | M C T V | Returns a table with information about each column in the semantic model, such as name, description, and format string. This information helps you understand the model and to self-document the model when used in calculated tables. |  |
| INFO.VIEW.MEASURES | info | table | M C T V | Returns a table with information about each measure in the semantic model, such as name, description, and DAX formula. This information helps you understand the model and to self-document the model when used in calculated tables. |  |
| INFO.VIEW.RELATIONSHIPS | info | table | M C T V | Returns a table with information about each [relationship](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-create-and-manage-relationships) in the semantic model, such as name, cardinality, and cross-filtering behavior. This information helps you understand the model and to self-document the model when used in calculated tables. |  |
| INFO.VIEW.TABLES | info | table | M C T V | Returns a table with information about each table in the semantic model, such as table name, description, and storage mode. This information helps you understand the model and to self-document the model when used in calculated tables. |  |
| INT | math-and-trig | scalar | M C T V | Rounds a number down to the nearest integer. |  |
| INTERSECT | table-manipulation | table | M C T V | Returns the row intersection of two tables, retaining duplicates. |  |
| INTRATE | financial | scalar | M C T V | Returns the interest rate for a fully invested security. |  |
| IPMT | financial | scalar | M C T V | Returns the interest payment for a given period for an investment based on periodic, constant payments and a constant interest rate. |  |
| ISAFTER | information | scalar | M C T V | A boolean function that emulates the behavior of a Start At clause and returns true for a row that meets all of the condition parameters. |  |
| ISATLEVEL |  | scalar | V | Reports whether the column is present at the current level. |  |
| ISBLANK | information | scalar | M C T V | Checks whether a value is blank, and returns `TRUE` or `FALSE`. |  |
| ISBOOLEAN | information | scalar | M C T V | Checks whether a value is a logical value, (`TRUE` or `FALSE`), and returns `TRUE` or `FALSE`. Alias of [ISLOGICAL](https://learn.microsoft.com/en-us/dax/islogical-function-dax). |  |
| ISCROSSFILTERED | information | scalar | M C T V | Returns `TRUE` when `columnName` or another column in the same or related table is being filtered. |  |
| ISCURRENCY | information | scalar | M C T V | Checks whether a value is a decimal number, and returns `TRUE` or `FALSE`. Alias of [ISDECIMAL](https://learn.microsoft.com/en-us/dax/isdecimal-function-dax). |  |
| ISDATETIME | information | scalar | M C T V | Checks whether a value is a date / time, and returns `TRUE` or `FALSE`. |  |
| ISDECIMAL | information | scalar | M C T V | Checks whether a value is a decimal number, and returns `TRUE` or `FALSE`. Alias of [ISCURRENCY](https://learn.microsoft.com/en-us/dax/iscurrency-function-dax). |  |
| ISDOUBLE | information | scalar | M C T V | Checks whether a value is a floating-point number, and returns `TRUE` or `FALSE`. |  |
| ISEMPTY | information | scalar | M C T V | Checks if a table is empty. |  |
| ISERROR | information | scalar | M C T V | Checks whether a value is an error, and returns `TRUE` or `FALSE`. |  |
| ISEVEN | information | scalar | M C T V | Returns `TRUE` if number is even, or `FALSE` if number is odd. |  |
| ISFILTERED | information | scalar | M C T V | Returns `TRUE` when `columnName` is being filtered directly. |  |
| ISINSCOPE | information | scalar | M C T V | Returns true when the specified column is the level in a hierarchy of levels. |  |
| ISINT64 | information | scalar | M C T V | Checks whether a value is a whole number, and returns `TRUE` or `FALSE`. Alias of [ISINTEGER](https://learn.microsoft.com/en-us/dax/isinteger-function-dax). |  |
| ISINTEGER | information | scalar | M C T V | Checks whether a value is a whole number, and returns `TRUE` or `FALSE`. Alias of [ISINT64](https://learn.microsoft.com/en-us/dax/isint64-function-dax). |  |
| ISLOGICAL | information | scalar | M C T V | Checks whether a value is a logical value, (`TRUE` or `FALSE`), and returns `TRUE` or `FALSE`. Alias of [ISBOOLEAN](https://learn.microsoft.com/en-us/dax/isboolean-function-dax). |  |
| ISNONTEXT | information | scalar | M C T V | Checks if a value is not text (blank cells are not text), and returns `TRUE` or `FALSE`. |  |
| ISNUMBER | information | scalar | M C T V | Checks whether a value is a number, and returns `TRUE` or `FALSE`. Alias of [ISNUMERIC](https://learn.microsoft.com/en-us/dax/isnumeric-function-dax). |  |
| ISNUMERIC | information | scalar | M C T V | Checks whether a value is a number, and returns `TRUE` or `FALSE`. Alias of [ISNUMBER](https://learn.microsoft.com/en-us/dax/isnumber-function-dax). |  |
| ISO.CEILING | math-and-trig | scalar | M C T V | Rounds a number up, to the nearest integer or to the nearest multiple of significance. |  |
| ISODD | information | scalar | M C T V | Returns `TRUE` if number is odd, or `FALSE` if number is even. |  |
| ISONORAFTER | information | scalar | M C T V | A boolean function that emulates the behavior of a Start At clause and returns true for a row that meets all of the condition parameters. |  |
| ISPMT | financial | scalar | M C T V | Calculates the interest paid (or received) for the specified period of a loan (or investment) with even principal payments. |  |
| ISSELECTEDMEASURE | information | scalar | M C T | Used by expressions for calculation items to determine the measure that is in context is one of those specified in a list of measures. |  |
| ISSTRING | information | scalar | M C T V | Checks if a value is text, and returns `TRUE` or `FALSE`. Alias of [ISTEXT](https://learn.microsoft.com/en-us/dax/istext-function-dax). |  |
| ISSUBTOTAL | information | scalar | M C T | Creates another column in a SUMMARIZE expression that returns True if the row contains subtotal values for the column given as argument, otherwise returns False. |  |
| ISTEXT | information | scalar | M C T V | Checks if a value is text, and returns `TRUE` or `FALSE`. Alias of [ISSTRING](https://learn.microsoft.com/en-us/dax/isstring-function-dax). |  |
| KEEPFILTERS | filter | table | M C T V | Modifies how filters are applied while evaluating a CALCULATE or CALCULATETABLE function. | ★ |
| LAST | filter | scalar | V | Used in visual calculations only. Retrieves a value in the visual matrix from the last row of an axis. |  |
| LASTDATE | time-intelligence | table | M C T V | Returns the last date in the current context for the specified column of dates. | ⛔ |
| LASTNONBLANK | filter | table | M C T V | Returns the last value in the column, `column`, filtered by the current context, where the expression is not blank. | ⛔ |
| LASTNONBLANKVALUE | filter | scalar | M C T V | Evaluates an expression filtered by the sorted values of a column and returns the last value of the expression that is not blank. | ⛔ |
| LCM | math-and-trig | scalar | M C T V | Returns the least common multiple of integers. |  |
| LEFT | text | scalar | M C T V | Returns the specified number of characters from the start of a text string. |  |
| LEN | text | scalar | M C T V | Returns the number of characters in a text string. |  |
| LINEST | statistical | scalar | M C T V | Uses the Least Squares method to calculate a straight line that best fits the given data. |  |
| LINESTX | statistical | scalar | M C T V | Uses the Least Squares method to calculate a straight line that best fits the given data. The data result from expressions evaluated for each row in a table. |  |
| LN | math-and-trig | scalar | M C T V | Returns the natural logarithm of a number. |  |
| LOG | math-and-trig | scalar | M C T V | Returns the logarithm of a number to the base you specify. |  |
| LOG10 | math-and-trig | scalar | M C T V | Returns the base-10 logarithm of a number. |  |
| LOOKUP | filter | scalar | V | In visual calculation mode only. Look up the value when filters applied. |  |
| LOOKUPVALUE | filter | scalar | M C T | Returns the value for the row that meets all criteria specified by search conditions. The function can apply one or more search conditions. | ★ |
| LOOKUPWITHTOTALS | filter | scalar | V | In visual calculation mode only. Look up the value when filters applied. Filters not specified will not be inferred. |  |
| LOWER | text | scalar | M C T V | Converts all letters in a text string to lowercase. |  |
| MATCHBY | filter | scalar | M C T V | In window functions, defines the columns that are used to determine how to match data and identify the *current row*. |  |
| MAX | aggregation | scalar | M C T V | Returns the largest numeric value in a column, or between two scalar expressions. |  |
| MAXA | aggregation | scalar | M C T V | Returns the largest value in a column. |  |
| MAXX | aggregation | scalar | M C T V | Evaluates an expression for each row of a table and returns the largest numeric value. | ★ |
| MDURATION | financial | scalar | M C T V | Returns the modified Macauley duration for a security with an assumed par value of $100. |  |
| MEDIAN | statistical | scalar | M C T V | Returns the median of numbers in a column. |  |
| MEDIANX | statistical | scalar | M C T V | Returns the median number of an expression evaluated for each row in a table. |  |
| MID | text | scalar | M C T V | Returns a string of characters from the middle of a text string, given a starting position and length. |  |
| MIN | aggregation | scalar | M C T V | Returns the smallest numeric value in a column, or between two scalar expressions. |  |
| MINA | aggregation | scalar | M C T V | Returns the smallest value in a column, including any logical values and numbers represented as text. |  |
| MINUTE | date-and-time | scalar | M C T V | Returns the minute as a number from 0 to 59, given a date and time value. |  |
| MINX | aggregation | scalar | M C T V | Returns the smallest numeric value that results from evaluating an expression for each row of a table. |  |
| MOD | math-and-trig | scalar | M C T V | Returns the remainder after a number is divided by a divisor. The result always has the same sign as the divisor. |  |
| MONTH | date-and-time | scalar | M C T V | Returns the month as a number from 1 (January) to 12 (December). |  |
| MOVINGAVERAGE | filter | scalar | V | Returns a moving average calculated along the given axis of the visual matrix. |  |
| MROUND | math-and-trig | scalar | M C T V | Returns a number rounded to the desired multiple. |  |
| NAMEOF | information | scalar | M C T V | Returns the name of a table, column, measure, or calendar as a text string. |  |
| NATURALINNERJOIN | table-manipulation | table | M C T V | Performs an inner join of a table with another table. |  |
| NATURALLEFTOUTERJOIN | table-manipulation | table | M C T V | Performs a join of the LeftTable with the RightTable. |  |
| NETWORKDAYS | date-and-time | scalar | M C T V | Returns the number of whole workdays between two dates. |  |
| NEXT | filter | scalar | V | Used in visual calculations only. Retrieves a value in the next row of an axis in the visual matrix. |  |
| NEXTDAY | time-intelligence | table | M C T V | Returns a table that contains a column of all dates from the next day, based on the last date specified in the dates column in the current context. | ⛔ |
| NEXTMONTH | time-intelligence | table | M C T V | Returns a table that contains a column of all dates from the next month, based on the last date in the dates column in the current context. | ⛔ |
| NEXTQUARTER | time-intelligence | table | M C T V | Returns a table that contains a column of all dates in the next quarter, based on the last date specified in the dates column, in the current context. | ⛔ |
| NEXTWEEK | time-intelligence | table | M C T V | Returns a table that contains a column of all dates from the next week, based on the last date in the dates column in the current context. | ⛔ |
| NEXTYEAR | time-intelligence | table | M C T V | Returns a table that contains a column of all dates in the next year, based on the last date in the dates column, in the current context. | ⛔ |
| NOMINAL | financial | scalar | M C T V | Returns the nominal annual interest rate, given the effective rate and the number of compounding periods per year. |  |
| NONFILTER |  | table | M C T | Modifies how filters are applied while evaluating a GROUPCROSSAPPLY or GROUPCROSSAPPLYTABLE function. |  |
| NONVISUAL | information | table | M C T | Marks a value filter in a SUMMARIZECOLUMNS expression as non-visual. |  |
| NORM.DIST | statistical | scalar | M C T V | Returns the normal distribution for the specified mean and standard deviation. |  |
| NORM.INV | statistical | scalar | M C T V | The inverse of the normal cumulative distribution for the specified mean and standard deviation. |  |
| NORM.S.DIST | statistical | scalar | M C T V | Returns the standard normal distribution (has a mean of zero and a standard deviation of one). |  |
| NORM.S.INV | statistical | scalar | M C T V | Returns the inverse of the standard normal cumulative distribution. |  |
| NOT | logical | scalar | M C T V | Changes `FALSE` to `TRUE`, or `TRUE` to `FALSE`. |  |
| NOW | date-and-time | scalar | M C T V | Returns the current date and time in datetime format. |  |
| NPER | financial | scalar | M C T V | Returns the number of periods for an investment based on periodic, constant payments and a constant interest rate. |  |
| ODD | math-and-trig | scalar | M C T V | Returns number rounded up to the nearest odd integer. |  |
| ODDFPRICE | financial | scalar | M C T V | Returns the price per \$100 face value of a security having an odd (short or long) first period. |  |
| ODDFYIELD | financial | scalar | M C T V | Returns the yield of a security that has an odd (short or long) first period. |  |
| ODDLPRICE | financial | scalar | M C T V | Returns the price per $100 face value of a security having an odd (short or long) last coupon period. |  |
| ODDLYIELD | financial | scalar | M C T V | Returns the yield of a security that has an odd (short or long) last period. |  |
| OFFSET | filter | scalar | M C T V | Returns a single row that is positioned either before or after the *current row* within the same table, by a given offset. |  |
| OPENINGBALANCEMONTH | time-intelligence | scalar | M C T V | Evaluates the expression at the first date of the month in the current context. | ⛔ |
| OPENINGBALANCEQUARTER | time-intelligence | scalar | M C T V | Evaluates the expression at the first date of the quarter, in the current context. | ⛔ |
| OPENINGBALANCEWEEK | time-intelligence | scalar | M C T V | Evaluates the expression at the first date of the week in the current context. | ⛔ |
| OPENINGBALANCEYEAR | time-intelligence | scalar | M C T V | Evaluates the expression at the first date of the year in the current context. | ⛔ |
| OR | logical | scalar | M C T V | Checks whether one of the arguments is `TRUE` to return `TRUE`. |  |
| ORDERBY | filter | scalar | M C T V | Defines the columns that determine the sort order within each of a window function’s partitions. |  |
| PARALLELPERIOD | time-intelligence | table | M C T V | Returns a table that contains a column of dates that represents a period parallel to the dates in the specified dates column, in the current context, with the dates shifted a number of intervals either forward in time or back in time. | ⛔ |
| PARTITIONBY | filter | scalar | M C T V | Defines the columns that are used to partition a window function’s `relation` parameter. |  |
| PATH | parent-and-child | scalar | M C T V | Returns a delimited text string with the identifiers of all the parents of the current identifier. |  |
| PATHCONTAINS | parent-and-child | scalar | M C T V | Returns `TRUE` if the specified `item` exists within the specified `path`. |  |
| PATHITEM | parent-and-child | scalar | M C T V | Returns the item at the specified `position` from a string resulting from evaluation of a PATH function. |  |
| PATHITEMREVERSE | parent-and-child | scalar | M C T V | Returns the item at the specified `position` from a string resulting from evaluation of a PATH function. |  |
| PATHLENGTH | parent-and-child | scalar | M C T V | Returns the number of parents to the specified item in a given PATH result, including self. |  |
| PDURATION | financial | scalar | M C T V | Returns the number of periods required by an investment to reach a specified value. |  |
| PERCENTILE.EXC | statistical | scalar | M C T V | Returns the k-th percentile of values in a range, where k is in the range 0..1, exclusive. |  |
| PERCENTILE.INC | statistical | scalar | M C T V | Returns the k-th percentile of values in a range, where k is in the range 0..1, inclusive. |  |
| PERCENTILEX.EXC | statistical | scalar | M C T V | Returns the percentile number of an expression evaluated for each row in a table. |  |
| PERCENTILEX.INC | statistical | scalar | M C T V | Returns the percentile number of an expression evaluated for each row in a table. |  |
| PERMUT | statistical | scalar | M C T V | Returns the number of permutations for a given number of objects that can be selected from number objects. |  |
| PI | math-and-trig | scalar | M C T V | Returns the value of Pi, 3.14159265358979, accurate to 15 digits. |  |
| PMT | financial | scalar | M C T V | Calculates the payment for a loan based on constant payments and a constant interest rate. |  |
| POISSON.DIST | statistical | scalar | M C T V | Returns the Poisson distribution. |  |
| POWER | math-and-trig | scalar | M C T V | Returns the result of a number raised to a power. |  |
| PPMT | financial | scalar | M C T V | Returns the payment on the principal for a given period for an investment based on periodic, constant payments and a constant interest rate. |  |
| PREVIOUS | filter | scalar | V | Used in visual calculations only. Retrieves a value in the previous row of an axis in the visual matrix. |  |
| PREVIOUSDAY | time-intelligence | table | M C T V | Returns a table that contains a column of all dates representing the day that is previous to the first date in the dates column, in the current context. | ⛔ |
| PREVIOUSMONTH | time-intelligence | table | M C T V | Returns a table that contains a column of all dates from the previous month, based on the first date in the dates column, in the current context. | ⛔★ |
| PREVIOUSQUARTER | time-intelligence | table | M C T V | Returns a table that contains a column of all dates from the previous quarter, based on the first date in the dates column, in the current context. | ⛔ |
| PREVIOUSWEEK | time-intelligence | table | M C T V | Returns a table that contains a column of all dates representing the week that is previous to the first date in the dates column, in the current context. | ⛔ |
| PREVIOUSYEAR | time-intelligence | table | M C T V | Returns a table that contains a column of all dates from the previous year, based on the first date in the dates column, in the current context. | ⛔ |
| PRICE | financial | scalar | M C T V | Returns the price per \$100 face value of a security that pays periodic interest. |  |
| PRICEDISC | financial | scalar | M C T V | Returns the price per \$100 face value of a discounted security. |  |
| PRICEMAT | financial | scalar | M C T V | Returns the price per $100 face value of a security that pays interest at maturity. |  |
| PRODUCT | aggregation | scalar | M C T V | Returns the product of the numbers in a column. |  |
| PRODUCTX | aggregation | scalar | M C T V | Returns the product of an expression evaluated for each row in a table. |  |
| PV | financial | scalar | M C T V | Calculates the present value of a loan or an investment, based on a constant interest rate. |  |
| QUARTER | date-and-time | scalar | M C T V | Returns the quarter as a number from 1 to 4. |  |
| QUOTIENT | math-and-trig | scalar | M C T V | Performs division and returns only the integer portion of the division result. |  |
| RADIANS | math-and-trig | scalar | M C T V | Converts degrees to radians. |  |
| RAND | math-and-trig | scalar | M C T V | Returns a random number greater than or equal to 0 and less than 1, evenly distributed. |  |
| RANDBETWEEN | math-and-trig | scalar | M C T V | Returns a random number in the range between two numbers you specify. |  |
| RANGE | filter | scalar | V | Returns an interval of rows within the given axis, relative to the current row. A shortcut for WINDOW. |  |
| RANK | filter | scalar | M C T V | Returns the ranking of a row within the given interval. |  |
| RANK.EQ | statistical | scalar | M C T V | Returns the ranking of a number in a list of numbers. |  |
| RANKX | statistical | scalar | M C T V | Returns the ranking of a number in a list of numbers for each row in the `table` argument. | ★ |
| RATE | financial | scalar | M C T V | Returns the interest rate per period of an annuity. |  |
| RECEIVED | financial | scalar | M C T V | Returns the amount received at maturity for a fully invested security. |  |
| RELATED | relationship | scalar | M C T | Returns a related value from another table. | ★ |
| RELATEDTABLE | relationship | table | M C T | Evaluates a table expression in a context modified by the given filters. | ★ |
| REMOVEFILTERS | filter | scalar | M C T V | Clears filters from the specified tables or columns. | ★ |
| REPLACE | text | scalar | M C T V | REPLACE replaces part of a text string, based on the number of characters you specify, with a different text string. |  |
| REPT | text | scalar | M C T V | Repeats text a given number of times. |  |
| RIGHT | text | scalar | M C T V | RIGHT returns the last character or characters in a text string, based on the number of characters you specify. |  |
| ROLLUP | table-manipulation | scalar | M C T | Modifies the behavior of SUMMARIZE by adding rollup rows to the result on columns defined by the groupBy_columnName parameter. |  |
| ROLLUPADDISSUBTOTAL | table-manipulation | scalar | M C T | Modifies the behavior of SUMMARIZECOLUMNS by adding rollup/subtotal rows to the result based on the groupBy_columnName columns. |  |
| ROLLUPGROUP | table-manipulation | scalar | M C T | Modifies the behavior of SUMMARIZE and SUMMARIZECOLUMNS by adding rollup rows to the result on columns defined by the the groupBy_columnName parameter. |  |
| ROLLUPISSUBTOTAL | table-manipulation | scalar | M C T | Pairs rollup groups with the column added by ROLLUPADDISSUBTOTAL within an ADDMISSINGITEMS expression. |  |
| ROUND | math-and-trig | scalar | M C T V | Rounds a number to the specified number of digits. |  |
| ROUNDDOWN | math-and-trig | scalar | M C T V | Rounds a number down, toward zero. |  |
| ROUNDUP | math-and-trig | scalar | M C T V | Rounds a number up, away from 0 (zero). |  |
| ROW | table-manipulation | scalar | M C T V | Returns a table with a single row containing values that result from the expressions given to each column. |  |
| ROWNUMBER | filter | scalar | M C T V | Returns the unique ranking of a row within the given interval. |  |
| RRI | financial | scalar | M C T V | Returns an equivalent interest rate for the growth of an investment. |  |
| RUNNINGSUM | filter | scalar | V | Returns a running sum calculated along the given axis of the visual matrix. |  |
| SAMEPERIODLASTYEAR | time-intelligence | scalar | M C T V | Returns a table that contains a column of dates shifted one year back in time from the dates in the specified dates column, in the current context. | ⛔★ |
| SAMPLE | statistical | table | M C T V | Returns a sample of N rows from the specified table. |  |
| SAMPLEAXISWITHLOCALMINMAX |  | scalar | M C T V | Returns a sample subset from a Table that is obtained by binning the primary X-axis into equal-sized bins and preserving the local min/max for each bin across different series. |  |
| SAMPLECARTESIANPOINTSBYCOVER | statistical | scalar | M C T V | Returns a sample subset from a Table that is obtained by plotting the rows as points in 2D space and removing overlapping points. |  |
| SEARCH | text | scalar | M C T V | Returns the number of the character at which a specific character or text string is first found, reading left to right. | ★ |
| SECOND | date-and-time | scalar | M C T V | Returns the seconds of a time value, as a number from 0 to 59. |  |
| SELECTCOLUMNS | table-manipulation | table | M C T V | Adds calculated columns to the given table or table expression. |  |
| SELECTEDMEASURE | information | scalar | M C T | Used by expressions for calculation items to reference the measure that is in context. |  |
| SELECTEDMEASUREFORMATSTRING | information | scalar | M C T | Used by expressions for calculation items to retrieve the format string of the measure that is in context. |  |
| SELECTEDMEASURENAME | information | scalar | M C T | Used by expressions for calculation items to determine the measure that is in context by name. |  |
| SELECTEDVALUE | filter | scalar | M C T V | Returns the value when the context for columnName has been filtered down to one distinct value only. Otherwise returns alternateResult. | ★ |
| SHADOWCLUSTER |  | table | M C T | Modifies how filters are applied while evaluating a GROUPCROSSAPPLY or GROUPCROSSAPPLYTABLE function. |  |
| SIGN | math-and-trig | scalar | M C T V | Determines the sign of a number, the result of a calculation, or a value in a column. |  |
| SIN | math-and-trig | scalar | M C T V | Returns the sine of the given angle. |  |
| SINH | math-and-trig | scalar | M C T V | Returns the hyperbolic sine of a number. |  |
| SLN | financial | scalar | M C T V | Returns the straight-line depreciation of an asset for one period. |  |
| SQRT | math-and-trig | scalar | M C T V | Returns the square root of a number. |  |
| SQRTPI | math-and-trig | scalar | M C T V | Returns the square root of (number * pi). |  |
| STARTOFMONTH | time-intelligence | table | M C T V | Returns the first date of the month in the current context for the specified column of dates. | ⛔ |
| STARTOFQUARTER | time-intelligence | table | M C T V | Returns the first date of the quarter in the current context for the specified column of dates. | ⛔ |
| STARTOFWEEK | time-intelligence | table | M C T V | Returns the first date of the week in the current context for the specified column of dates. | ⛔ |
| STARTOFYEAR | time-intelligence | table | M C T V | Returns the first date of the year in the current context for the specified column of dates. | ⛔ |
| STDEV.P | statistical | scalar | M C T V | Returns the standard deviation of the entire population. |  |
| STDEV.S | statistical | scalar | M C T V | Returns the standard deviation of a sample population. |  |
| STDEVX.P | statistical | scalar | M C T V | Returns the standard deviation of the entire population. |  |
| STDEVX.S | statistical | scalar | M C T V | Returns the standard deviation of a sample population. |  |
| SUBSTITUTE | text | scalar | M C T V | Replaces existing text with new text in a text string. |  |
| SUBSTITUTEWITHINDEX | table-manipulation | table | M C T | Returns a table which represents a left semijoin of the two tables supplied as arguments. |  |
| SUM | aggregation | scalar | M C T V | Adds all the numbers in a column. |  |
| SUMMARIZE | table-manipulation | table | M C T V | Returns a summary table for the requested totals over a set of groups. |  |
| SUMMARIZECOLUMNS | table-manipulation | table | M C T | Returns a summary table over a set of groups. |  |
| SUMX | aggregation | scalar | M C T V | Returns the sum of an expression evaluated for each row in a table. | ★ |
| SWITCH | logical | scalar | M C T V | Evaluates an expression against a list of values and returns one of multiple possible result expressions. |  |
| SYD | financial | scalar | M C T V | Returns the sum-of-years' digits depreciation of an asset for a specified period. |  |
| T.DIST | statistical | scalar | M C T V | Returns the Student's left-tailed t-distribution. |  |
| T.DIST.2T | statistical | scalar | M C T V | Returns the two-tailed Student's t-distribution. |  |
| T.DIST.RT | statistical | scalar | M C T V | Returns the right-tailed Student's t-distribution. |  |
| T.INV | statistical | scalar | M C T V | Returns the left-tailed inverse of the Student's t-distribution. |  |
| T.INV.2t | statistical | scalar | M C T V | Returns the two-tailed inverse of the Student's t-distribution. |  |
| TABLEOF | information | table | M C T | Returns a reference to the table associated with a specified column, measure, or calendar. |  |
| TAN | math-and-trig | scalar | M C T V | Returns the tangent of the given angle. |  |
| TANH | math-and-trig | scalar | M C T V | Returns the hyperbolic tangent of a number. |  |
| TBILLEQ | financial | scalar | M C T V | Returns the bond-equivalent yield for a Treasury bill. |  |
| TBILLPRICE | financial | scalar | M C T V | Returns the price per $100 face value for a Treasury bill. |  |
| TBILLYIELD | financial | scalar | M C T V | Returns the yield for a Treasury bill. |  |
| TIME | date-and-time | scalar | M C T V | Converts hours, minutes, and seconds given as numbers to a time in datetime format. |  |
| TIMEVALUE | date-and-time | scalar | M C T V | Converts a time in text format to a time in datetime format. |  |
| TOCSV | other | scalar | M C T V | Returns a table as a string in CSV format. |  |
| TODAY | date-and-time | scalar | M C T V | Returns the current date. |  |
| TOJSON | other | scalar | M C T V | Returns a table as a string in JSON format. |  |
| TOPN | table-manipulation | table | M C T V | Returns the top N rows of the specified table. | ★ |
| TOPNSKIP |  | table | M C T V | Returns the top N rows of the specified table, skipping a number of rows. |  |
| TOTALMTD | time-intelligence | scalar | M C T V | Evaluates the value of the expression for the month to date, in the current context. | ⛔ |
| TOTALQTD | time-intelligence | scalar | M C T V | Evaluates the value of the expression for the dates in the quarter to date, in the current context. | ⛔ |
| TOTALWTD | time-intelligence | scalar | M C T V | Evaluates the value of the expression for the week to date, in the current context. | ⛔ |
| TOTALYTD | time-intelligence | scalar | M C T V | Evaluates the year-to-date value of the expression in the current context. | ⛔ |
| TREATAS | table-manipulation | table | M C T V | Applies the result of a table expression as filters to columns from an unrelated table. |  |
| TRIM | text | scalar | M C T V | Removes all spaces from text except for single spaces between words. |  |
| TRUE | logical | scalar | M C T V | Returns the logical value `TRUE`. |  |
| TRUNC | math-and-trig | scalar | M C T V | Truncates a number to an integer by removing the decimal, or fractional, part of the number. |  |
| UNICHAR | text | scalar | M C T V | Returns the Unicode character referenced by the numeric value. |  |
| UNICODE | text | scalar | M C T V | Returns the numeric code corresponding to the first character of the text string. |  |
| UNION | table-manipulation | table | M C T V | Creates a union (join) table from a pair of tables. |  |
| UPPER | text | scalar | M C T V | Converts a text string to all uppercase letters. |  |
| USERCULTURE | information | scalar | M C T V | Returns the locale for the current user. |  |
| USERELATIONSHIP | relationship | scalar | M C T | Specifies the relationship to be used in a specific calculation as the one that exists between columnName1 and columnName2. |  |
| USERNAME | information | scalar | M C T V | Returns the domain name and username from the credentials given to the system at connection time. |  |
| USEROBJECTID | information | scalar | M C T V | Returns the current user's Object ID or SID. |  |
| USERPRINCIPALNAME | information | scalar | M C T V | Returns the user principal name. |  |
| UTCNOW | date-and-time | scalar | M C T V | Returns the current UTC date and time |  |
| UTCTODAY | date-and-time | scalar | M C T V | Returns the current UTC date. |  |
| VALUE | text | scalar | M C T V | Converts a text string that represents a number to a number. |  |
| VALUES | table-manipulation | table | M C T V | Returns a one-column table that contains the distinct values from the specified table or column. | ★ |
| VAR.P | statistical | scalar | M C T V | Returns the variance of the entire population. |  |
| VAR.S | statistical | scalar | M C T V | Returns the variance of a sample population. |  |
| VARX.P | statistical | scalar | M C T V | Returns the variance of the entire population. |  |
| VARX.S | statistical | scalar | M C T V | Returns the variance of a sample population. |  |
| VDB | financial | scalar | M C T V | Returns the depreciation of an asset for any period you specify, including partial periods, using the double-declining balance method or some other method you specify. |  |
| WEEKDAY | date-and-time | scalar | M C T V | Returns a number from 1 to 7 identifying the day of the week of a date. |  |
| WEEKNUM | date-and-time | scalar | M C T V | Returns the week number for the given date and year according to the return_type value. |  |
| WINDOW | filter | scalar | M C T V | Returns multiple rows which are positioned within the given interval. |  |
| XIRR | financial | scalar | M C T V | Returns the internal rate of return for a schedule of cash flows that is not necessarily periodic. |  |
| XNPV | financial | scalar | M C T V | Returns the present value for a schedule of cash flows that is not necessarily periodic. |  |
| YEAR | date-and-time | scalar | M C T V | Returns the year of a date as a four digit integer in the range 1900-9999. |  |
| YEARFRAC | date-and-time | scalar | M C T V | Calculates the fraction of the year represented by the number of whole days between two dates. |  |
| YIELD | financial | scalar | M C T V | Returns the yield on a security that pays periodic interest. |  |
| YIELDDISC | financial | scalar | M C T V | Returns the annual yield for a discounted security. |  |
| YIELDMAT | financial | scalar | M C T V | Returns the annual yield of a security that pays interest at maturity. |  |
