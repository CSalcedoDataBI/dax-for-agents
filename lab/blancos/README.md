# Blancos en una columna numérica

## Qué demuestra

Las funciones de promedio **saltan los blancos**: dividen entre las filas que tienen valor, no
entre todas. Eso está documentado. Lo que no está es lo fácil que es romperlo sin darse
cuenta: basta con que la expresión convierta el blanco en cero — un `COALESCE` puesto "por
seguridad", o incluso un `+ 0` — para que el denominador cambie y la media baje.

Contoso no sirve para enseñarlo porque ninguna columna numérica tiene blancos. Por eso esta
nota no se escribió al principio.

## El modelo

Una tabla, cinco filas, dos con los metros en blanco:

| TiendaKey | Nombre | Metros |
|---|---|---|
| 1 | Centro | 100 |
| 2 | Norte | 200 |
| 3 | Sur | 300 |
| 4 | Este | *(en blanco)* |
| 5 | Oeste | *(en blanco)* |

100 + 200 + 300 = 600. Entre **3** son 200; entre **5** son 120. Los números están elegidos
para que se distinga de un vistazo cuál de los dos denominadores se usó.

## 1. Quién cuenta y quién no

```dax
EVALUATE
ROW(
  "filas",               COUNTROWS(Tiendas),
  "con_metros",          COUNT(Tiendas[Metros]),
  "en_blanco",           COUNTBLANK(Tiendas[Metros]),
  "SUM",                 SUM(Tiendas[Metros]),
  "AVERAGE",             AVERAGE(Tiendas[Metros]),
  "AVERAGEX",            AVERAGEX(Tiendas, Tiendas[Metros]),
  "SUM_entre_COUNTROWS", DIVIDE(SUM(Tiendas[Metros]), COUNTROWS(Tiendas))
)
```

| expresión | resultado | denominador |
|---|---|---|
| `COUNTROWS(Tiendas)` | **5** | |
| `COUNT(Tiendas[Metros])` | **3** | |
| `COUNTBLANK(Tiendas[Metros])` | **2** | |
| `SUM(Tiendas[Metros])` | **600** | |
| `AVERAGE(Tiendas[Metros])` | **200** | 3 |
| `AVERAGEX(Tiendas, Tiendas[Metros])` | **200** | 3 |
| `DIVIDE(SUM(...), COUNTROWS(...))` | **120** | 5 |

**`AVERAGE` y `AVERAGEX` dan lo mismo.** Eso contradice la intuición de que el iterador
"recorre todas las filas y por tanto cuenta las vacías": no lo hace, salta el blanco igual
que `AVERAGE`. Lo que se aparta es `SUM / COUNTROWS`, que divide entre 5.

> Esta trampa también está **dibujada**: página «1. Quien cuenta y quien no» del informe. Ábrela con
> el `.pbip` y míralo, que es donde se ve lo que el resultado de la consulta no enseña.

## 2. Cómo se rompe sin querer

```dax
EVALUATE
ROW(
  "AVERAGE",               AVERAGE(Tiendas[Metros]),
  "AVERAGEX_columna",      AVERAGEX(Tiendas, Tiendas[Metros]),
  "AVERAGEX_con_COALESCE", AVERAGEX(Tiendas, COALESCE(Tiendas[Metros], 0)),
  "AVERAGEX_con_mas_cero", AVERAGEX(Tiendas, Tiendas[Metros] + 0)
)
```

| expresión | resultado |
|---|---|
| `AVERAGE(Tiendas[Metros])` | **200** |
| `AVERAGEX(Tiendas, Tiendas[Metros])` | **200** |
| `AVERAGEX(Tiendas, COALESCE(Tiendas[Metros], 0))` | **120** |
| `AVERAGEX(Tiendas, Tiendas[Metros] + 0)` | **120** |

Ahí está la trampa. **`Tiendas[Metros] + 0` cambia la media de 200 a 120.** El `+ 0` no
altera ningún valor existente: lo único que hace es convertir el blanco en cero, y con eso el
blanco pasa a contar en el denominador.

El `COALESCE` es peor porque parece deliberado y defensivo. Quien lo escribe cree estar
evitando un error; lo que hace es cambiar la definición de la métrica.

Ninguno de los dos resultados está mal — dependen de si "sin dato" significa "no aplica" o
"cero". Lo que está mal es que la diferencia esté escondida en un `+ 0`.

> Esta trampa también está **dibujada**: página «2. El + 0 que mueve el denominador» del informe. Ábrela con
> el `.pbip` y míralo, que es donde se ve lo que el resultado de la consulta no enseña.

## De dónde salen los datos

Esas cinco filas son un parquet de **1 KB** publicado en
[`CSalcedoDataBI/SampleDataSets`](https://github.com/CSalcedoDataBI/SampleDataSets) (público,
MIT, sintético), que el modelo lee igual que los otros tres escenarios:

```
Parquet.Document(Web.Contents(DataBaseUrl, [RelativePath="Tiendas.parquet"]))
```

Hay un detalle que el origen **tiene que** preservar y por eso no vale cualquiera: el blanco
viaja como `null` dentro del parquet y Power Query lo entrega como `null`, así que la columna
llega a DAX en blanco y no como cero. Si el origen convirtiera el hueco en cero, el escenario
dejaría de demostrar nada — `AVERAGE` daría 120 y no habría diferencia que enseñar.

Se regeneran con [`build_datasets.py`](../build_datasets.py), que las escribe a mano una a una.

## Cómo reproducirlo

1. Abre `Blancos.pbip` en Power BI Desktop.
2. **Refresca** — al abrir un PBIP el modelo carga sin datos, hay que pedirlo. Necesita
   internet; no hay credenciales que dar.
3. Pega las consultas en la vista de consulta DAX, o deja que el runner las ejecute:

```bash
python lab/check_lab.py blancos localhost:<puerto>
```

Medido el 2026-08-12 con las dos consultas de arriba, tal cual están escritas.
