---
function: GCD
model: ninguno
---

# GCD — ejemplos

## 1. Admite solo DOS argumentos, no los 255 de Excel

Esto es lo primero que rompe al portar una fórmula. En Excel `GCD` acepta hasta 255 números; en
DAX, dos.

```dax
EVALUATE ROW("tres_numeros", GCD(24, 36, 60))
```

```result
ERROR: Too many arguments were passed to the GCD function. The maximum argument count for the function is 2.
```

Con más de dos hay que anidar, y esto sí funciona porque el máximo común divisor es asociativo:

```dax
EVALUATE
ROW(
  "dos", GCD(24, 36),
  "tres_anidada", GCD(GCD(24, 36), 60),
  "coprimos", GCD(7, 9),
  "iguales", GCD(7, 7)
)
```

```result
dos | tres_anidada | coprimos | iguales
12 | 12 | 1 | 7
```

## 2. Redondea los decimales — Excel los trunca

Misma fórmula, distinta respuesta al migrar. Y `FACT`, en el mismo repertorio, sí trunca.

```dax
EVALUATE
ROW(
  "cuatro_coma_cuatro", GCD(4.4, 6),
  "cuatro_coma_cinco", GCD(4.5, 6),
  "cuatro_coma_seis", GCD(4.6, 6),
  "cuatro", GCD(4, 6),
  "cinco", GCD(5, 6)
)
```

```result
cuatro_coma_cuatro | cuatro_coma_cinco | cuatro_coma_seis | cuatro | cinco
2 | 1 | 1 | 2 | 1
```

4,4 se comporta como 4 y 4,5 como 5. Si trunca lo esperabas, 4,5 te da 1 donde creías tener 2.
Redondea tú antes con la regla que quieras y deja de depender de esta.

## 3. Los negativos abortan; el cero y el blanco no

```dax
EVALUATE
ROW(
  "cero", GCD(0, 5),
  "blanco", GCD(BLANK(), 5),
  "ambos_cero", GCD(0, 0),
  "negativo", IFERROR(GCD(-4, 6), "aborta")
)
```

```result
cero | blanco | ambos_cero | negativo
5 | 5 | 0 | aborta
```

`GCD(0, n)` es `n`, que es la definición correcta. El blanco entra como cero y se comporta
igual. Un negativo, en cambio, mata la consulta — y en datos reales el negativo llega antes que
el cero.

Ver [`lcm`](./lcm.md), que comparte estas reglas, y [`fact`](./fact.md), que no.
