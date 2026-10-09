---
name: USERNAME
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/username-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# USERNAME

Returns the domain name and username from the credentials given to the system at connection time.

## Syntax

```dax
USERNAME()
```

### Parameters

This expression has no parameters.

## Return value

The username from the credentials given to the system at connection time

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula verifies if the user login is part of the UsersTable.

```dax
= IF(CONTAINS(UsersTable,UsersTable[login], USERNAME()), "Allowed", BLANK())
```
