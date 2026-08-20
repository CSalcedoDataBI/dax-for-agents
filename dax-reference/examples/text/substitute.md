---
function: SUBSTITUTE
model: ninguno
---

# SUBSTITUTE — ejemplos

## 1. Distingue mayúsculas de minúsculas

Al contrario que [`search`](./search.md), que no las distingue. Es la asimetría que hace que
una limpieza «funcione» en la prueba y deje la mitad de las filas sin tocar en producción.

```dax
EVALUATE
ROW(
  "coincide",     SUBSTITUTE("Sony Bravia", "Sony", "SONY"),
  "no_coincide",  SUBSTITUTE("Sony Bravia", "sony", "SONY"),
  "todas",        SUBSTITUTE("aaa", "a", "b"),
  "sin_encontrar", SUBSTITUTE("hola", "z", "!")
)
```

```result
coincide | no_coincide | todas | sin_encontrar
SONY Bravia | Sony Bravia | bbb | hola
```

Cuando no encuentra nada **no da error**: devuelve el texto igual. El fallo es silencioso.

## 2. Reemplaza TODAS las apariciones, salvo que digas cuál

El cuarto argumento elige la ocurrencia. Sin él, cambia todas — que casi nunca es lo que se
quiere al limpiar un separador.

```dax
EVALUATE
ROW(
  "todas",     SUBSTITUTE("a-b-c-d", "-", "/"),
  "solo_la_1", SUBSTITUTE("a-b-c-d", "-", "/", 1),
  "solo_la_3", SUBSTITUTE("a-b-c-d", "-", "/", 3),
  "la_9",      SUBSTITUTE("a-b-c-d", "-", "/", 9)
)
```

```result
todas | solo_la_1 | solo_la_3 | la_9
a/b/c/d | a/b-c-d | a-b-c/d | a-b-c-d
```

Pedir una ocurrencia que no existe tampoco falla: devuelve el texto sin tocar.

## 3. Es la herramienta para el espacio duro que TRIM no quita

El caso real por el que se usa. Hay que **nombrar** el carácter, porque no se ve.

```dax
EVALUATE
VAR Sucio = "  hola" & UNICHAR(160) & "mundo  "
RETURN
ROW(
  "solo_trim",         LEN(TRIM(Sucio)),
  "substitute_y_trim", LEN(TRIM(SUBSTITUTE(Sucio, UNICHAR(160), " "))),
  "resultado",         TRIM(SUBSTITUTE(Sucio, UNICHAR(160), " ")),
  "borrar_del_todo",   SUBSTITUTE("a b c", " ", "")
)
```

```result
solo_trim | substitute_y_trim | resultado | borrar_del_todo
10 | 10 | hola mundo | abc
```

Ver [`trim`](./trim.md) para por qué no basta con él, y [`replace`](./replace.md) para
sustituir **por posición** en vez de por contenido.
