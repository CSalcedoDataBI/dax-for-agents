---
function: QUOTIENT
model: ninguno
---

# QUOTIENT — ejemplos

## 1. Trunca hacia cero, no hacia abajo

Con números positivos las dos cosas coinciden y nadie lo nota. Con negativos se separan, y
`QUOTIENT` **no** es `INT` de la división.

```dax
EVALUATE
ROW(
  "quotient_pos", QUOTIENT(10, 3),
  "int_pos", INT(10 / 3),
  "quotient_neg", QUOTIENT(-10, 3),
  "int_neg", INT(-10 / 3),
  "trunc_neg", TRUNC(-10 / 3)
)
```

```result
quotient_pos | int_pos | quotient_neg | int_neg | trunc_neg
3 | 3 | -3 | -4 | -3
```

`QUOTIENT` va con `TRUNC` (hacia cero) y no con `INT` (hacia abajo). Si estás paginando o
troceando por lotes y algún valor puede ser negativo, la diferencia es un lote entero.

## 2. Descarta el resto en silencio, incluso con decimales

No redondea: se queda con la parte entera del cociente y tira lo demás sin avisar.

```dax
EVALUATE
ROW(
  "casi_cuatro", QUOTIENT(11.9, 3),
  "division_real", ROUND(11.9 / 3, 6),
  "decimales_arriba", QUOTIENT(7, 2),
  "division_real_2", 7 / 2
)
```

```result
casi_cuatro | division_real | decimales_arriba | division_real_2
3 | 3.966667 | 3 | 3.5
```

3,97 se convierte en 3. Es lo que se pide de una división entera, pero conviene verlo escrito
antes de usarla para repartir importes.

## 3. El divisor cero aborta la consulta

Como [`mod`](./mod.md) y a diferencia de [`divide`](./divide.md), aquí no hay blanco de
cortesía.

```dax
EVALUATE
ROW(
  "divisor_cero", IFERROR(QUOTIENT(10, 0), "aborta"),
  "dividendo_blanco", QUOTIENT(BLANK(), 3),
  "divisor_blanco", IFERROR(QUOTIENT(10, BLANK()), "aborta")
)
```

```result
divisor_cero | dividendo_blanco | divisor_blanco
aborta | (blank) | aborta
```

Un divisor **en blanco** también aborta, porque entra como cero. Ese es el caso que llega desde
los datos y no desde una constante escrita a mano.

Ver [`mod`](./mod.md), [`divide`](./divide.md) e [`int`](./int.md).
