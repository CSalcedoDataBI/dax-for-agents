---
function: ISDATETIME
model: ninguno
---

# ISDATETIME — ejemplos

## 1. Una fecha es fecha Y es número al mismo tiempo

Ese solapamiento es lo que rompe las clasificaciones por tipo escritas en el orden equivocado.

```dax
EVALUATE
ROW(
  "fecha_es_fecha", ISDATETIME(DATE(2024, 1, 1)),
  "fecha_es_numero", ISNUMBER(DATE(2024, 1, 1)),
  "numero_es_fecha", ISDATETIME(45000),
  "numero_es_numero", ISNUMBER(45000)
)
```

```result
fecha_es_fecha | fecha_es_numero | numero_es_fecha | numero_es_numero
True | True | False | True
```

La asimetría es la clave: una fecha pasa por número, pero un número **no** pasa por fecha
aunque sea un número de serie válido. El tipo lo lleva el valor, no su magnitud. En una
escalera de `IF`, `ISDATETIME` tiene que ir **antes** que [`isnumber`](./isnumber.md).

## 2. Una fecha escrita como texto no es una fecha

```dax
EVALUATE
ROW(
  "fecha", ISDATETIME(DATE(2024, 1, 1)),
  "texto_con_pinta_de_fecha", ISDATETIME("2024-01-01"),
  "es_texto", ISTEXT("2024-01-01"),
  "hora_tambien_cuenta", ISDATETIME(TIME(12, 30, 0))
)
```

```result
fecha | texto_con_pinta_de_fecha | es_texto | hora_tambien_cuenta
True | False | True | True
```

Es el mismo patrón que `ISNUMBER("42")`. Y una hora sin fecha también entra: el tipo es
`datetime`, no «fecha».

## 3. El blanco no tiene tipo, tampoco aquí

```dax
EVALUATE
ROW(
  "blanco", ISDATETIME(BLANK()),
  "blanco_es_blanco", ISBLANK(BLANK()),
  "fecha_cero", ISDATETIME(DATE(1899, 12, 30)),
  "booleano", ISDATETIME(TRUE)
)
```

```result
blanco | blanco_es_blanco | fecha_cero | booleano
False | True | True | False
```

30/12/1899 es el origen del calendario en DAX y sigue siendo una fecha perfectamente válida —
lo que no es fecha es el blanco. Para las columnas de fecha con huecos, la pregunta va con
[`isblank`](./isblank.md).

Ver [`isnumber`](./isnumber.md) y [`isblank`](./isblank.md).
