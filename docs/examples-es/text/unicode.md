---
function: UNICODE
model: ninguno
---

# UNICODE — ejemplos

## 1. Solo mira el PRIMER carácter

No es «el código del texto»: es el del primero y nada más. Sirve para auditar qué hay al
principio de una cadena, no para comparar cadenas.

```dax
EVALUATE
ROW(
  "una_letra",    UNICODE("A"),
  "una_palabra",  UNICODE("Abc"),
  "otra_palabra", UNICODE("Azz"),
  "iguales",      UNICODE("Abc") = UNICODE("Azz")
)
```

```result
una_letra | una_palabra | otra_palabra | iguales
65 | 65 | 65 | True
```

## 2. Para lo que sirve de verdad: ver el carácter invisible

Cuando dos textos se ven iguales y no cruzan, esto lo dice en una línea.

```dax
EVALUATE
VAR Sucio = "hola" & UNICHAR(160)
RETURN
ROW(
  "ultimo_de_sucio",  UNICODE(RIGHT(Sucio, 1)),
  "ultimo_de_limpio", UNICODE(RIGHT("hola ", 1)),
  "tras_trim",        UNICODE(RIGHT(TRIM(Sucio), 1)),
  "esperado_a",       UNICODE("a")
)
```

```result
ultimo_de_sucio | ultimo_de_limpio | tras_trim | esperado_a
160 | 32 | 160 | 97
```

160 frente a 32: el primero es el espacio duro que [`trim`](./trim.md) no quita, el segundo
el espacio normal. Y `tras_trim` sigue siendo 160, que es la demostración en una celda.

## 3. Con blanco y con cadena vacía devuelve BLANCO, no error

Es lo contrario de lo que hace [`value`](./value.md), que aborta con la cadena vacía. Aquí no
hay que proteger nada — pero tampoco se puede distinguir «no había texto» de «el primer
carácter es raro» sin mirar antes.

```dax
EVALUATE
ROW(
  "numero",       UNICODE("5"),
  "acentuada",    UNICODE("é"),
  "enye",         UNICODE("ñ"),
  "cadena_vacia", UNICODE(""),
  "blanco",       UNICODE(BLANK())
)
```

```result
numero | acentuada | enye | cadena_vacia | blanco
53 | 233 | 241 | (blank) | (blank)
```

Donde sí aborta es con medio par sustituto — la mitad de un emoji cortado con `LEFT`. Ver
[`unichar`](./unichar.md), que es el camino de vuelta y donde está ese caso.
