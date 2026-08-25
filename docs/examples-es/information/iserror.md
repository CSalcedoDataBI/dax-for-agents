---
function: ISERROR
model: ninguno
---

# ISERROR — ejemplos

## 1. Un blanco no es un error, y `DIVIDE` por cero tampoco

Es la distinción que separa a las dos familias de «algo salió mal» en DAX.

```dax
EVALUATE
ROW(
  "division_con_operador", ISERROR(1 / 0),
  "division_con_funcion", ISERROR(DIVIDE(1, 0)),
  "blanco", ISERROR(BLANK()),
  "normal", ISERROR(1 / 2)
)
```

```result
division_con_operador | division_con_funcion | blanco | normal
True | False | False | False
```

`1 / 0` es un error; `DIVIDE(1, 0)` es un **blanco**, que no lo es. Esa es la razón entera de
que [`divide`](../math-and-trig/divide.md) exista.

## 2. Sí atrapa lo que aborta la consulta — al contrario que `IFERROR` sobre un iterador

```dax
EVALUATE
ROW(
  "log_de_cero", ISERROR(LN(0)),
  "raiz_negativa", ISERROR(SQRT(-1)),
  "cero_a_la_cero", ISERROR(POWER(0, 0)),
  "texto_mas_numero", ISERROR(1 + "hola")
)
```

```result
log_de_cero | raiz_negativa | cero_a_la_cero | texto_mas_numero
True | True | True | True
```

Las cuatro matarían la consulta escritas sueltas. `ISERROR` las evalúa y devuelve verdadero sin
que la consulta caiga — ojo, eso vale para la **expresión** que envuelve, no para un `SUMX`
entero, como está medido en [`ln`](../math-and-trig/ln.md).

## 3. Sirve para clasificar, no para reemplazar

Si lo único que quieres es un valor alternativo, `IFERROR` lo dice en una línea. `ISERROR`
gana cuando necesitas **contar** o **etiquetar** los errores en vez de taparlos.

```dax
EVALUATE
VAR Entradas = { 4, 0, -1 }
RETURN
ROW(
  "cuantas_fallan", COUNTROWS(FILTER(Entradas, ISERROR(SQRT([Value])))),
  "cuantas_valen", COUNTROWS(FILTER(Entradas, NOT ISERROR(SQRT([Value])))),
  "suma_de_las_buenas", SUMX(FILTER(Entradas, NOT ISERROR(SQRT([Value]))), SQRT([Value]))
)
```

```result
cuantas_fallan | cuantas_valen | suma_de_las_buenas
1 | 2 | 2
```

Una de las tres entradas es imposible. `IFERROR` la habría convertido en cero y el informe
diría que hay tres medidas correctas; así dice que hay dos y una rota.

Ver [`isblank`](./isblank.md) y [`divide`](../math-and-trig/divide.md).
