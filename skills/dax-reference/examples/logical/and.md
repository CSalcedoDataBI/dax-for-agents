---
function: AND
model: ninguno
---

# AND — ejemplos

## 1. Solo acepta DOS argumentos

Es la diferencia con Excel que más tiempo cuesta. Con tres condiciones hay que anidarla, o
usar `&&`, que sí encadena.

```dax
EVALUATE
ROW(
  "dos_condiciones", AND(1 = 1, 2 = 2),
  "anidada",         AND(1 = 1, AND(2 = 2, 3 = 3)),
  "operador",        1 = 1 && 2 = 2 && 3 = 3
)
```

```result
dos_condiciones | anidada | operador
True | True | True
```

Con tres argumentos no da un resultado raro: **aborta**, y el mensaje dice exactamente cuántos
esperaba.

```dax
EVALUATE ROW("tres_argumentos", AND(1 = 1, 2 = 2, 3 = 3))
```

```result
ERROR: Too many arguments were passed to the AND function. The maximum argument count for the function is 2.
```

## 2. Un blanco es FALSO, y no se distingue de un falso de verdad

`AND` convierte a booleano antes de operar, así que un blanco entra como `FALSE`. El
resultado no dice si la condición era falsa o si no había dato.

```dax
EVALUATE
ROW(
  "blanco_y_cierto", AND(BLANK(), TRUE()),
  "falso_y_cierto",  AND(FALSE(), TRUE()),
  "blanco_y_blanco", AND(BLANK(), BLANK()),
  "cero_y_cierto",   AND(0, TRUE())
)
```

```result
blanco_y_cierto | falso_y_cierto | blanco_y_blanco | cero_y_cierto
False | False | False | False
```

Si necesitas distinguir «no aplica» de «no», `AND` no es la herramienta: hace falta un
`ISBLANK` explícito antes.

## 3. Con números no compara, convierte

Cualquier valor distinto de cero es verdadero. Un `AND` sobre columnas numéricas no está
comparando magnitudes: está preguntando si son distintas de cero.

```dax
EVALUATE
ROW(
  "dos_positivos",   AND(5, 3),
  "uno_negativo",    AND(-1, 1),
  "con_cero",        AND(5, 0),
  "decimal_pequeno", AND(0.0001, 1)
)
```

```result
dos_positivos | uno_negativo | con_cero | decimal_pequeno
True | True | False | True
```

Ver [`or`](./or.md), que tiene exactamente las mismas tres trampas.
