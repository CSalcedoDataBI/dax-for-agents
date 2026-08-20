---
function: LEFT
model: ninguno
---

# LEFT — ejemplos

## 1. Pedir más de lo que hay no da error

Devuelve lo que haya. Suena cómodo y es justo lo que impide detectar que el dato venía corto:
un código de 3 letras y uno de 8 salen los dos «bien».

```dax
EVALUATE
ROW(
  "normal",       LEFT("Contoso", 3),
  "mas_de_largo", LEFT("ab", 10),
  "cero",         "[" & LEFT("Contoso", 0) & "]",
  "sin_segundo",  LEFT("Contoso")
)
```

```result
normal | mas_de_largo | cero | sin_segundo
Con | ab | [] | C
```

Sin el segundo argumento devuelve **un** carácter, no la cadena entera.

## 2. Un número negativo sí aborta

Es la única forma de que avise, y llega por una variable calculada, no por una constante.

```dax
EVALUATE ROW("negativo", LEFT("Contoso", -1))
```

```result
ERROR: An argument of function 'LEFT' has the wrong data type or has an invalid value.
```

## 3. Sobre un blanco y sobre un número

```dax
EVALUATE
ROW(
  "blanco",     "[" & LEFT(BLANK(), 3) & "]",
  "es_blanco",  ISBLANK(LEFT(BLANK(), 3)),
  "numero",     LEFT(12345, 2),
  "decimal",    LEFT(1.75, 3)
)
```

```result
blanco | es_blanco | numero | decimal
[] | True | 12 | 1,7
```

Sobre un número convierte a texto primero, con la cultura del modelo — así que el corte
depende de si el separador decimal es coma o punto.

Ver [`right`](./right.md), [`mid`](./mid.md) y [`len`](./len.md), que cuenta unidades de
código y no caracteres visibles: ahí es donde un emoji se parte por la mitad.
