---
function: RADIANS
model: ninguno
---

# RADIANS — ejemplos

## 1. Sin ella, las funciones trigonométricas leen los grados como radianes

Y no fallan: devuelven un número perfectamente creíble que está mal.

```dax
EVALUATE
ROW(
  "sen_90_bien", ROUND(SIN(RADIANS(90)), 10),
  "sen_90_mal", ROUND(SIN(90), 6),
  "cos_180_bien", ROUND(COS(RADIANS(180)), 10),
  "cos_180_mal", ROUND(COS(180), 6)
)
```

```result
sen_90_bien | sen_90_mal | cos_180_bien | cos_180_mal
1 | 0.893997 | -1 | -0.59846
```

`SIN(90)` devuelve 0,894 porque 90 **radianes** son catorce vueltas y pico. Ningún error, ningún
aviso: solo la cifra equivocada en el informe.

## 2. Es `x × π / 180`, y el ida y vuelta cierra

```dax
EVALUATE
ROW(
  "rad_180", ROUND(RADIANS(180), 10),
  "pi", ROUND(PI(), 10),
  "rad_90", ROUND(RADIANS(90), 10),
  "escrita_a_mano", ROUND(90 * PI() / 180, 10),
  "ida_y_vuelta", ROUND(DEGREES(RADIANS(37)), 10)
)
```

```result
rad_180 | pi | rad_90 | escrita_a_mano | ida_y_vuelta
3.141593 | 3.141593 | 1.570796 | 1.570796 | 37
```

Escribirla a mano da lo mismo; `RADIANS` solo deja claro qué estás haciendo, que en una medida
larga vale más que ahorrar caracteres.

## 3. No tiene dominio, y el blanco sale en blanco

```dax
EVALUATE
ROW(
  "blanco", RADIANS(BLANK()),
  "es_blanco", ISBLANK(RADIANS(BLANK())),
  "cero", RADIANS(0),
  "negativo", ROUND(RADIANS(-90), 10),
  "mil_grados", ROUND(RADIANS(1000), 6)
)
```

```result
blanco | es_blanco | cero | negativo | mil_grados
(blank) | True | 0 | -1.570796 | 17.453293
```

Acepta cualquier número. Mil grados son casi tres vueltas, y `RADIANS` no las normaliza — las
funciones trigonométricas tampoco lo necesitan, porque son periódicas.

Ver [`degrees`](./degrees.md), su inversa, y [`pi`](./pi.md).
