---
function: ABS
model: ninguno
---

# ABS — ejemplos

## 1. Lo previsible, y el texto que se convierte solo

```dax
EVALUATE
ROW(
  "negativo", ABS(-7.5),
  "positivo", ABS(7.5),
  "cero", ABS(0),
  "texto", ABS("-3")
)
```

```result
negativo | positivo | cero | texto
7.5 | 7.5 | 0 | 3
```

La cuarta columna es una conversión implícita: la cadena `"-3"` se lee como número. Funciona,
pero depende de la cultura del modelo — mira [`convert`](./convert.md), donde `"1.5"` sale
**15** en un modelo en español.

## 2. Un blanco sale en blanco, y aun así vale cero

```dax
EVALUATE
ROW(
  "abs_blanco", ABS(BLANK()),
  "es_blanco", ISBLANK(ABS(BLANK())),
  "compara_con_cero", ABS(BLANK()) = 0,
  "abs_cero", ABS(0),
  "cero_es_blanco", ISBLANK(ABS(0))
)
```

```result
abs_blanco | es_blanco | compara_con_cero | abs_cero | cero_es_blanco
(blank) | True | True | 0 | False
```

Las dos afirmaciones del medio parecen contradecirse y no lo hacen. El blanco entra como cero,
`ABS(0)` es cero, y un cero que viene de un blanco vuelve a salir como blanco. Un `0` escrito a
mano devuelve un cero que **no** está en blanco.

Importa al filtrar: `FILTER(T, ABS(T[x]) = 0)` se queda también con las filas donde `x` está
vacío, no solo con las que valen cero.

## 3. Es lo que separa «desviación» de «error»

El uso real de `ABS` casi siempre es este: una diferencia cuyo signo no interesa, y una suma
que sin ella se cancela sola.

```dax
EVALUATE
VAR Desviaciones = { -3, 5, -2 }
RETURN
ROW(
  "suma_con_signo", SUMX(Desviaciones, [Value]),
  "suma_absoluta", SUMX(Desviaciones, ABS([Value])),
  "media_absoluta", ROUND(AVERAGEX(Desviaciones, ABS([Value])), 6)
)
```

```result
suma_con_signo | suma_absoluta | media_absoluta
0 | 10 | 3.333333
```

La primera columna dice **0** y no significa que no haya error: significa que los errores se
compensaron. Es la diferencia entre un sesgo y una magnitud.

Ver [`sign`](./sign.md), que responde a la otra mitad de la pregunta.
