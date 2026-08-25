---
function: NOT
model: ninguno
---

# NOT — ejemplos

## 1. NOT de un blanco es VERDADERO

Es la trampa que convierte un filtro «lo que no sea X» en «lo que no sea X, más todo lo que
no tenga dato». El blanco se convierte en `FALSE`, y su negación es `TRUE`.

```dax
EVALUATE
ROW(
  "not_blanco", NOT(BLANK()),
  "not_falso",  NOT(FALSE()),
  "not_cierto", NOT(TRUE()),
  "not_cero",   NOT(0)
)
```

```result
not_blanco | not_falso | not_cierto | not_cero
True | True | False | True
```

Una fila sin dato pasa el filtro. Si eso no es lo que quieres, hace falta
`NOT(...) && NOT(ISBLANK(...))`.

## 2. Con números, cualquier cosa distinta de cero es verdadera

```dax
EVALUATE
ROW(
  "not_uno",      NOT(1),
  "not_cien",     NOT(100),
  "not_negativo", NOT(-5),
  "not_decimal",  NOT(0.5)
)
```

```result
not_uno | not_cien | not_negativo | not_decimal
False | False | False | False
```

El signo no importa: solo si es cero.

## 3. Negar una comparación no es invertirla

Con blancos de por medio, `NOT(a > b)` y `a <= b` dejan de comportarse como el álgebra
sugiere, porque la comparación con blanco no es la que uno tiene en la cabeza.

```dax
EVALUATE
ROW(
  "blanco_mayor_cero",     BLANK() > 0,
  "not_blanco_mayor_cero", NOT(BLANK() > 0),
  "blanco_menor_igual",    BLANK() <= 0,
  "blanco_igual_cero",     BLANK() = 0
)
```

```result
blanco_mayor_cero | not_blanco_mayor_cero | blanco_menor_igual | blanco_igual_cero
False | True | True | True
```
