---
function: DEGREES
model: ninguno
---

# DEGREES — examples

## 1. It converts the OUTPUT of the trigonometric functions, which return radians

That is its real use. `ATAN`, `ACOS` and company do not return degrees, and a report showing
angles needs them.

```dax
EVALUATE
ROW(
  "atan_1_radianes", ROUND(ATAN(1), 6),
  "atan_1_grados", ROUND(DEGREES(ATAN(1)), 6),
  "acos_0_grados", ROUND(DEGREES(ACOS(0)), 6),
  "pendiente_100pc", ROUND(DEGREES(ATAN(1)), 2)
)
```

```result
atan_1_radianes | atan_1_grados | acos_0_grados | pendiente_100pc
0.785398 | 45 | 90 | 45
```

A 100% gradient is 45 degrees, not 90. It is the kind of figure that gets published wrong when
the conversion is forgotten.

## 2. One radian is 57.3 degrees, and the round trip closes exactly

```dax
EVALUATE
ROW(
  "un_radian", ROUND(DEGREES(1), 6),
  "pi_radianes", DEGREES(PI()),
  "ida_y_vuelta", ROUND(DEGREES(RADIANS(37)), 10),
  "vuelta_e_ida", ROUND(RADIANS(DEGREES(1.234)), 10)
)
```

```result
un_radian | pi_radianes | ida_y_vuelta | vuelta_e_ida
57.29578 | 180 | 37 | 1.234
```

The last two columns close the circle with no visible remainder, which is not the norm in
floating point — compare with [`sqrt`](./sqrt.md), where `SQRT(2) * SQRT(2)` does **not** come
back to 2.

## 3. The blank comes out blank, and a negative goes through without complaint

```dax
EVALUATE
ROW(
  "blanco", DEGREES(BLANK()),
  "es_blanco", ISBLANK(DEGREES(BLANK())),
  "cero", DEGREES(0),
  "negativo", ROUND(DEGREES(-PI()), 6),
  "mas_de_una_vuelta", ROUND(DEGREES(10), 4)
)
```

```result
blanco | es_blanco | cero | negativo | mas_de_una_vuelta
(blank) | True | 0 | -180 | 572.9578
```

There is no domain: any number is fine, and the result can exceed 360 with nobody normalising it.
If you need the angle within one turn, you write the `MOD(x, 360)` yourself — with the care
[`mod`](./mod.md) calls for if the value can be negative.

See [`radians`](./radians.md), its inverse, and [`pi`](./pi.md).
