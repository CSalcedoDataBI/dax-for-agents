---
function: IF.EAGER
model: ninguno
---

# IF.EAGER — ejemplos

## 1. Devuelve exactamente lo mismo que IF

Y eso es lo primero que hay que entender: **no existe para cambiar el resultado**. Si alguna
vez devuelve algo distinto de `IF`, es un error, no una función.

```dax
EVALUATE
ROW(
  "if_verdadero",       IF(1 = 1, "sí", "no"),
  "if_eager_verdadero", IF.EAGER(1 = 1, "sí", "no"),
  "if_falso",           IF(1 = 2, "sí", "no"),
  "if_eager_falso",     IF.EAGER(1 = 2, "sí", "no")
)
```

```result
if_verdadero | if_eager_verdadero | if_falso | if_eager_falso
sí | sí | no | no
```

## 2. La diferencia es CUÁNDO se evalúan las ramas

`IF` puede saltarse la rama que no se toma. `IF.EAGER` evalúa las dos siempre. La razón de
existir es el plan de consulta: a veces evaluar las dos de golpe sale más barato que ramificar.

**Esa diferencia no se ve en el resultado**, y este ejemplo lo enseña precisamente así: las
dos formas devuelven lo mismo aunque la rama descartada contenga una división por cero
protegida con `DIVIDE`. Quien busque una diferencia de valor no la va a encontrar, y eso es
lo que hay que saber antes de cambiar una por otra.

```dax
EVALUATE
ROW(
  "if_rama_muerta",       IF(1 = 1, "tomada", DIVIDE(1, 0)),
  "if_eager_rama_muerta", IF.EAGER(1 = 1, "tomada", DIVIDE(1, 0)),
  "ambas_validas",        IF.EAGER(1 = 2, DIVIDE(10, 2), DIVIDE(20, 2))
)
```

```result
if_rama_muerta | if_eager_rama_muerta | ambas_validas
tomada | tomada | 10
```

## 3. La rama no tomada sí puede costarte

Si la rama descartada es cara, `IF.EAGER` la paga igual. Aquí las dos ramas devuelven lo
mismo y la diferencia está en el trabajo, no en el número — por eso este ejemplo enseña
valores idénticos: **es la prueba de que lo único que cambia es el coste**.

```dax
EVALUATE
ROW(
  "if_barato",       IF(1 = 1, 1, SUMX(GENERATESERIES(1, 100000), [Value])),
  "if_eager_caro",   IF.EAGER(1 = 1, 1, SUMX(GENERATESERIES(1, 100000), [Value])),
  "lo_que_costaba",  SUMX(GENERATESERIES(1, 100000), [Value])
)
```

```result
if_barato | if_eager_caro | lo_que_costaba
1 | 1 | 5000050000
```

Para medir esa diferencia hace falta volumen y el motor en frío: eso está en
[`lab/rendimiento`](../../../lab/rendimiento/), no aquí.
