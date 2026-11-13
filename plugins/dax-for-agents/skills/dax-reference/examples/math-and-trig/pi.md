---
function: PI
model: ninguno
---

# PI — examples

## 1. It takes no arguments, but the parentheses are compulsory

```dax
EVALUATE
ROW(
  "pi", ROUND(PI(), 10),
  "dos_pi", ROUND(PI() * 2, 10),
  "medio_pi", ROUND(PI() / 2, 10),
  "grados", DEGREES(PI())
)
```

```result
pi | dos_pi | medio_pi | grados
3.141593 | 6.283185 | 1.570796 | 180
```

`PI()` without parentheses does not compile: DAX would read it as a column name. The last column
is the working definition — π radians **are** 180 degrees.

## 2. It is more precise than typing 3.1416, and the difference shows sooner than you would think

```dax
EVALUATE
VAR Aproximado = 3.1416
RETURN
ROW(
  "diferencia", ROUND(PI() - Aproximado, 10),
  "area_r_1000_real", ROUND(PI() * POWER(1000, 2), 4),
  "area_r_1000_aprox", ROUND(Aproximado * POWER(1000, 2), 4),
  "error_absoluto", ROUND(ABS(PI() * POWER(1000, 2) - Aproximado * POWER(1000, 2)), 4)
)
```

```result
diferencia | area_r_1000_real | area_r_1000_aprox | error_absoluto
-0.000007 | 3141592.6536 | 3141600 | 7.3464
```

At radius 1000 the approximation is already off by 7.3 units. (The first column prints as
-0.000007 because the report shows six decimals; the real value is -0.0000073464.) There is never
a reason to write the constant by hand.

## 3. Where it is really used: converting to radians without `RADIANS`

DAX's trigonometric functions take **radians**. `PI()` is how you write the conversion when the
angle arrives as a fraction of a turn rather than in degrees.

```dax
EVALUATE
ROW(
  "sen_90_grados", ROUND(SIN(PI() / 2), 10),
  "sen_con_radians", ROUND(SIN(RADIANS(90)), 10),
  "cos_180", ROUND(COS(PI()), 10),
  "vuelta_completa", ROUND(SIN(2 * PI()), 10)
)
```

```result
sen_90_grados | sen_con_radians | cos_180 | vuelta_completa
1 | 1 | -1 | 0
```

The first two are the same sum. If the angle arrives in degrees from the data,
[`radians`](./radians.md) reads better; if it arrives as a fraction of a circumference, `PI()` is
more direct.

See [`radians`](./radians.md), [`degrees`](./degrees.md) and [`sqrtpi`](./sqrtpi.md).
