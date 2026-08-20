---
function: DEGREES
model: ninguno
---

# DEGREES — ejemplos

## 1. Convierte la SALIDA de las funciones trigonométricas, que devuelven radianes

Ese es su uso real. `ATAN`, `ACOS` y compañía no devuelven grados, y un informe que enseñe
ángulos los necesita.

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

Una pendiente del 100 % son 45 grados, no 90. Es el tipo de cifra que se publica mal cuando se
olvida la conversión.

## 2. Un radián son 57,3 grados, y el ida y vuelta cuadra exacto

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

Las dos últimas columnas cierran el círculo sin residuo visible, que no es lo habitual en coma
flotante — compara con [`sqrt`](./sqrt.md), donde `SQRT(2) * SQRT(2)` **no** vuelve a 2.

## 3. El blanco sale en blanco, y el negativo pasa sin quejarse

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

No hay dominio: cualquier número vale, y el resultado puede pasarse de 360 sin que nadie lo
normalice. Si necesitas el ángulo dentro de una vuelta, el `MOD(x, 360)` lo escribes tú — con
el cuidado que pide [`mod`](./mod.md) si el valor puede ser negativo.

Ver [`radians`](./radians.md), su inversa, y [`pi`](./pi.md).
