---
function: BITAND
model: ninguno
---

# BITAND — ejemplos

## 1. Para qué sirve de verdad: preguntar si un permiso está puesto

El caso real de las funciones de bits es una columna donde cada bit es una bandera. `BITAND`
con la máscara responde «¿está encendida esta?» sin desmontar el número.

```dax
EVALUATE
VAR Permisos = 13
RETURN
ROW(
  "valor",          Permisos,
  "tiene_bit_1",    BITAND(Permisos, 1),
  "tiene_bit_2",    BITAND(Permisos, 2),
  "tiene_bit_4",    BITAND(Permisos, 4),
  "tiene_bit_8",    BITAND(Permisos, 8)
)
```

```result
valor | tiene_bit_1 | tiene_bit_2 | tiene_bit_4 | tiene_bit_8
13 | 1 | 0 | 4 | 8
```

13 es `1101` en binario: bits 1, 4 y 8 puestos, el 2 no. El resultado **no es cierto o falso**,
es el valor de la máscara o cero — y por eso hay que compararlo, no usarlo tal cual dentro de
un `IF`.

## 2. Con negativos entra el complemento a dos

Los enteros de DAX son de 64 bits con signo, así que `-1` tiene todos los bits a uno y actúa
como elemento neutro.

```dax
EVALUATE
ROW(
  "menos_uno_con_5",  BITAND(-1, 5),
  "menos_dos_con_5",  BITAND(-2, 5),
  "negativo_negativo", BITAND(-4, -2),
  "cero_con_todo",    BITAND(0, -1)
)
```

```result
menos_uno_con_5 | menos_dos_con_5 | negativo_negativo | cero_con_todo
5 | 4 | -4 | 0
```

## 3. Los decimales se REDONDEAN antes de operar, no se truncan

Esto se escribió al revés y lo corrigió el motor. La intuición dice «truncar», como hacen los
operadores de bits en casi todos los lenguajes. DAX **redondea**: `12.9` entra como `13`, no
como `12`.

```dax
EVALUATE
ROW(
  "entero",     BITAND(12, 10),
  "decimal",    BITAND(12.9, 10.9),
  "negativo_decimal", BITAND(-12.9, 10),
  "casi_uno",   BITAND(0.9, 1)
)
```

```result
entero | decimal | negativo_decimal | casi_uno
8 | 9 | 2 | 1
```

Ver [`bitor`](./bitor.md) para encender una bandera y [`bitxor`](./bitxor.md) para
cambiarla.
