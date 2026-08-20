# rendimiento — qué cuesta de verdad sobre dos millones de filas

Este escenario existe porque sobre Contoso no se podía medir nada: 126.524 filas se
resuelven en milisegundos y cualquier comparación caía dentro del ruido.

Y salió lo contrario de lo que se fue a buscar. Se construyó para demostrar que `FILTER`
sobre una tabla entera es caro —el consejo que todo el mundo repite— y **no lo es**. Lo que
cuesta es otra cosa.

## El modelo

Una tabla, `Ventas`, con **2.000.000 de filas**. En los otros dos escenarios sintéticos los
datos son cinco o siete filas elegidas a mano porque la anomalía se lee de un vistazo; aquí el
volumen **es** el escenario: por debajo de unos millones de filas un plan bueno y uno malo
cuestan lo mismo y no hay nada que comparar.

| columna | qué es |
|---|---|
| `VentaKey` | 1..2.000.000, única |
| `Importe` | 1..1000, repartido con un paso primo |
| `CategoriaKey` | 20 valores distintos — cardinalidad 1 entre 100.000 |

Las medidas van **en pares, y las dos de cada par devuelven el mismo número**. Sin eso,
comparar tiempos no diría nada sobre rendimiento.

## De dónde salen los datos

Un parquet publicado en
[`CSalcedoDataBI/SampleDataSets`](https://github.com/CSalcedoDataBI/SampleDataSets) (público,
MIT, sintético), leído igual que en los otros tres escenarios:

```
Parquet.Document(Web.Contents(DataBaseUrl, [RelativePath="Ventas.parquet"]))
```

**Pesa 385 KB, no 8,9 MB**, y esa diferencia tiene una causa concreta. `VentaKey` son dos
millones de valores distintos y consecutivos: el diccionario de parquet no le sirve de nada y
con snappy a secas la columna deja el fichero en 8,9 MB — cuatro veces el Contoso entero.
Codificada como **diferencias** (`DELTA_BINARY_PACKED`) baja 23×, porque el salto entre una
fila y la siguiente es siempre 1. Las otras dos columnas conservan su diccionario.

Que Power Query lea esa codificación **está comprobado, no supuesto**: es lo que refresca este
modelo. Las otras dos columnas se dejaron en diccionario porque no ganaban nada con el cambio.

Quitar `VentaKey` habría hecho el fichero aún más pequeño —ninguna medida la usa— y **no se
hizo**: los tiempos publicados abajo se midieron con ella, y un modelo sin ella sería otro
modelo. Los nueve valores de la tabla final se volvieron a medir tras cambiar el origen y
salen idénticos.

Se regenera con [`build_datasets.py`](../build_datasets.py), de forma determinista:
`Importe = (i × 7919) mod 1000 + 1` y `CategoriaKey = i mod 20 + 1`.

## Cómo se midió

- **En frío**: `ClearCache` antes de cada corrida. Sin eso se mide la caché, no el plan.
- **Tres corridas** por medida, se toma la **mediana**.
- Se publican **razones y órdenes de magnitud**, no tiempos absolutos: un número en
  milisegundos envejece con el hardware; que una forma cueste ~290 veces más que otra, no.
- Métricas del propio motor (duración, pico de memoria, consultas al motor de
  almacenamiento), no tiempo de pared del cliente.

## Lo que NO cuesta

Las seis medidas del grupo A, **las seis juntas y en frío**:

| | |
|---|---|
| duración | **5 ms** |
| pico de memoria | 1.027 KB |
| consultas al motor de almacenamiento | 3 |

Y ahí dentro están las tres formas que el consejo habitual da por caras:

| par | las dos formas | resultado |
|---|---|---|
| A1 | `FILTER(ALL(Ventas), Ventas[Importe] > 900)` vs el predicado `Ventas[Importe] > 900` | 190.100.000 |
| A2 | filtrar la **tabla** por categoría vs filtrar la **columna** (20 valores) | 50.900.000 |
| A3 | predicado que compara **dos columnas** entre sí, sobre la tabla vs sobre las columnas | 642.600.000 |

**El motor empuja el predicado al almacenamiento en los tres casos**, incluido el que compara
dos columnas entre sí. Envolver la tabla en un `FILTER` no cuesta nada aquí.

