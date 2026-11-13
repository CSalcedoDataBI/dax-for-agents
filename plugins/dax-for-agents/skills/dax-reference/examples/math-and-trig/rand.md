---
function: RAND
model: ninguno
---

# RAND — examples

> The `result` blocks on this card assert **properties** and not values: `RAND` never returns the
> same thing twice, so a specific number could not be checked again.

## 1. Every call returns a different value, even on the same row

This is what breaks measures that call `RAND` more than once believing they are talking about the
same number.

```dax
EVALUATE
ROW(
  "dentro_del_rango", RAND() >= 0 && RAND() < 1,
  "dos_llamadas_difieren", RAND() <> RAND(),
  "nunca_es_blanco", ISBLANK(RAND())
)
```

```result
dentro_del_rango | dos_llamadas_difieren | nunca_es_blanco
True | True | False
```

The interval is **[0, 1)**: zero can come out and one cannot. And `RAND()` never returns blank,
unlike almost everything else in this category.

## 2. A variable freezes it; repeating the call does not

If you need to use the same random number twice — compare it against a threshold and also show it
— it has to go through a `VAR`.

```dax
EVALUATE
VAR Sorteo = RAND()
RETURN
ROW(
  "la_variable_es_estable", Sorteo = Sorteo,
  "la_funcion_no", RAND() <> RAND(),
  "umbral_coherente", (Sorteo < 0.5) = (Sorteo < 0.5)
)
```

```result
la_variable_es_estable | la_funcion_no | umbral_coherente
True | True | True
```

Without the `VAR`, `IF(RAND() < 0.5, RAND(), 0)` draws **twice**: once to decide and once for the
value it returns.

## 3. It recalculates, so it is no good for a stable column

`RAND` is non-deterministic. In a measure it is re-evaluated every time the visual refreshes; in
a calculated column it is fixed at refresh, but changes at the next one. For a stable identifier
it will not do.

```dax
EVALUATE
VAR Muestra = GENERATESERIES(1, 200, 1)
VAR ConSorteo = ADDCOLUMNS(Muestra, "r", RAND())
RETURN
ROW(
  "todos_en_rango", COUNTROWS(FILTER(ConSorteo, [r] < 0 || [r] >= 1)),
  "hay_variedad", COUNTROWS(DISTINCT(SELECTCOLUMNS(ConSorteo, "v", [r]))) > 190,
  "cuantos", COUNTROWS(ConSorteo)
)
```

```result
todos_en_rango | hay_variedad | cuantos
(blank) | True | 200
```

None of the 200 rows falls outside the interval — the first column counts the ones that do and
gives blank — and nearly all are distinct. If you want reproducibility, the seed has to come from
the data: something like `MOD(hash_of_the_key, n)` written by hand.

See [`randbetween`](./randbetween.md).
