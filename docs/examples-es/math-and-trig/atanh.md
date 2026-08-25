---
function: ATANH
model: ninguno
---

# ATANH — ejemplos

## 1. Solo entre -1 y 1, y los extremos NO valen

`TANH` vive dentro de (-1, 1) sin llegar nunca a los bordes, así que su inversa se dispara ahí.

```dax
EVALUATE ROW("en_el_borde", ATANH(1))
```

```result
ERROR: An argument of function 'ATANH' has the wrong data type or the result is too large or too small.
```

```dax
EVALUATE
ROW(
  "medio", ROUND(ATANH(0.5), 6),
  "casi_uno", ROUND(ATANH(0.999), 6),
  "uno", IFERROR(ATANH(1), "aborta"),
  "mas_de_uno", IFERROR(ATANH(2), "aborta")
)
```

```result
medio | casi_uno | uno | mas_de_uno
0.549306 | 3.800201 | aborta | aborta
```

En 0,999 el valor todavía es 3,8: se dispara solo en el último tramo. Es el intervalo abierto,
no el cerrado — y un dato normalizado que llegue justo a 1 tumba la consulta.

## 2. El blanco pasa y sale en blanco

```dax
EVALUATE
ROW(
  "blanco", ATANH(BLANK()),
  "es_blanco", ISBLANK(ATANH(BLANK())),
  "cero", ATANH(0),
  "acoth_blanco", IFERROR(ACOTH(BLANK()), "aborta")
)
```

```result
blanco | es_blanco | cero | acoth_blanco
(blank) | True | 0 | aborta
```

El cero está **dentro** de su dominio, así que el blanco entra, sale cero y vuelve a salir
blanco. [`acoth`](./acoth.md), cuyo dominio es justo el complementario, aborta con el mismo
blanco.

## 3. Es impar, es un logaritmo, y por eso se usa para correlaciones

```dax
EVALUATE
ROW(
  "impar", ROUND(ATANH(0.5) + ATANH(-0.5), 10),
  "ida_y_vuelta", ROUND(ATANH(TANH(2)), 10),
  "formula_cerrada", ROUND(ATANH(0.5) - 0.5 * LN(1.5 / 0.5), 10),
  "fisher_de_0_9", ROUND(ATANH(0.9), 6)
)
```

```result
impar | ida_y_vuelta | formula_cerrada | fisher_de_0_9
0 | 2 | 0 | 1.472219
```

`ATANH(x) = ½ · LN((1+x)/(1-x))`. Es la transformación *z* de Fisher: convierte un coeficiente
de correlación —que vive acotado en (-1, 1) y no se puede promediar sin sesgo— en una escala
sin techo donde sí se puede.

Ver [`tanh`](./tanh.md), [`acoth`](./acoth.md) y [`ln`](./ln.md).
