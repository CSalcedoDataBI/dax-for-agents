---
function: LEN
model: ninguno
---

# LEN — ejemplos

## 1. LEN de un blanco es BLANCO, pero compara igual que 0

Lo escribí al revés y lo corrigió el motor: `LEN(BLANK())` **no** devuelve 0, devuelve blanco.
Y aun así `LEN(BLANK()) = 0` es verdadero, porque `=` iguala el blanco a su valor neutro. Las
dos cosas a la vez son la trampa.

```dax
EVALUATE
ROW(
  "len_blanco",       LEN(BLANK()),
  "es_blanco",        ISBLANK(LEN(BLANK())),
  "len_cadena_vacia", LEN(""),
  "compara_con_cero", LEN(BLANK()) = 0,
  "estricto",         LEN(BLANK()) == 0
)
```

```result
len_blanco | es_blanco | len_cadena_vacia | compara_con_cero | estricto
(blank) | True | 0 | True | False
```

Así que `LEN(columna) = 0` **no distingue** «vacío» de «sin dato»: los dos pasan. Para
distinguirlos hace falta `ISBLANK`, o el `==` estricto.

## 2. Sobre un número, cuenta los caracteres de su representación

`LEN` convierte a texto antes de contar, y esa conversión usa la **cultura del modelo**, no
el formato de la medida. Este modelo es `es-ES`, así que el separador decimal es la coma.

```dax
EVALUATE
ROW(
  "entero",    LEN(12345),
  "decimal",   LEN(1.5),
  "negativo",  LEN(-42),
  "cero_coma", LEN(0.50)
)
```

```result
entero | decimal | negativo | cero_coma
5 | 3 | 3 | 3
```

`0.50` mide 3 y no 4: el cero final no existe en el número, solo en cómo se escribió.

## 3. Cuenta unidades de código, no caracteres visibles

Con emoji la cuenta deja de coincidir con lo que se ve: uno fuera del plano básico ocupa
**dos**. Los acentos y la eñe, en cambio, ocupan uno.

```dax
EVALUATE
ROW(
  "con_acento",  LEN("café"),
  "con_enye",    LEN("año"),
  "emoji",       LEN(UNICHAR(128512)),
  "texto_emoji", LEN("ok" & UNICHAR(128512))
)
```

```result
con_acento | con_enye | emoji | texto_emoji
4 | 3 | 2 | 4
```

Si cortas con [`left`](./left.md) o [`mid`](./mid.md) contando a ojo, ahí es donde se parte
un carácter por la mitad.
