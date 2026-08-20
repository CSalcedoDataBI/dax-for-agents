---
name: PATHLENGTH
category: [parent-and-child]
primaryCategory: parent-and-child
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/pathlength-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# PATHLENGTH

Returns the number of parents to the specified item in a given PATH result, including self.

## Syntax

```dax
PATHLENGTH(<path>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`path`|  A text expression resulting from evaluation of a PATH function. |

## Return value

The number of items that are parents to the specified item in a given PATH result, including the specified item.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example takes an employee ID as input to a PATH function and returns a list of the managers above that employee in the hierarchy, The PATHLENGTH function takes that result and counts the different levels of employees and managers, including the employee you started with.

```dax
= PATHLENGTH(PATH(Employee[EmployeeKey], Employee[ParentEmployeeKey]))
```
