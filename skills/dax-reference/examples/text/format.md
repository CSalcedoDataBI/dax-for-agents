---
function: FORMAT
model: ninguno
---

# FORMAT — ejemplos

> La nota de campo [`format`](../../notes/format.md) cubre lo importante: devuelve **texto**,
> y con eso se pierde el orden numérico. Aquí van las cadenas de formato y sus bordes.

## 1. Los formatos con nombre son los que hay que usar

Son estables y se traducen con la cultura del modelo. Los personalizados se escriben a mano y
son donde aparecen las sorpresas.

```dax
EVALUATE
ROW(
  "general",   FORMAT(1234.567, "General Number"),
  "fijo",      FORMAT(1234.567, "Fixed"),
  "estandar",  FORMAT(1234.567, "Standard"),
  "porcentaje", FORMAT(0.1234, "Percent")
)
```

```result
general | fijo | estandar | porcentaje
1234,567 | 1234,57 | 1.234,57 | 12,34%
```

`Percent` **multiplica por 100**: al valor ya convertido a porcentaje se le va otra vez la
coma, y sale un número cien veces mayor que nadie revisa.

## 2. Un formato personalizado con secciones cambia según el signo

Separadas por `;` van el positivo, el negativo y el cero. Es potente y es donde se cuelan los
errores, porque solo se ven con datos de los tres tipos.

```dax
EVALUATE
ROW(
  "positivo", FORMAT(1234, "#,##0;(#,##0);cero"),
  "negativo", FORMAT(-1234, "#,##0;(#,##0);cero"),
  "cero",     FORMAT(0, "#,##0;(#,##0);cero"),
  "blanco",   FORMAT(BLANK(), "#,##0;(#,##0);cero")
)
```

```result
positivo | negativo | cero | blanco
1.234 | (1.234) | cero | (blank)
```

El blanco **no** entra por la sección del cero: sigue siendo blanco. Es la buena noticia — «sin
dato» y «cero» no acaban escritos igual — y a la vez el motivo por el que una tercera sección
escrita para cubrir los huecos no los cubre. Para eso hace falta `COALESCE` antes del
`FORMAT`, no una sección más.

## 3. Una cadena de formato que no existe no da error

Devuelve el texto de la cadena tal cual, o algo parecido. No hay validación, así que una
errata sobrevive hasta que alguien mira el visual.

```dax
EVALUATE
ROW(
  "valido",       FORMAT(1234.5, "#,##0.00"),
  "errata",       FORMAT(1234.5, "#,##O.OO"),
  "inventado",    FORMAT(1234.5, "no soy un formato"),
  "fecha_sobre_numero", FORMAT(1234.5, "yyyy-mm-dd")
)
```

```result
valido | errata | inventado | fecha_sobre_numero
1.234,50 | 1.235O,OO | 0o 0o138 u0 for5ato | 1903-05-18
```

El último es el más traicionero: un número interpretado como fecha da una fecha creíble, no
un error.
