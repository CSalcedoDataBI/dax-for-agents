---
function: ISNONTEXT
model: ninguno
---

# ISNONTEXT — ejemplos

## 1. Dice verdadero para un blanco — y `NOT ISTEXT` también

Conviene decirlo antes que nada, porque el nombre invita a suponer lo contrario: `ISNONTEXT` no
se comporta distinto de `NOT ISTEXT` en ningún caso probado, ni siquiera en el blanco (la
sección 3 lo mide). Existe por compatibilidad con Excel, donde la pregunta se formula así:
«¿esta celda tiene algo que no sea texto?», y una celda vacía cuenta que sí.

```dax
EVALUATE
ROW(
  "blanco", ISNONTEXT(BLANK()),
  "istext_del_blanco", ISTEXT(BLANK()),
  "cadena", ISNONTEXT("hola"),
  "numero", ISNONTEXT(42)
)
```

```result
blanco | istext_del_blanco | cadena | numero
True | False | False | True
```

El blanco no es texto, así que es «no texto». Suena a perogrullada hasta que lo usas para
filtrar: `FILTER(T, ISNONTEXT(T[x]))` se queda **también con las filas vacías**.

## 2. La cadena vacía va al otro lado

```dax
EVALUATE
ROW(
  "cadena_vacia", ISNONTEXT(""),
  "blanco", ISNONTEXT(BLANK()),
  "cero", ISNONTEXT(0),
  "booleano", ISNONTEXT(TRUE)
)
```

```result
cadena_vacia | blanco | cero | booleano
False | True | True | True
```

`""` es texto, así que `ISNONTEXT("")` es falso — mientras que el blanco da verdadero. Dos
valores que un visual pinta igual y que este predicado separa en dos grupos opuestos.

## 3. Coincide con `NOT ISTEXT` en todos los casos probados

```dax
EVALUATE
ROW(
  "blanco", ISNONTEXT(BLANK()) = NOT ISTEXT(BLANK()),
  "cadena", ISNONTEXT("x") = NOT ISTEXT("x"),
  "cadena_vacia", ISNONTEXT("") = NOT ISTEXT(""),
  "numero", ISNONTEXT(42) = NOT ISTEXT(42),
  "fecha", ISNONTEXT(DATE(2024,1,1)) = NOT ISTEXT(DATE(2024,1,1))
)
```

```result
blanco | cadena | cadena_vacia | numero | fecha
True | True | True | True | True
```

Son equivalentes, así que la elección es de legibilidad: `ISNONTEXT` se lee mejor cuando la
intención es «cualquier cosa menos texto, incluido nada».

Ver [`istext`](./istext.md) y [`isblank`](./isblank.md).
