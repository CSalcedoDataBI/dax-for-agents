# Claves huérfanas y la fila en blanco

## Qué demuestra

Cuando la tabla de hechos referencia una clave que **no existe** en la dimensión, el motor no
descarta esas filas ni da error: añade una **fila en blanco** a la dimensión y cuelga de ella
todo lo huérfano. Esa fila no está en los datos, aparece sola.

Contoso no sirve para enseñarlo porque tiene la integridad referencial intacta. Por eso la
nota de [`countrows`](../../skills/dax-reference/notes/countrows.md) tuvo que **retirar** esa
afirmación tras una review: no se podía demostrar, y una nota sin demostrar no se escribe.
Este modelo existe para poder escribirla.

## El modelo

Tres tablas, siete filas de datos, y el problema en una sola línea:

| `DimProducto` | | | `Ventas` | |
|---|---|---|---|---|
| **ProductoKey** | **Nombre** | | **ProductoKey** | **Unidades** |
| 1 | Alfa | | 1 | 10 |
| 2 | Beta | | 2 | 20 |
| 3 | Gamma | | 3 | 30 |
| | | | **99** | **50** |

`Ventas[ProductoKey] = 99` no existe en `DimProducto`. Esas siete filas son la tabla de
arriba, entera: no hay nada más en el modelo.

## 1. De qué lado se ve la fila en blanco

```dax
EVALUATE
ROW(
  "filas_en_DimProducto",        COUNTROWS(DimProducto),
  "VALUES_del_lado_UNO",         COUNTROWS(VALUES(DimProducto[ProductoKey])),
  "VALUES_del_lado_MUCHOS",      COUNTROWS(VALUES(Ventas[ProductoKey])),
  "ALLNOBLANKROW_del_lado_UNO",  COUNTROWS(ALLNOBLANKROW(DimProducto[ProductoKey]))
)
```

| expresión | resultado | |
|---|---|---|
| `COUNTROWS(DimProducto)` | **3** | la tabla base no tiene la fila en blanco |
| `COUNTROWS(VALUES(DimProducto[ProductoKey]))` | **4** | ← aquí sí aparece |
| `COUNTROWS(VALUES(Ventas[ProductoKey]))` | **4** | pero por otro motivo: son 1, 2, 3 y **99** |
| `COUNTROWS(ALLNOBLANKROW(DimProducto[ProductoKey]))` | **3** | la excluye a propósito |

Los dos `VALUES` dan 4 y **no significan lo mismo**. Del lado *uno* el cuarto elemento es la
fila en blanco que el motor inventó; del lado *muchos* es la clave 99 de verdad, que sigue
ahí. Confundir las dos cosas fue exactamente el error que la review de la nota detectó.

> Esta trampa también está **dibujada**: página «1. De que lado se ve la fila en blanco» del informe. Ábrela con
> el `.pbip` y míralo, que es donde se ve lo que el resultado de la consulta no enseña.

## 2. Dónde van a parar las unidades huérfanas

```dax
EVALUATE
ADDCOLUMNS(
  VALUES(DimProducto[Nombre]),
  "unidades", CALCULATE(SUM(Ventas[Unidades]))
)
ORDER BY DimProducto[Nombre]
```

| Nombre | unidades |
|---|---|
| *(en blanco)* | **50** |
| Alfa | 10 |
| Beta | 20 |
| Gamma | 30 |

Una fila sin nombre con 50 unidades. En un informe real esto es la categoría vacía que sale
en el gráfico y que nadie sabe de dónde viene: son las ventas cuyo producto no está en la
dimensión.

> Esta trampa también está **dibujada**: página «2. Donde caen las unidades huerfanas» del informe. Ábrela con
> el `.pbip` y míralo, que es donde se ve lo que el resultado de la consulta no enseña.

## 3. El total sí las cuenta, y "limpiar" la fila en blanco las pierde

```dax
EVALUATE
ROW(
  "total_Ventas",              SUM(Ventas[Unidades]),
  "suma_por_producto_visible", SUMX(VALUES(DimProducto[Nombre]), CALCULATE(SUM(Ventas[Unidades]))),
  "suma_sin_fila_en_blanco",   SUMX(ALLNOBLANKROW(DimProducto[Nombre]), CALCULATE(SUM(Ventas[Unidades])))
)
```

| expresión | resultado |
|---|---|
| `SUM(Ventas[Unidades])` | **110** |
| Suma por producto, con `VALUES` | **110** ✅ cuadra |
| Suma por producto, con `ALLNOBLANKROW` | **60** ❌ faltan 50 |

Esta es la parte que hace daño. `ALLNOBLANKROW` suena a "quitar el ruido", y lo que hace es
**perder 50 unidades sin avisar**: el detalle deja de sumar el total y la diferencia son
justo las huérfanas.

> Esta trampa también está **dibujada**: página «3. Limpiar la fila en blanco pierde 50» del informe. Ábrela con
> el `.pbip` y míralo, que es donde se ve lo que el resultado de la consulta no enseña.

## De dónde salen los datos

Dos parquet de **2 KB entre los dos**, publicados en
[`CSalcedoDataBI/SampleDataSets`](https://github.com/CSalcedoDataBI/SampleDataSets) (público,
MIT, sintético), que el modelo lee igual que los otros tres escenarios:

```
Parquet.Document(Web.Contents(DataBaseUrl, [RelativePath="Ventas.parquet"]))
```

La huérfana está **escrita a mano**, no inyectada por un porcentaje de calidad de datos. La
diferencia importa: el escenario necesita *una* huérfana concreta con *un* número de unidades
concreto, porque las tres tablas de resultados de arriba cuadran fila a fila con ella. Un
`orphan_fk_pct = 0.25` daría una huérfana distinta en cada regeneración y los 110, 60 y 50 de
este README dejarían de ser comprobables.

Se regeneran con [`build_datasets.py`](../build_datasets.py).

## Cómo reproducirlo

1. Abre `ClavesHuerfanas.pbip` en Power BI Desktop.
2. **Refresca** — al abrir un PBIP el modelo carga sin datos, hay que pedirlo. Necesita
   internet; no hay credenciales que dar.
3. Pega las consultas en la vista de consulta DAX, o deja que el runner las ejecute:

```bash
python lab/check_lab.py claves-huerfanas localhost:<puerto>
```

Medido el 2026-08-12 con las tres consultas de arriba, tal cual están escritas.
