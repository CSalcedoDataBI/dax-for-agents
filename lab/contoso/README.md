# contoso — el modelo contra el que se midieron 30 de las 31 notas

Los otros tres escenarios existen para demostrar una trampa que Contoso **no puede**
demostrar. Este es el contrario: es el modelo donde se midió casi todo lo demás.

Hasta ahora vivía en una máquina. Veintinueve notas de campo llevaban al pie *«Medido sobre
Contoso Retail (FactSales 126.524 filas, 137 productos…)»* y el lector tenía la consulta, el
número, y **ninguna forma de ejecutarlos**. Eso era la mayor parte del contenido escrito a
mano del repo apoyándose en algo que nadie más podía abrir.

## El modelo

Star schema de siete tablas más `_Measures`:

| tabla | filas | qué es |
|---|---|---|
| `FactSales` | **126.524** | una línea de pedido (`OrderKey` + `LineNumber`) |
| `DimProduct` | **137** | producto, con `Brand`, `CategoryName`, `Color`, `Price` |
| `DimCustomer` | 12.000 | cliente |
| `DimStore` | 25 | tienda — `CloseDate` en blanco salvo las cerradas |
| `DimDate` | — | **2023-01-01 a 2024-12-31**, una fila por día |
| `DimCurrency` · `DimCurrencyExchange` | — | divisa y tipo de cambio |

Las cifras en negrita son las que citan los pies de las notas, y las comprueba
[`check_lab.py`](../check_lab.py) antes de ejecutar ninguna consulta: si el modelo deja de
ser el que dicen, no tiene sentido seguir.

## Las diez páginas del informe

Seis existen porque una trampa de las notas de campo **no se puede enseñar en texto** —
solo vive dentro de un visual. Las otras cuatro, añadidas después, muestran en vivo lo que
aportó, una por una, cada skill de las que existían al construirlas, a un escenario real (la media móvil de
3 meses medida en [`dax-reference/notes/window.md`](../../dax-reference/notes/window.md)).
Los dos grupos comparten el mismo lenguaje visual: un textbox de nota arriba, un visual de
datos real debajo, contra medidas persistidas en `_Measures.tmdl` — nunca contra una consulta
suelta.

### Las seis primeras: trampas que solo viven en un visual

| página | qué se ve, y no se puede contar |
|---|---|
| ALLSELECTED — respeta el slicer, ignora el interno | Selecciona 2-3 marcas: una columna cambia y la otra no se mueve. En una consulta DAX no hay slicer |
| SELECTEDVALUE — la tarjeta que no distingue dos casos | Sin selección y con dos marcas la tarjeta dice lo mismo. No distingue «no eligió» de «eligió varias» |
| RANKX — 1 en todas las filas de la matriz | La columna del medio vale 1 en las 58 filas, porque la matriz ya trajo una sola marca al contexto |
| SUMX — el Total que no cuadra con sus filas | El Total de la primera columna no es la suma de la columna. Se evalúa otra vez, sin los filtros de fila |
| El blanco borra la categoría; el cero la dibuja | Dos gráficos con la misma división: al de la izquierda le faltan catorce barras |
| FORMAT — el 9 va después del 10 | La misma cifra como número y como cadena. Ordena la segunda por ventas |

Ábrelas con el `.pbip`. **El dibujo no lo comprueba ningún test**, y las dos primeras necesitan
además que muevas el slicer con el ratón.

### Las otras cuatro: lo que aportó cada skill

| página | qué muestra |
|---|---|
| dax-lib — ya existe, pero solo el índice | `TimeSeries.MovingAverage` ya está publicado en daxlib.org; el índice dice qué existe, no trae el código |
| dax-reference — MOVINGAVERAGE no aplica aquí | `MOVINGAVERAGE` nativo es `appliesTo: [visual-calculation]` únicamente; una matriz sin filtro prueba que la alternativa con `WINDOW` sí funciona como medida |
| dax-window-functions — la trampa medida, en vivo | Fija el slicer de `Year` en 2024: `Media 3M (rota)` se separa de `Media 3M (corregida)` cerca de enero-febrero, sin ningún error visible. La demostración interactiva del hallazgo de `window.md` |
| dax-udf-authoring — reutilizable, no un one-off | Las dos medidas de la página anterior son envoltorios de una sola función persistida (`Contoso.Lab.MediaMovil3M_Corregida`); esta matriz la llama dos veces con distinto parámetro `months` |

