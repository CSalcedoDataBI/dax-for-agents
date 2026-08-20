---
function: CEILING
model: ninguno
---

# CEILING — ejemplos

## 1. Con significancia positiva va hacia MÁS infinito

Así que con un negativo se acerca al cero — al revés que [`roundup`](./roundup.md), que se
aleja. Las dos suenan a «hacia arriba» y no coinciden.

```dax
EVALUATE
ROW(
  "positivo",  CEILING(2.1, 1),
  "negativo",  CEILING(-2.1, 1),
  "roundup",   ROUNDUP(-2.1, 0),
  "a_medios",  CEILING(2.3, 0.5)
)
```

```result
positivo | negativo | roundup | a_medios
3 | -2 | -3 | 2.5
```

## 2. Con significancia NEGATIVA cambia de dirección, y ahí se separa de ISO.CEILING

Es la única diferencia real entre las dos, y solo aparece con el signo cruzado.

```dax
EVALUATE
ROW(
  "ceiling_sig_neg", CEILING(-2.3, -1),
  "iso_sig_neg",     ISO.CEILING(-2.3, -1),
  "ceiling_sig_pos", CEILING(-2.3, 1),
  "iso_sig_pos",     ISO.CEILING(-2.3, 1)
)
```

```result
ceiling_sig_neg | iso_sig_neg | ceiling_sig_pos | iso_sig_pos
-3 | -2 | -2 | -2
```

`ISO.CEILING` **siempre** va hacia más infinito, pase lo que pase con el signo de la
significancia. `CEILING` no. Si el múltiplo sale de un cálculo y puede ser negativo, esa
diferencia es un descuadre silencioso.

## 3. Significancia cero da cero, no error

Igual que [`mround`](./mround.md), y con el mismo riesgo: un múltiplo calculado que salga
cero se lleva el valor por delante sin avisar.

```dax
EVALUATE
ROW(
  "sig_cero",  CEILING(5, 0),
  "blanco",    CEILING(BLANK(), 1),
  "es_blanco", ISBLANK(CEILING(BLANK(), 1)),
  "ya_multiplo", CEILING(6, 3)
)
```

```result
sig_cero | blanco | es_blanco | ya_multiplo
0 | (blank) | True | 6
```
