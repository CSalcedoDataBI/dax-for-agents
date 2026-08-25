---
function: MROUND
model: ninguno
---

# MROUND — ejemplos

## 1. Redondea al múltiplo más cercano

Es como se agrupan importes en tramos, o se ajustan tiempos a bloques de 15 minutos.

```dax
EVALUATE
ROW(
  "siete_a_tres",   MROUND(7, 3),
  "medio_sube",     MROUND(2.5, 1),
  "a_medios",       MROUND(2.3, 0.5),
  "a_veinticincos", MROUND(0.37, 0.25)
)
```

```result
siete_a_tres | medio_sube | a_medios | a_veinticincos
6 | 3 | 2.5 | 0.25
```

## 2. Si el número y el múltiplo tienen signos DISTINTOS, aborta

Esto no está en la firma y es la trampa de verdad: no devuelve un valor raro ni un blanco,
tumba la consulta. Y llega cuando aparece el primer importe negativo, no cuando se escribe.

```dax
EVALUATE ROW("signos_distintos", MROUND(-2.5, 1))
```

```result
ERROR: An argument of function 'MROUND' has the wrong data type or the result is too large or too small.
```

Con los dos negativos funciona:

```dax
EVALUATE
ROW(
  "ambos_negativos", MROUND(-7, -3),
  "negativo_medio",  MROUND(-2.5, -1),
  "positivo_normal", MROUND(7, 3)
)
```

```result
ambos_negativos | negativo_medio | positivo_normal
-6 | -3 | 6
```

Así que un `MROUND(columna, 100)` sobre una columna que puede traer negativos es una consulta
que funciona hasta que no.

## 3. Múltiplo cero da cero, no error

Es la excepción a lo anterior, y conviene saberla porque un múltiplo calculado que salga cero
no avisa: devuelve cero y el tramo entero desaparece.

```dax
EVALUATE
ROW(
  "multiplo_cero", MROUND(5, 0),
  "ceiling_cero",  CEILING(5, 0),
  "blanco",        MROUND(BLANK(), 3),
  "es_blanco",     ISBLANK(MROUND(BLANK(), 3))
)
```

```result
multiplo_cero | ceiling_cero | blanco | es_blanco
0 | 0 | (blank) | True
```

Ver [`ceiling`](./ceiling.md) y [`floor`](./floor.md), que hacen lo mismo pero siempre en una
dirección.