`Contoso.Lab.MediaMovil3M` y `Contoso.Lab.MediaMovil3M_Corregida` viven en
[`functions.tmdl`](./Contoso.SemanticModel/definition/functions.tmdl) — nuevas desde estas
cuatro páginas, y requieren `compatibilityLevel: 1702` (antes 1606), también nuevo aquí.


## De dónde salen los datos

Igual que los otros tres escenarios, y este fue el primero en hacerlo:

```
Parquet.Document(Web.Contents(DataBaseUrl, [RelativePath="FactSales.parquet"]))
```

`DataBaseUrl` es un parámetro M de verdad que apunta a
[`CSalcedoDataBI/SampleDataSets`](https://github.com/CSalcedoDataBI/SampleDataSets) —
repositorio **público**, licencia **MIT**, datos **100% sintéticos** (ni una persona ni una
empresa real). Sin autenticación, sin SQL Server, sin rutas locales: refresca en la máquina
de cualquiera. Para usar un fork, una rama o un espejo local, se cambia ese único valor.

Los parquet **no se copian al repo**: son ~2 MB y ya viven en un sitio público. Lo que se
versiona son los ~20 KB de TMDL.

## Cómo se usa

1. Abre `Contoso.pbip` en Power BI Desktop y **refresca** — al abrir un PBIP el modelo carga
   sin datos, hay que pedirlo.
2. Ejecuta la consulta de cualquier nota en la vista de consulta DAX, o deja que el runner
   las ejecute todas:

```bash
python lab/check_lab.py contoso localhost:<puerto>
```

Eso comprueba primero que el modelo es el que declaran las notas, y después ejecuta **las 39
consultas** publicadas en las notas de campo comparándolas con
[`notes_expected.py`](../notes_expected.py).

Las consultas **no están copiadas** en el runner: las lee del propio `.md` de cada nota. Si
alguien edita la consulta de una nota y el resultado cambia, sale rojo. Ese es el punto —
una nota cuyo número dejó de salir del motor está mintiendo.

Para regenerar los esperados tras tocar una nota:

```bash
python lab/dump_notes.py localhost:<puerto> > lab/notes_expected.py
```

Lo que imprima hay que **mirarlo** contra la tabla que publica la nota antes de aceptarlo:
ese script traslada resultados a código, no decide si son los correctos.

## Dos consultas que fallan a propósito

`removefilters` y `values` publican un **error del motor** como resultado, no un número:

| nota | lo que el motor rechaza |
|---|---|
| `removefilters` | `REMOVEFILTERS function cannot be used as a table expression` |
| `values` | `A table of multiple values was supplied where a single value was expected` |

El runner los espera. Si algún día el motor dejara de rechazarlas, ambas estarían mintiendo y
el escenario se pone rojo — que es exactamente lo que debe pasar.

## Qué se dejó fuera al traerlo

El modelo semántico es **idéntico byte a byte** al maestro del que salió, con dos ausencias
deliberadas:

- **`cultures/es-ES.tmdl`** — 400 KB de traducciones de nombres para mostrar. Era el fichero
  más grande del modelo con diferencia y no cambia ni un resultado de DAX.
- **El informe del maestro.** Trae imágenes de marca personal y de empresa en
  `StaticResources`, y este repo está a un paso de una decisión de publicación cuya única
  parte sin vuelta atrás es la historia de git. Aquí el informe está vacío, igual que en los
  otros tres escenarios: las consultas se ejecutan contra el modelo, no contra el informe.

## Límites, dichos

- **La tabla de fechas no está marcada** como tabla de fechas. Las notas de inteligencia de
  tiempo (`DATESYTD`, `SAMEPERIODLASTYEAR`, `PREVIOUSMONTH`, `DATEADD`) se midieron así y
  reproducen así. Marcarla cambiaría el modelo respecto al que produjo los números.
- **El refresco necesita internet.** Si `raw.githubusercontent.com` no es alcanzable, este
  escenario no se puede ejecutar — ni ningún otro del laboratorio. Es el precio de no meter
  los datos en el repo, y lo pagan los cuatro por igual.
- **Ninguna cifra de rendimiento sale de aquí.** A 126.524 filas todo se resuelve en
  milisegundos y cualquier comparación caería dentro del ruido; para eso está
  [`rendimiento`](../rendimiento/).
