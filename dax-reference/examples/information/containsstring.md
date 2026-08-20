---
function: CONTAINSSTRING
model: ninguno
---

# CONTAINSSTRING — ejemplos

## 1. Ignora las mayúsculas pero NO los acentos

Media verdad es peor que ninguna, y aquí la media verdad es «no distingue mayúsculas». Cierto.
Lo que nadie dice es que los acentos sí los distingue, y en español eso es la mitad del
catálogo.

```dax
EVALUATE
ROW(
  "minusculas", CONTAINSSTRING("Bicicleta", "bici"),
  "acento_perdido", CONTAINSSTRING("Almacén", "almacen"),
  "acento_puesto", CONTAINSSTRING("Almacén", "MACÉN"),
  "enie", CONTAINSSTRING("Año", "ano")
)
```

```result
minusculas | acento_perdido | acento_puesto | enie
True | False | True | False
```

`"bici"` encuentra `"Bicicleta"` y `"MACÉN"` encuentra `"Almacén"` — la caja da igual. Pero
`"almacen"` **no** encuentra `"Almacén"`, y `"ano"` no encuentra `"Año"`. Un buscador de un
informe donde el usuario teclea sin tildes devuelve cero resultados y parece roto.

## 2. `*` y `?` son comodines, no caracteres

Esto no está en el nombre de la función ni se espera de algo llamado «contiene cadena».

```dax
EVALUATE
ROW(
  "asterisco", CONTAINSSTRING("aXXXb", "a*b"),
  "interrogante", CONTAINSSTRING("aXb", "a?b"),
  "interrogante_exige_uno", CONTAINSSTRING("ab", "a?b"),
  "asterisco_sobre_si_mismo", CONTAINSSTRING("a*b", "a*b")
)
```

```result
asterisco | interrogante | interrogante_exige_uno | asterisco_sobre_si_mismo
True | True | False | True
```

`"a*b"` encuentra `"aXXXb"`: el `*` se traga cualquier cosa. El `?` sustituye **exactamente
un** carácter, así que `"a?b"` no encuentra `"ab"` — donde no hay carácter, no hay coincidencia.

La cuarta columna es la trampa fina: `CONTAINSSTRING("a*b", "a*b")` es verdadero, pero **no
porque haya encontrado el asterisco**. Es verdadero porque `a`, cualquier cosa, `b` describe a
`"a*b"` igual que describe a `"aXXXb"`. Tal cual, esta llamada no distingue un asterisco real de
uno imaginario. Para eso está el escape de la sección siguiente.

## 3. Una aguja en blanco encuentra siempre

```dax
EVALUATE
ROW(
  "aguja_vacia", CONTAINSSTRING("Bicicleta", ""),
  "aguja_blanca", CONTAINSSTRING("Bicicleta", BLANK()),
  "pajar_blanco", CONTAINSSTRING(BLANK(), "a"),
  "numeros", CONTAINSSTRING(12345, 234)
)
```

```result
aguja_vacia | aguja_blanca | pajar_blanco | numeros
True | True | False | True
```

Las dos primeras columnas son la razón de leer esto. Un cuadro de búsqueda vacío se traduce en
`CONTAINSSTRING([Producto], [TextoBuscado])` con el segundo argumento en blanco, y **eso
devuelve verdadero para todas las filas**: el filtro no filtra nada. No es un fallo, es que la
cadena vacía está contenida en cualquier cadena. Pero pasa desapercibido porque el informe
enseña justo lo que enseñaría sin filtro.

La defensa es no llamar a la función cuando no hay término. Pero **`ISBLANK` no basta**, y es un
error fácil de cometer porque las dos columnas de arriba parecen el mismo caso y no lo son:
`ISBLANK("")` es falso —la cadena vacía es texto, medido en [`isblank`](./isblank.md)—, así que
un guardia con `ISBLANK` deja pasar justo la mitad del problema. El que cubre las dos es `LEN`:

