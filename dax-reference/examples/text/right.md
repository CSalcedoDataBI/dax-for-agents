---
function: RIGHT
model: ninguno
---

# RIGHT — ejemplos

## 1. El patrón de «los últimos N» que se rompe con datos cortos

Igual que [`left`](./left.md): pedir de más devuelve lo que haya, sin avisar.

```dax
EVALUATE
ROW(
  "normal",       RIGHT("Contoso", 3),
  "mas_de_largo", RIGHT("ab", 10),
  "cero",         "[" & RIGHT("Contoso", 0) & "]",
  "sin_segundo",  RIGHT("Contoso")
)
```

```result
normal | mas_de_largo | cero | sin_segundo
oso | ab | [] | o
```

## 2. Para quedarse con la extensión o el sufijo, es frágil

El patrón habitual —`RIGHT(texto, LEN(texto) - FIND(".", texto))`— depende de que el
separador exista. Cuando no está, la cuenta se descuadra.

```dax
EVALUATE
VAR ConPunto = "informe.pbix"
RETURN
ROW(
  "posicion",  FIND(".", ConPunto),
  "extension", RIGHT(ConPunto, LEN(ConPunto) - FIND(".", ConPunto)),
  "dos_puntos", RIGHT("a.b.c", LEN("a.b.c") - FIND(".", "a.b.c")),
  "ultimo_punto_no", RIGHT("a.b.c", 1)
)
```

```result
posicion | extension | dos_puntos | ultimo_punto_no
8 | pbix | b.c | c
```

Con dos puntos corta por el **primero**, no por el último: `FIND` busca de izquierda a
derecha. Ver [`find`](./find.md).

## 3. Rellenar por la izquierda: el uso que sí aguanta

`RIGHT` sobre un texto ya rellenado es la forma corta de forzar un ancho fijo, y funciona
tanto si el original era corto como si era largo.

```dax
EVALUATE
ROW(
  "corto",  RIGHT("0000" & 42, 4),
  "justo",  RIGHT("0000" & 1234, 4),
  "largo",  RIGHT("0000" & 123456, 4),
  "blanco", RIGHT("0000" & BLANK(), 4)
)
```

```result
corto | justo | largo | blanco
0042 | 1234 | 3456 | 0000
```

El caso `largo` es el aviso: recorta por delante y se lleva las cifras significativas sin
decir nada.
