---
function: CONTAINSSTRINGEXACT
model: ninguno
---

# CONTAINSSTRINGEXACT — ejemplos

## 1. Distingue mayúsculas, que es lo que promete el nombre

```dax
EVALUATE
ROW(
  "minusculas", CONTAINSSTRINGEXACT("Bicicleta", "bici"),
  "capitalizado", CONTAINSSTRINGEXACT("Bicicleta", "Bici"),
  "lo_mismo_con_containsstring", CONTAINSSTRING("Bicicleta", "bici"),
  "acento", CONTAINSSTRINGEXACT("Almacén", "Almacen")
)
```

```result
minusculas | capitalizado | lo_mismo_con_containsstring | acento
False | True | True | False
```

Las dos primeras columnas son la diferencia anunciada. La tercera la pone al lado de
[`containsstring`](./containsstring.md), que sí encuentra `"bici"`. La cuarta recuerda que el
acento **también** cuenta aquí — igual que en la otra, que tampoco los ignora.

## 2. La diferencia que no anuncia: aquí `*` y `?` NO son comodines

Las dos funciones están documentadas como si solo cambiara la sensibilidad a mayúsculas. Son
dos diferencias, no una, y esta segunda cambia el resultado de una búsqueda entera.

```dax
EVALUATE
ROW(
  "exacto_con_asterisco", CONTAINSSTRINGEXACT("aXXXb", "a*b"),
  "containsstring_con_asterisco", CONTAINSSTRING("aXXXb", "a*b"),
  "exacto_asterisco_literal", CONTAINSSTRINGEXACT("a*b", "a*b"),
  "exacto_con_interrogante", CONTAINSSTRINGEXACT("aXb", "a?b"),
  "exacto_interrogante_literal", CONTAINSSTRINGEXACT("a?b", "a?b")
)
```

```result
exacto_con_asterisco | containsstring_con_asterisco | exacto_asterisco_literal | exacto_con_interrogante | exacto_interrogante_literal
False | True | True | False | True
```

Las dos primeras columnas son la misma llamada con la misma aguja sobre el mismo pajar, y
devuelven lo contrario. En `CONTAINSSTRINGEXACT` el `*` es un asterisco y nada más: encuentra
`"a*b"` porque ahí hay un asterisco de verdad, y no encuentra `"aXXXb"` porque ahí no lo hay.

Eso la hace cómoda para **buscar caracteres que son comodines**: referencias con `*`, códigos
con `?`, cualquier campo donde esos símbolos sean datos.

Lo que **no** es cierto es que sea la única forma de hacerlo. `CONTAINSSTRING` acepta el escape
`~`, y con él busca el carácter literal sin renunciar a ignorar mayúsculas — está medido en
[`containsstring`](./containsstring.md), sección 4. La elección real es esta:

| quieres | usa |
|---|---|
| comodín literal, **ignorando** mayúsculas | `CONTAINSSTRING` con `~*` / `~?` |
| comodín literal, **distinguiendo** mayúsculas | `CONTAINSSTRINGEXACT`, sin escapar nada |

Y el `~` **no** es un escape aquí. Lo siguiente lo mide, junto al truco de normalizar con
[`upper`](../text/upper.md):

```dax
EVALUATE
ROW(
  "tilde_no_escapa_aqui", CONTAINSSTRINGEXACT("a*b", "a~*b"),
  "upper_en_los_dos_lados", CONTAINSSTRINGEXACT(UPPER("Bicicleta"), UPPER("bici")),
  "pero_upper_no_arregla_el_acento", CONTAINSSTRINGEXACT(UPPER("Almacén"), UPPER("almacen"))
)
```

```result
tilde_no_escapa_aqui | upper_en_los_dos_lados | pero_upper_no_arregla_el_acento
False | True | False
```

La primera columna es falsa porque aquí `"a~*b"` se busca tal cual, tilde incluida, y en
`"a*b"` no está. La segunda confirma que normalizar con `UPPER` a ambos lados sí devuelve la
insensibilidad a mayúsculas. La tercera avisa de hasta dónde llega ese arreglo: **el acento
sigue sin perdonarse**, porque `UPPER` cambia la caja, no los diacríticos.

## 3. Una aguja en blanco también encuentra siempre

```dax
EVALUATE
ROW(
  "aguja_vacia", CONTAINSSTRINGEXACT("Bicicleta", ""),
  "aguja_blanca", CONTAINSSTRINGEXACT("Bicicleta", BLANK()),
  "acento_igual", CONTAINSSTRINGEXACT("Almacén", "macén"),
  "trozo_en_medio", CONTAINSSTRINGEXACT("Bicicleta", "cicle")
)
```

```result
aguja_vacia | aguja_blanca | acento_igual | trozo_en_medio
True | True | True | True
```

Hereda el mismo agujero que [`containsstring`](./containsstring.md): un término de búsqueda
vacío o en blanco devuelve verdadero para todo, así que el filtro deja de filtrar sin decirlo.

Y hereda también su matiz: **`ISBLANK` no sirve de guardia aquí**, porque `ISBLANK("")` es
falso y la cadena vacía se cuela igual. Usa `IF(LEN([Buscado]) > 0, ...)`, que cubre los dos
casos — está medido en [`containsstring`](./containsstring.md), sección 3.

Las dos últimas confirman lo esperado: encuentra en cualquier posición, no solo al principio.

Ver [`containsstring`](./containsstring.md) y [`contains`](./contains.md).
