---
function: BITOR
model: ninguno
---

# BITOR — examples

## 1. Turning a flag on without touching the others

It is the complement of [`bitand`](./bitand.md): that one asks, this one sets. And it is
idempotent — turning the same flag on twice leaves the value unchanged.

```dax
EVALUATE
VAR Permisos = 5
RETURN
ROW(
  "valor",           Permisos,
  "enciende_el_2",   BITOR(Permisos, 2),
  "enciende_el_1",   BITOR(Permisos, 1),
  "dos_veces_el_2",  BITOR(BITOR(Permisos, 2), 2)
)
```

```result
valor | enciende_el_2 | enciende_el_1 | dos_veces_el_2
5 | 7 | 5 | 7
```

`enciende_el_1` returns 5 again because the bit was already set. Adding would not do: `5 + 1`
would give 6 and would have corrupted the mask.

## 2. That is why it is not done with an addition

The difference only shows up when the flag was already on — that is, in production and not in
testing.

```dax
EVALUATE
VAR Permisos = 5
RETURN
ROW(
  "bitor_con_4",  BITOR(Permisos, 4),
  "suma_con_4",   Permisos + 4,
  "bitor_con_2",  BITOR(Permisos, 2),
  "suma_con_2",   Permisos + 2
)
```

```result
bitor_con_4 | suma_con_4 | bitor_con_2 | suma_con_2
5 | 9 | 7 | 7
```

With bit 2 (which was missing) the two agree. With bit 4 (which was already there) they do not.

## 3. With negatives, a single zero rules

`-1` has every bit set, so it absorbs any `BITOR`.

```dax
EVALUATE
ROW(
  "con_menos_uno",  BITOR(5, -1),
  "menos_dos_y_1",  BITOR(-2, 1),
  "cero_y_cero",    BITOR(0, 0),
  "decimal",        BITOR(5.9, 2.9)
)
```

```result
con_menos_uno | menos_dos_y_1 | cero_y_cero | decimal
-1 | -1 | 0 | 7
```
