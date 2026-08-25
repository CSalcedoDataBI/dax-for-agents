---
title: New DAX functions
topic: whats-new
summary: "Learn more about: New DAX functions"
source: query-languages/dax/new-dax-functions.md@323524c
sourceDate: 
---
# New DAX functions

DAX is continuously being improved with new functions and functionality to support new features. New functions and updates are included in service, application, and tool updates which in most cases are monthly.

While functions and functionality are being updated all the time, only those updates that have a visible and functional change exposed to users are described in documentation. New functions and updates to existing functions within the past year are shown here.

> [!IMPORTANT]
> Not all functions are supported in all versions of Power BI Desktop, Analysis Services, and Power Pivot in Excel. New and updated functions are typically first introduced in Power BI Desktop, and then later in Analysis Services, Power Pivot in Excel, and tools.

## New functions

|Function  |Month  | Description |
|---------|---------|---------|
|[TABLEOF](../library/tableof.md)|February, 2026|Returns a reference to the table associated with a specified column, measure, or calendar.|
|[TOTALWTD](../library/totalwtd.md)|September, 2025|Calculates the running total of a measure to the current week in the filter context.|
|[CLOSINGBALANCEWEEK](../library/closingbalanceweek.md)|September, 2025|Returns the closing balance for the week in the current context.|
|[ENDOFWEEK](../library/endofweek.md)|September, 2025|Returns the last date of the current week in the calendar.|
|[NEXTWEEK](../library/nextweek.md)|September, 2025|Returns a table that contains a column of dates for the next week.|
|[OPENINGBALANCEWEEK](../library/openingbalanceweek.md)|September, 2025|Returns the opening balance for the week in the current context.|
|[PREVIOUSWEEK](../library/previousweek.md)|September, 2025|Returns a table that contains a column of dates for the previous week.|
|[STARTOFWEEK](../library/startofweek.md)|September, 2025|Returns the first date of the current week in the calendar.|
|[LOOKUPWITHTOTALS](../library/lookupwithtotals.md)|June, 2025| Used in visual calculations only. Look up the value when filters are applied. Filters not specified would not be inferred.|
|[LOOKUP](../library/lookup.md)|June, 2025| Used in visual calculations only. Look up the value when filters are applied. |
|[FIRST](../library/first.md)|January, 2024|Used in visual calculations only. Retrieves a value in the visual matrix from the first row of an axis.|
|[LAST](../library/last.md)|January, 2024|Used in visual calculations only. Retrieves a value in the visual matrix from the last row of an axis.|
|[NEXT](../library/next.md)|January, 2024|Used in visual calculations only. Retrieves a value in the next row of an axis in the visual matrix.|
|[PREVIOUS](../library/previous.md)|January, 2024|Used in visual calculations only. Retrieves a value in the previous row of an axis in the visual matrix. |
|[MATCHBY](../library/matchby.md)|May, 2023|Define the columns that are used to to match data and identify the current row, in a window function expression.|
|[RANK](../library/rank.md)|April, 2023|Returns the ranking for the current context within the specified partition, sorted by the specified order.|
|[ROWNUMBER](../library/rownumber.md)|April, 2023|Returns the unique ranking for the current context within the specified partition, sorted by the specified order.|
|[LINEST](../library/linest.md)|February, 2023|Uses the Least Squares method to calculate a straight line that best fits the given data.|
|[LINESTX](../library/linestx.md)|February, 2023|Uses the Least Squares method to calculate a straight line that best fits the given data. The data result from expressions evaluated for each row in a table.|
