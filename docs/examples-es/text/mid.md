---
function: MID
model: ninguno
---

# MID — ejemplos

## 1. La posición empieza en 1, y el 0 no es «desde el principio»: aborta

Es el error de traducción más común desde cualquier lenguaje de programación, donde el índice
empieza en cero. Aquí no devuelve la cadena entera ni una vacía — tumba la consulta.

```dax
EVALUATE ROW("desde_0", MID("Contoso", 0, 3))
```

```result
ERROR: An argument of function 'MID' has the wrong data type or has an invalid value.
```

Lo que sí es válido:

```dax
EVALUATE
ROW(
  "desde_1",  MID("Contoso", 1, 3),
  "desde_3",  MID("Contoso", 3, 3),
  "mas_alla", "[" & MID("Contoso", 20, 3) & "]",
  "pide_de_mas", MID("Contoso", 5, 99)
)
```

```result
desde_1 | desde_3 | mas_alla | pide_de_mas
Con | nto | [] | oso
```

Empezar más allá del final **no** da error: devuelve vacío. Así que el fallo silencioso y el
ruidoso están a un carácter de distancia.

## 2. Combinada con FIND, para partir por un separador

El patrón real. Y su punto débil: si el separador no está, `FIND` aborta y se lleva la
consulta entera.

```dax
EVALUATE
VAR Codigo = "ES-2024-0042"
RETURN
ROW(
  "primer_guion",  FIND("-", Codigo),
  "segundo_guion", FIND("-", Codigo, FIND("-", Codigo) + 1),
  "el_ano",        MID(Codigo, FIND("-", Codigo) + 1, 4),
  "el_pais",       LEFT(Codigo, FIND("-", Codigo) - 1)
)
```

```result
primer_guion | segundo_guion | el_ano | el_pais
3 | 8 | 2024 | ES
```

## 3. Sobre blanco, con longitud cero y con longitud negativa

```dax
EVALUATE
ROW(
  "blanco",        "[" & MID(BLANK(), 1, 3) & "]",
  "longitud_cero", "[" & MID("Contoso", 2, 0) & "]"
)
```

```result
blanco | longitud_cero
[] | []
```

La longitud negativa sí aborta, con el mismo mensaje genérico que la posición 0 — así que el
error no dice cuál de los dos argumentos estaba mal:

```dax
EVALUATE ROW("longitud_negativa", MID("Contoso", 2, -1))
```

```result
ERROR: An argument of function 'MID' has the wrong data type or has an invalid value.
```

Ver [`left`](./left.md), [`right`](./right.md) y [`find`](./find.md).
