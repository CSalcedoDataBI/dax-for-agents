---
function: ISNUMERIC
model: ninguno
---

# ISNUMERIC — ejemplos

## 1. NO es un alias exacto de `ISNUMBER`: difieren en las fechas

La documentación las declara alias. Medido, no lo son. Una fecha es número para `ISNUMBER` y
**no** lo es para `ISNUMERIC`.

```dax
EVALUATE
ROW(
  "fecha_isnumber", ISNUMBER(DATE(2024, 1, 1)),
  "fecha_isnumeric", ISNUMERIC(DATE(2024, 1, 1)),
  "hora_isnumber", ISNUMBER(TIME(12, 0, 0)),
  "hora_isnumeric", ISNUMERIC(TIME(12, 0, 0))
)
```

```result
fecha_isnumber | fecha_isnumeric | hora_isnumber | hora_isnumeric
True | False | True | False
```

Cambiar una por otra en un modelo que maneje fechas cambia el resultado. No es una preferencia
de estilo.

## 2. En todo lo demás sí coinciden

El desacuerdo está acotado a los valores `datetime`, y solo a esos.

```dax
EVALUATE
ROW(
  "entero", ISNUMERIC(42) = ISNUMBER(42),
  "decimal", ISNUMERIC(1.5) = ISNUMBER(1.5),
  "moneda", ISNUMERIC(CURRENCY(2)) = ISNUMBER(CURRENCY(2)),
  "texto", ISNUMERIC("42") = ISNUMBER("42"),
  "blanco", ISNUMERIC(BLANK()) = ISNUMBER(BLANK()),
  "fecha", ISNUMERIC(DATE(2024,1,1)) = ISNUMBER(DATE(2024,1,1))
)
```

```result
entero | decimal | moneda | texto | blanco | fecha
True | True | True | True | True | False
```

Cada columna compara las dos funciones sobre el mismo valor. Las cinco primeras coinciden; la
sexta es la única que no.

## 3. Cuál usar, ahora que se sabe que no da igual

```dax
EVALUATE
ROW(
  "numero", ISNUMERIC(42),
  "texto_numerico", ISNUMERIC("42"),
  "fecha", ISNUMERIC(DATE(2024, 1, 1)),
  "booleano", ISNUMERIC(TRUE),
  "blanco", ISNUMERIC(BLANK())
)
```

```result
numero | texto_numerico | fecha | booleano | blanco
True | False | False | False | False
```

`ISNUMERIC` es la que responde «número, y no una fecha disfrazada». Si lo que quieres es
separar fechas de cantidades, es la correcta y `ISNUMBER` te las mezcla. Si quieres que las
fechas entren, la buena es [`isnumber`](./isnumber.md).

Lo que **ninguna de las dos** responde es «¿puede el motor operar aritméticamente con esto?».
`ISNUMBER("42")` es falso y sin embargo `"42" + 1` da 43: DAX convierte al operar, y el
predicado de tipo no lo sabe. Para esa pregunta no hay predicado — hay que intentar la
operación y protegerla.

El par [`istext`](./istext.md)/[`isstring`](./isstring.md) sí resultó idéntico en todos los
casos probados. Que dos funciones estén documentadas como alias no significa que lo sean.

Ver [`isnumber`](./isnumber.md) y [`isdatetime`](./isdatetime.md).
