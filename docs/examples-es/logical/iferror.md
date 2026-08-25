---
function: IFERROR
model: ninguno
---

# IFERROR — ejemplos

## 1. Se traga el error que querías ver

Es su función y también su peligro. Un `IFERROR` puesto alrededor de una expresión grande
oculta cualquier fallo que ocurra dentro, incluidos los que no tenían nada que ver con el
caso que se quería cubrir.

```dax
EVALUATE
ROW(
  "division_por_cero", IFERROR(1 / 0, "capturado"),
  "texto_a_numero",    IFERROR(VALUE("no soy un número"), "capturado"),
  "sin_error",         IFERROR(10 / 2, "capturado")
)
```

```result
division_por_cero | texto_a_numero | sin_error
capturado | capturado | 5
```

Los dos primeros devuelven lo mismo, y son problemas distintos: uno es aritmética, el otro un
dato con la forma equivocada. Con `IFERROR` alrededor de los dos, el informe no distingue.

## 2. Para dividir, DIVIDE es mejor

`DIVIDE` resuelve el caso concreto sin desactivar el resto de errores, y el motor lo entiende
mejor que un `IFERROR` envolviendo una división.

```dax
EVALUATE
ROW(
  "iferror",        IFERROR(1 / 0, 0),
  "divide",         DIVIDE(1, 0, 0),
  "divide_sin_alt", ISBLANK(DIVIDE(1, 0)),
  "cero_entre_cero", DIVIDE(0, 0, -1)
)
```

```result
iferror | divide | divide_sin_alt | cero_entre_cero
0 | 0 | True | -1
```

`DIVIDE` sin tercer argumento devuelve blanco, no cero. Otra vez la misma decisión.

## 3. El valor alternativo no tiene que ser del mismo tipo

Y ahí empieza el problema siguiente: lo que devuelve puede no servir para lo que venía
después.

```dax
EVALUATE
ROW(
  "numero_o_texto", IFERROR(1 / 0, "sin dato"),
  "suma_despues",   IFERROR(1 / 0, 0) + 100,
  "anidado",        IFERROR(IFERROR(1 / 0, VALUE("x")), "los dos fallaron")
)
```

```result
numero_o_texto | suma_despues | anidado
sin dato | 100 | los dos fallaron
```

Ver [`coalesce`](./coalesce.md), que es lo que suele querer quien escribe un `IFERROR`: no
capturar un error, sino sustituir un blanco.
