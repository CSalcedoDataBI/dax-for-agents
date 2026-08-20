---
function: CONCATENATE
model: ninguno
---

# CONCATENATE — ejemplos

## 1. Solo dos argumentos, como AND y OR

Con tres aborta. Para encadenar está el operador `&`, que además se lee mejor.

```dax
EVALUATE
ROW(
  "dos",       CONCATENATE("Power", " BI"),
  "anidada",   CONCATENATE("Power", CONCATENATE(" ", "BI")),
  "operador",  "Power" & " " & "BI"
)
```

```result
dos | anidada | operador
Power BI | Power BI | Power BI
```

```dax
EVALUATE ROW("tres", CONCATENATE("a", "b", "c"))
```

```result
ERROR: Too many arguments were passed to the CONCATENATE function. The maximum argument count for the function is 2.
```

## 2. Un blanco junto a texto desaparece; dos blancos siguen siendo blanco

Es la mitad de la regla que uno espera. Al lado de texto, el blanco se comporta como cadena
vacía: desaparece sin dejar rastro, y con él la señal de que faltaba un dato. Pero
`CONCATENATE(BLANK(), BLANK())` **no** devuelve cadena vacía: devuelve blanco.

```dax
EVALUATE
ROW(
  "blanco_delante", "[" & CONCATENATE(BLANK(), "hola") & "]",
  "blanco_detras",  "[" & CONCATENATE("hola", BLANK()) & "]",
  "los_dos",        "[" & CONCATENATE(BLANK(), BLANK()) & "]",
  "es_blanco",      ISBLANK(CONCATENATE(BLANK(), BLANK()))
)
```

```result
blanco_delante | blanco_detras | los_dos | es_blanco
[hola] | [hola] | [] | True
```

Un nombre completo montado con `&` sobre un apellido ausente sale con el espacio de más y
nadie se entera. Y la fila entera solo desaparece del visual si **todo** venía en blanco.

## 3. Convierte los números a texto usando la cultura del modelo

Lo que sale no es lo que muestra el informe: el formato de la medida no interviene.

```dax
EVALUATE
ROW(
  "entero",   CONCATENATE("n=", 1234),
  "decimal",  CONCATENATE("x=", 1.5),
  "negativo", CONCATENATE("t=", -3),
  "booleano", CONCATENATE("b=", TRUE())
)
```

```result
entero | decimal | negativo | booleano
n=1234 | x=1,5 | t=-3 | b=TRUE
```

Para controlar cómo se escribe el número hay que decirlo con [`format`](./format.md) — y
entonces el resultado deja de ordenarse como número, que es la trampa de esa ficha.

Ver [`concatenatex`](./concatenatex.md) para unir los valores de una **columna**.