## Lo que SÍ cuesta

La **transición de contexto**: referenciar una *medida* donde hay contexto de fila obliga a
convertir esa fila en filtro, dos millones de veces.

| medida | mediana en frío | pico de memoria | consultas SE |
|---|---|---|---|
| `SUMX(Ventas, [Total])` | **871 ms** | **197.300 KB** | 2 |
| `SUMX(Ventas, Ventas[Importe])` | **3 ms** | 0 KB | 1 |
| `CALCULATE([Total], FILTER(ALL(Ventas), [Total] > 900))` | **873 ms** | **197.342 KB** | 2 |
| `CALCULATE([Total], Ventas[Importe] > 900)` | dentro de los 5 ms del grupo A | — | — |

**≈ 290×**, y de cero a ~193 MB de memoria. Las dos parejas devuelven el mismo número que su
versión barata: 1.001.000.000 y 190.100.000.

> Esta trampa también está **dibujada**: página «2. Lo que cuesta cada forma (medido, no calculado)» del informe. Ábrela con
> el `.pbip` y míralo, que es donde se ve lo que el resultado de la consulta no enseña.

## Lo que esto quiere decir

El bulto no está en `FILTER`, ni en pasarle una tabla en vez de una columna. Está en **qué
hay dentro del predicado**. Un predicado sobre columnas lo resuelve el motor de
almacenamiento de una pasada; una **medida** dentro obliga al motor de fórmulas a materializar
y a transitar el contexto fila a fila.

La regla que se sostiene con estos números no es «no uses FILTER sobre tablas», sino:

> **No metas una medida donde vas a iterar dos millones de filas.**

Ver [`sumx`](../../dax-reference/notes/sumx.md) y [`calculate`](../../dax-reference/notes/calculate.md)
para el mecanismo, que es el mismo que hace que `SUMX` con una medida dé un número distinto
al de `SUMX` con la expresión escrita a mano. Aquí se ve lo que además cuesta.

## Las consultas

```dax
EVALUATE
{
  ("A1 FILTER",             [Alto FILTER]),
  ("A1 predicado",          [Alto predicado]),
  ("A2 por tabla",          [Categoria por tabla]),
  ("A2 por columna",        [Categoria por columna]),
  ("A3 cruce por tabla",    [Cruce por tabla]),
  ("A3 cruce por columnas", [Cruce por columnas]),
  ("B1 con medida",         [Suma con medida]),
  ("B1 con columna",        [Suma con columna]),
  ("B2 con medida",         [Alto con medida])
}
```

| medida | valor |
|---|---|
| A1 (las dos) | 190.100.000 |
| A2 (las dos) | 50.900.000 |
| A3 (las dos) | 642.600.000 |
| B1 (las dos) | 1.001.000.000 |
| B2 | 190.100.000 |

Esos valores sí son estables y los comprueba [`check_lab.py`](../check_lab.py). **Los tiempos
no se comprueban automáticamente**: dependen de la máquina, y un umbral en un test sería una
falsa promesa. Lo que el runner garantiza es que los pares siguen devolviendo lo mismo, que es
la condición sin la cual la comparación de tiempos no significa nada.

> Esta trampa también está **dibujada**: página «1. Los pares devuelven el mismo numero» del informe. Ábrela con
> el `.pbip` y míralo, que es donde se ve lo que el resultado de la consulta no enseña.

## Límites, dichos

- **Un modelo, una máquina, un motor.** Estos números salieron de Power BI Desktop en un
  portátil. La razón ~290× es lo que se publica porque es lo que aguanta un cambio de
  hardware; los milisegundos están para dar contexto, no para citarlos.
- **Que aquí no cueste no quiere decir que nunca cueste.** `FILTER` sobre una tabla puede
  costar mucho con más columnas, con relaciones de por medio o con predicados que el motor no
  sepa empujar. Lo medido es lo que se afirma: en este modelo, con estos predicados, no cuesta.
- **El refresco necesita internet**, como los otros tres escenarios. Dos millones de filas
  entran en 385 KB de parquet, así que la descarga no es el cuello de botella; cargarlas en el
  motor sí tarda unos segundos.
