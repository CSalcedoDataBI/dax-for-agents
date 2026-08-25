---
function: LOG
model: ninguno
---

# LOG — ejemplos

## 1. Sin segundo argumento la base es 10, no *e*

Viniendo de C, Python o R —donde `log` es el natural— esto se lee al revés. En DAX, como en
Excel, `LOG` sin base es base 10.

```dax
EVALUATE
ROW(
  "log_100", LOG(100),
  "log10_100", LOG10(100),
  "ln_100", ROUND(LN(100), 6),
  "log_100_base_e", ROUND(LOG(100, EXP(1)), 6)
)
```

```result
log_100 | log10_100 | ln_100 | log_100_base_e
2 | 2 | 4.60517 | 4.60517
```

Las columnas 1 y 2 son la misma función; las 3 y 4 también. Confundir las dos parejas da un
número creíble multiplicado por 2,302585.

## 2. La base 1 aborta, y la base 2 es la que de verdad se usa

```dax
EVALUATE ROW("base_uno", LOG(8, 1))
```

```result
ERROR: Division by zero has occurred when evaluating function 'LOG'.
```

No hay logaritmo en base 1: `1ˣ` es siempre 1, así que no existe exponente que dé 8. El
mensaje es literalmente **una división por cero**, y no el error genérico de argumento que
sueltan el resto de funciones de esta familia: internamente `LOG(n, b)` es `LN(n) / LN(b)`, y
`LN(1)` es cero. El caso
útil de verdad es la base 2, para contar duplicaciones:

```dax
EVALUATE
ROW(
  "log2_8", LOG(8, 2),
  "log2_1024", LOG(1024, 2),
  "duplicaciones", ROUND(LOG(1000, 2), 6),
  "log2_1", LOG(1, 2)
)
```

```result
log2_8 | log2_1024 | duplicaciones | log2_1
3 | 10 | 9.965784 | 0
```

Mil son casi diez duplicaciones. `LOG(1, base)` es 0 en cualquier base, que es lo que dice la
definición.

## 3. Cero y negativos abortan, y el blanco entra como cero

```dax
EVALUATE
ROW(
  "cero", IFERROR(LOG(0), "aborta"),
  "negativo", IFERROR(LOG(-5), "aborta"),
  "blanco", IFERROR(LOG(BLANK()), "aborta"),
  "base_negativa", IFERROR(LOG(8, -2), "aborta")
)
```

```result
cero | negativo | blanco | base_negativa
aborta | aborta | aborta | aborta
```

Cuatro formas de tumbar la misma consulta. Y ojo con dónde pones la protección: envolver un
iterador en `IFERROR` **no** atrapa el error que se levanta dentro — está medido en
[`ln`](./ln.md).

Ver [`ln`](./ln.md), [`log10`](./log10.md) y [`power`](./power.md), su inversa.
