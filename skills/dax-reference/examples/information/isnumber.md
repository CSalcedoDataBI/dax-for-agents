---
function: ISNUMBER
model: ninguno
---

# ISNUMBER — ejemplos

## 1. Una FECHA también es un número

Es el resultado que rompe la clasificación por tipos escrita a la ligera. Internamente una
fecha es un número de serie, y `ISNUMBER` lo ve.

```dax
EVALUATE
ROW(
  "entero", ISNUMBER(42),
  "decimal", ISNUMBER(1.5),
  "moneda", ISNUMBER(CURRENCY(1.5)),
  "fecha", ISNUMBER(DATE(2024, 1, 1)),
  "fecha_tambien_es_fecha", ISDATETIME(DATE(2024, 1, 1))
)
```

```result
entero | decimal | moneda | fecha | fecha_tambien_es_fecha
True | True | True | True | True
```

Si ordenas una escalera de `IF(ISNUMBER(x), ..., IF(ISDATETIME(x), ...))`, las fechas nunca
llegan a la segunda rama. Pregunta primero por [`isdatetime`](./isdatetime.md).

## 2. Un número escrito como texto NO es un número

```dax
EVALUATE
ROW(
  "numero", ISNUMBER(42),
  "texto_que_parece_numero", ISNUMBER("42"),
  "booleano", ISNUMBER(TRUE),
  "blanco", ISNUMBER(BLANK())
)
```

```result
numero | texto_que_parece_numero | booleano | blanco
True | False | False | False
```

`ISNUMBER("42")` es **falso** aunque `ABS("42")` funcione: la conversión implícita ocurre al
operar, no al preguntar por el tipo. Y un booleano tampoco cuenta como número, aunque se sume
como 0 y 1.

## 3. `ISNUMERIC` está documentada como su alias y NO lo es

```dax
EVALUATE
ROW(
  "entero", ISNUMBER(42) = ISNUMERIC(42),
  "texto", ISNUMBER("42") = ISNUMERIC("42"),
  "moneda", ISNUMBER(CURRENCY(2)) = ISNUMERIC(CURRENCY(2)),
  "fecha", ISNUMBER(DATE(2024,1,1)) = ISNUMERIC(DATE(2024,1,1)),
  "fecha_con_isnumeric", ISNUMERIC(DATE(2024,1,1))
)
```

```result
entero | texto | moneda | fecha | fecha_con_isnumeric
True | True | True | False | False
```

Las tres primeras columnas comparan las dos funciones y coinciden. La cuarta dice que en una
**fecha no coinciden**: `ISNUMBER` la acepta y [`isnumeric`](./isnumeric.md) la rechaza. El
desacuerdo está acotado a los valores `datetime`, y cambiar una por otra en un modelo con
fechas cambia el resultado.

Ver [`isnumeric`](./isnumeric.md), [`isdatetime`](./isdatetime.md) y [`istext`](./istext.md).
