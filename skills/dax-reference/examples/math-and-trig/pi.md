---
function: PI
model: ninguno
---

# PI — ejemplos

## 1. No lleva argumentos, pero los paréntesis son obligatorios

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

`PI()` sin paréntesis no compila: DAX lo leería como el nombre de una columna. La última
columna es la definición operativa — π radianes **son** 180 grados.

## 2. Es más preciso que escribir 3,1416, y la diferencia se nota antes de lo que parece

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

Con radio 1000 la aproximación ya se desvía 7,3 unidades. (La primera columna sale como
-0,000007 porque el informe imprime seis decimales; el valor real es -0,0000073464.) Nunca hay motivo para escribir la
constante a mano.

## 3. Donde de verdad se usa: convertir a radianes sin `RADIANS`

Las funciones trigonométricas de DAX toman **radianes**. `PI()` es la forma de escribir la
conversión cuando el ángulo viene en fracciones de vuelta y no en grados.

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

Las dos primeras son la misma cuenta. Si el ángulo llega en grados desde los datos,
[`radians`](./radians.md) se lee mejor; si llega como fracción de circunferencia, `PI()` es
más directo.

Ver [`radians`](./radians.md), [`degrees`](./degrees.md) y [`sqrtpi`](./sqrtpi.md).