```dax
EVALUATE
ROW(
  "len_de_blanco", LEN(BLANK()),
  "len_de_cadena_vacia", LEN(""),
  "guardia_con_blanco", LEN(BLANK()) > 0,
  "guardia_con_vacia", LEN("") > 0,
  "guardia_con_termino", LEN("bici") > 0,
  "isblank_no_ve_la_vacia", ISBLANK("")
)
```

```result
len_de_blanco | len_de_cadena_vacia | guardia_con_blanco | guardia_con_vacia | guardia_con_termino | isblank_no_ve_la_vacia
(blank) | 0 | False | False | True | False
```

Fíjate en la primera columna: `LEN(BLANK())` **no es 0, es blanco**. El guardia funciona
igualmente, y la razón merece medirse aparte porque es fácil contarla mal:

```dax
EVALUATE
ROW(
  "blanco_igual_a_cero", BLANK() = 0,
  "blanco_mayor_que_cero", BLANK() > 0,
  "blanco_menor_que_cero", BLANK() < 0,
  "blanco_mayor_o_igual_cero", BLANK() >= 0,
  "blanco_mayor_que_menos_uno", BLANK() > -1
)
```

```result
blanco_igual_a_cero | blanco_mayor_que_cero | blanco_menor_que_cero | blanco_mayor_o_igual_cero | blanco_mayor_que_menos_uno
True | False | False | True | True
```

No es que comparar un blanco con un número dé falso —`BLANK() = 0` es **verdadero**, y
`BLANK() > -1` también—. Es que en una comparación numérica **el blanco se comporta como un
cero**. Por eso `LEN(BLANK()) > 0` es falso: no porque la comparación falle, sino porque cero
no es mayor que cero.

Así que la forma correcta es `IF(LEN([Buscado]) > 0, CONTAINSSTRING(...))`, y funciona por la
misma razón para el blanco y para la cadena vacía.

Y la última columna: los números entran convertidos a texto, así que `234` se encuentra dentro
de `12345` aunque ninguno de los dos sea una cadena.

## 4. `~` desactiva el comodín, y ahí sí busca el carácter de verdad

```dax
EVALUATE
ROW(
  "escapado_encuentra_el_literal", CONTAINSSTRING("a*b", "a~*b"),
  "escapado_ya_no_es_comodin", CONTAINSSTRING("aXXXb", "a~*b"),
  "sin_escapar_encuentra_los_dos", CONTAINSSTRING("aXXXb", "a*b"),
  "interrogante_escapado", CONTAINSSTRING("a?b", "a~?b"),
  "interrogante_escapado_no_es_comodin", CONTAINSSTRING("aXb", "a~?b")
)
```

```result
escapado_encuentra_el_literal | escapado_ya_no_es_comodin | sin_escapar_encuentra_los_dos | interrogante_escapado | interrogante_escapado_no_es_comodin
True | False | True | True | False
```

Con `~` delante, el asterisco vuelve a ser un asterisco: encuentra `"a*b"` y **deja de
encontrar** `"aXXXb"`. Las dos primeras columnas son exactamente la distinción que la sección
anterior no podía hacer.

Esto cambia la recomendación práctica: para buscar un comodín literal **sin** perder la
insensibilidad a mayúsculas, la respuesta es `CONTAINSSTRING` con `~`, no
[`containsstringexact`](./containsstringexact.md) — que sí trata `*` como literal, pero a cambio
obliga a acertar la caja. Y ojo: el `~` es un escape **solo aquí**; en
`CONTAINSSTRINGEXACT` es un carácter más, medido en su ficha.

Consecuencia menos obvia: si el término lo teclea un usuario, un `*` suelto en su búsqueda **no
se comporta como texto**. Si quieres que lo sea, escápalo tú —`SUBSTITUTE([Buscado], "*",
"~*")`— antes de pasarlo.

Ver [`containsstringexact`](./containsstringexact.md) y [`contains`](./contains.md) para buscar
en tablas en vez de en texto.
