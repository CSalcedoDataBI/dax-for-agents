---
function: LOG10
model: ninguno
---

# LOG10 — ejemplos

## 1. Cuenta dígitos, que es para lo que sirve en un informe

`LOG10` de un número es aproximadamente cuántos dígitos tiene menos uno. Es la forma corta de
agrupar por órdenes de magnitud sin escribir una escalera de `IF`.

```dax
EVALUATE
ROW(
  "cien", LOG10(100),
  "mil", LOG10(1000),
  "mil_y_pico", ROUND(LOG10(1234), 6),
  "orden", INT(LOG10(1234)),
  "digitos", INT(LOG10(1234)) + 1
)
```

```result
cien | mil | mil_y_pico | orden | digitos
2 | 3 | 3.091315 | 3 | 4
```

`INT(LOG10(n)) + 1` da el número de dígitos de un entero positivo. Para agrupar en escalas
—decenas, centenas, miles— `INT(LOG10(n))` es el cubo directamente.

## 2. Es `LOG` sin segundo argumento, y no es `LN`

```dax
EVALUATE
ROW(
  "log10", LOG10(1000),
  "log_sin_base", LOG(1000),
  "log_base_10", LOG(1000, 10),
  "ln", ROUND(LN(1000), 6),
  "cociente", ROUND(LN(1000) / LOG10(1000), 6)
)
```

```result
log10 | log_sin_base | log_base_10 | ln | cociente
3 | 3 | 3 | 6.907755 | 2.302585
```

Las tres primeras son idénticas. La cuarta es otra función, y ese 2,302585 —`LN(10)`— es el
factor constante que las separa. Un informe con la función equivocada no falla: publica cifras
2,3 veces más grandes.

## 3. Cero, negativos y blanco abortan la consulta

```dax
EVALUATE
ROW(
  "cero", IFERROR(LOG10(0), "aborta"),
  "negativo", IFERROR(LOG10(-1), "aborta"),
  "blanco", IFERROR(LOG10(BLANK()), "aborta"),
  "uno", LOG10(1)
)
```

```result
cero | negativo | blanco | uno
aborta | aborta | aborta | 0
```

El blanco aborta porque entra como cero. Ese es el caso que llega desde una columna con huecos
y no desde una constante escrita a mano.

Ver [`log`](./log.md), [`ln`](./ln.md) y [`power`](./power.md).
