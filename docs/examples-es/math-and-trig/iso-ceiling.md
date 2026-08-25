---
function: ISO.CEILING
model: ninguno
---

# ISO.CEILING — ejemplos

## 1. Siempre hacia más infinito, pase lo que pase con el signo

Es toda su razón de existir. [`ceiling`](./ceiling.md) cambia de dirección cuando la
significancia es negativa; esta no.

```dax
EVALUATE
ROW(
  "iso_sig_neg",     ISO.CEILING(-2.3, -1),
  "ceiling_sig_neg", CEILING(-2.3, -1),
  "iso_sig_pos",     ISO.CEILING(-2.3, 1),
  "ceiling_sig_pos", CEILING(-2.3, 1)
)
```

```result
iso_sig_neg | ceiling_sig_neg | iso_sig_pos | ceiling_sig_pos
-2 | -3 | -2 | -2
```

Las dos primeras columnas son la diferencia entera entre ambas funciones. Con significancia
positiva coinciden siempre, y por eso el problema no aparece en las pruebas.

## 2. Con significancia positiva se comporta como CEILING

```dax
EVALUATE
ROW(
  "positivo",  ISO.CEILING(2.1, 1),
  "negativo",  ISO.CEILING(-2.1, 1),
  "a_medios",  ISO.CEILING(2.3, 0.5),
  "ya_multiplo", ISO.CEILING(6, 3)
)
```

```result
positivo | negativo | a_medios | ya_multiplo
3 | -2 | 2.5 | 6
```

## 3. El segundo argumento es opcional

Sin él, significancia 1 — que es el caso que se quiere el 90% de las veces.

```dax
EVALUATE
ROW(
  "sin_segundo",  ISO.CEILING(2.1),
  "con_uno",      ISO.CEILING(2.1, 1),
  "negativo_sin", ISO.CEILING(-2.1),
  "blanco",       ISBLANK(ISO.CEILING(BLANK()))
)
```

```result
sin_segundo | con_uno | negativo_sin | blanco
3 | 3 | -2 | True
```

El nombre lleva punto (`ISO.CEILING`), así que el fichero de su ficha es `iso-ceiling.md` y
no `iso.ceiling.md`.
