---
function: ROUNDDOWN
model: ninguno
---

# ROUNDDOWN — ejemplos

## 1. «Abajo» significa HACIA CERO, no hacia menos infinito

Es la confusión que produce cuentas descuadradas con importes negativos. `ROUNDDOWN(-2.7)` no
es `-3`: es `-2`, porque se acerca al cero. Quien quiera el suelo de verdad necesita
[`int`](./int.md).

```dax
EVALUATE
ROW(
  "positivo",     ROUNDDOWN(2.7, 0),
  "negativo",     ROUNDDOWN(-2.7, 0),
  "int_negativo", INT(-2.7),
  "trunc_negativo", TRUNC(-2.7)
)
```

```result
positivo | negativo | int_negativo | trunc_negativo
2 | -2 | -3 | -2
```

Con positivos las tres coinciden. Con negativos, `INT` se separa de las otras dos — y solo se
nota cuando llega el primer importe negativo.

## 2. No mira el medio: siempre corta

A diferencia de [`round`](./round.md), aquí `.5` no decide nada. Es truncar en la posición que
le digas.

```dax
EVALUATE
ROW(
  "medio_arriba", ROUND(2.5, 0),
  "medio_abajo",  ROUNDDOWN(2.5, 0),
  "casi_tres",    ROUNDDOWN(2.999, 0),
  "dos_decimales", ROUNDDOWN(2.999, 2)
)
```

```result
medio_arriba | medio_abajo | casi_tres | dos_decimales
3 | 2 | 2 | 2.99
```

## 3. Decimales negativos, y el blanco

```dax
EVALUATE
ROW(
  "a_decenas",  ROUNDDOWN(1999, -1),
  "a_millares", ROUNDDOWN(1999, -3),
  "blanco",     ROUNDDOWN(BLANK(), 2),
  "es_blanco",  ISBLANK(ROUNDDOWN(BLANK(), 2))
)
```

```result
a_decenas | a_millares | blanco | es_blanco
1990 | 1000 | (blank) | True
```

`ROUNDDOWN(1999, -3)` da 1000: para agrupar por magnitud es lo que se quiere, y para calcular
un total no lo es.

Ver [`roundup`](./roundup.md), que es su espejo y tiene la misma confusión al revés.
