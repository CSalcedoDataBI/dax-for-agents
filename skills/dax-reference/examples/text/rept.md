---
function: REPT
model: ninguno
---

# REPT — ejemplos

## 1. Cero repeticiones da cadena vacía, no blanco

Importa porque el uso típico de `REPT` es dibujar una barra en una tabla, y la fila con valor
cero tiene que quedar vacía sin desaparecer.

```dax
EVALUATE
ROW(
  "tres",       REPT("*", 3),
  "cero",       "[" & REPT("*", 0) & "]",
  "es_blanco",  ISBLANK(REPT("*", 0)),
  "uno",        REPT("ab", 1)
)
```

```result
tres | cero | es_blanco | uno
*** | [] | False | ab
```

## 2. El número se REDONDEA, no se trunca

Lo que importa cuando el conteo sale de una división: `2.5` no dibuja 2 barras.

```dax
EVALUATE
ROW(
  "dos_coma_cuatro", LEN(REPT("*", 2.4)),
  "dos_coma_cinco",  LEN(REPT("*", 2.5)),
  "dos_coma_seis",   LEN(REPT("*", 2.6)),
  "casi_uno",        LEN(REPT("*", 0.6))
)
```

```result
dos_coma_cuatro | dos_coma_cinco | dos_coma_seis | casi_uno
2 | 3 | 3 | 1
```

## 3. El caso real: una barra proporcional dentro de una tabla

Con la trampa de siempre — si el valor puede ser negativo, aborta.

```dax
EVALUATE
VAR Maximo = 20
RETURN
ROW(
  "barra_de_5",  REPT("█", DIVIDE(5, Maximo) * 10),
  "barra_de_20", REPT("█", DIVIDE(20, Maximo) * 10),
  "barra_de_0",  "[" & REPT("█", DIVIDE(0, Maximo) * 10) & "]"
)
```

```result
barra_de_5 | barra_de_20 | barra_de_0
███ | ██████████ | []
```

```dax
EVALUATE ROW("negativo", REPT("*", -1))
```

```result
ERROR: An argument of function 'REPT' has the wrong data type or has an invalid value.
```

Por eso el conteo va envuelto en `MAX(0, ...)` cuando el dato puede venir por debajo de cero.
