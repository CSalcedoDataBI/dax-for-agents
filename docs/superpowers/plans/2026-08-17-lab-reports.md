# Informes del laboratorio — plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dar a los cuatro escenarios de `lab/` trece páginas de informe, una por trampa, para las trampas que solo existen dentro de un visual.

**Architecture:** PBIR escrito a mano sobre la plantilla confirmada de un `visual.json` que produjo Power BI Desktop. Cada página consume **medidas** del modelo (una tarjeta no acepta DAX suelto), y cada medida nueva entra en `lab/check_lab.py` con su valor esperado, así que el informe hereda la misma disciplina que el resto del repositorio: si un número cambia, algo se pone rojo.

**Tech Stack:** PBIR 2.0.0 (`visualContainer` 2.11.0, `page` 2.0.0) · TMDL · Python 3 + pyadomd · Power BI Desktop para verificar el renderizado.

## Global Constraints

- **El repositorio es privado y está PROHIBIDO publicarlo.** Nada de lo que aquí se escriba cambia eso.
- **Solo visuales nativos.** Ningún Deneb, ningún visual del marketplace: obligaría a instalarlo antes de ver nada.
- **Se conserva el tema `CY25SU11`** que ya declara cada `report.json`. No se define tema propio.
- **Lienzo 1280×720**, el que ya tienen las cuatro páginas vacías.
- **Ninguna cifra sin medir.** Un número que aparece en una página sale de una medida que `check_lab.py` comprueba, o de la tabla `Tiempos`, que lleva escrito en el TMDL cuándo y cómo se midió.
- **Prosa en español, código y commits en inglés**, como el resto del repositorio.
- **Sin nombres de cliente ni marca personal** en ningún fichero, y sin nombrarlos aquí
  tampoco: escribir un término para prohibirlo lo mete en el repositorio, que es justo
  lo que se quiere evitar.
- Cada tarea termina con **commit**.

## Plantilla PBIR confirmada

Esto **no es una suposición**: sale de `ranking-bump-chart/pbip/ContosoRetail.Report`, un informe que escribió Power BI Desktop contra un Contoso con el mismo `_Measures` y el mismo `DimProduct` que el nuestro.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.11.0/schema.json",
  "name": "<id, igual que el nombre de la carpeta>",
  "position": { "x": 24, "y": 496, "z": 1000, "height": 184, "width": 1216, "tabOrder": 1000 },
  "visual": {
    "visualType": "clusteredBarChart",
    "query": {
      "queryState": {
        "Category": { "projections": [ {
          "field": { "Column": {
            "Expression": { "SourceRef": { "Entity": "DimProduct" } },
            "Property": "SubCategoryName" } },
          "queryRef": "DimProduct.SubCategoryName",
          "nativeQueryRef": "SubCategoryName",
          "active": true } ] },
        "Y": { "projections": [ {
          "field": { "Measure": {
            "Expression": { "SourceRef": { "Entity": "_Measures" } },
            "Property": "Total Sales" } },
          "queryRef": "_Measures.Total Sales",
          "nativeQueryRef": "Total Sales" } ] }
      }
    },
    "visualContainerObjects": {
      "title": [ { "properties": {
        "show": { "expr": { "Literal": { "Value": "true" } } },
        "text": { "expr": { "Literal": { "Value": "'El titulo, entre comillas simples DENTRO de la cadena'" } } } } } ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

Cinco cosas que se rompen si se olvidan:

1. **`name` tiene que coincidir con el nombre de la carpeta** que contiene el `visual.json`.
2. **Un literal de texto va con comillas simples dentro de la cadena JSON**: `"'Mi titulo'"`. Sin ellas, Power BI lo lee como una referencia y la propiedad se ignora en silencio.
3. Una **columna** usa `"Column"` y una **medida** usa `"Measure"`. Confundirlas hace que el visual cargue vacío sin dar error.
4. **Una columna en un pozo de VALORES necesita envoltorio `Aggregation`.** Esto lo encontró el gate de la Task 1, dibujado: con un `"Column"` pelado en el rol `Y`, Power BI Desktop abre el informe sin una sola queja, pinta el título, pinta el eje de categorías **y no dibuja ninguna barra**. No hay error, no hay aviso, no hay hueco: el gráfico sale en blanco. Un `Measure` sí vale pelado — el pozo de valores acepta algo ya agregado, y una columna no lo está.

   ```json
   "field": {
     "Aggregation": {
       "Expression": { "Column": {
         "Expression": { "SourceRef": { "Entity": "Tiendas" } },
         "Property": "Metros" } },
       "Function": 0
     }
   },
   "queryRef": "Sum(Tiendas.Metros)",
   "nativeQueryRef": "Suma de Metros"
   ```

   `Function`: `0` suma, `1` media, `2` recuento distinto, `3` mínimo, `4` máximo, `5` recuento. El `queryRef` tiene que declarar la misma agregación (`Sum(Tabla.Columna)`), no el nombre pelado de la columna.

5. **`"active": true` mata un `tableEx`.** Dentro del rol `Values` de una tabla, esa bandera deja el visual con la cabecera de la columna y **nada más** — ni filas ni la columna de la medida, otra vez sin un solo error. En un `pivotTable` (rol `Rows`) y en un gráfico de barras (rol `Category`) la misma bandera es inofensiva y es lo que escribe Desktop. Quítala solo en `tableEx`.

Y un hecho medido sobre el dibujo, no sobre el formato, que cambia lo que puede prometer una página: **una categoría cuyo valor es blanco no deja hueco en el eje — desaparece.** En `blancos` el gráfico sale con tres barras (Centro 100, Norte 200, Sur 300) y Este y Oeste no están. El diseño daba por hecho que se verían dos huecos vacíos. No es así, y la lección resultante es más fuerte: el blanco no adelgaza la barra, borra la fila entera del gráfico. Cualquier página que quiera enseñar el hueco necesita «mostrar elementos sin datos», que es otra cosa.

Roles por tipo de visual, que es lo único que cambia entre uno y otro:

| visualType | roles de `queryState` |
|---|---|
| `clusteredColumnChart` · `clusteredBarChart` | `Category`, `Y` |
| `card` | `Values` |
| `tableEx` | `Values` |
| `pivotTable` (matriz) | `Rows`, `Columns`, `Values` |
| `slicer` | `Values` |
| `textbox` | ninguno — no lleva bloque `query` |

## Estructura de ficheros

```
lab/<escenario>/<Nombre>.Report/definition/
  pages/
    pages.json                       ← MODIFICAR: pageOrder + activePageName
    <slug-de-pagina>/
      page.json                      ← CREAR: una por trampa
      visuals/
        <id-legible>/visual.json     ← CREAR: uno por visual
lab/<escenario>/<Nombre>.SemanticModel/definition/tables/
  _Medidas.tmdl | _Measures.tmdl     ← MODIFICAR: las medidas nuevas
  Tiempos.tmdl                       ← CREAR (solo rendimiento)
lab/build_datasets.py                ← MODIFICAR: la tabla Tiempos
lab/check_lab.py                     ← MODIFICAR: un CHECK por grupo de medidas
lab/<escenario>/README.md            ← MODIFICAR: enlazar la página
lab/README.md                        ← MODIFICAR: qué verifica el runner y qué no
```

Las páginas vacías `page1` («Lienzo vacío») **se borran** en la tarea que da su primera página real a cada escenario. Un lienzo vacío que sobrevive al lado de páginas con contenido no informa de nada.

---

### Task 1: La página piloto — `blancos/denominador`

Esta tarea existe para **retirar el riesgo**, no para entregar una página. Si el PBIR escrito a mano no renderiza, se sabe aquí y no en la página trece.

**Files:**
- Modify: `lab/blancos/Blancos.SemanticModel/definition/tables/_Medidas.tmdl`
- Create: `lab/blancos/Blancos.Report/definition/pages/denominador/page.json`
- Create: `lab/blancos/Blancos.Report/definition/pages/denominador/visuals/barras-metros/visual.json`
- Create: `lab/blancos/Blancos.Report/definition/pages/denominador/visuals/card-media/visual.json`
- Create: `lab/blancos/Blancos.Report/definition/pages/denominador/visuals/card-media-todas/visual.json`
- Create: `lab/blancos/Blancos.Report/definition/pages/denominador/visuals/card-filas/visual.json`
- Create: `lab/blancos/Blancos.Report/definition/pages/denominador/visuals/card-filas-metros/visual.json`
- Modify: `lab/blancos/Blancos.Report/definition/pages/pages.json`
- Delete: `lab/blancos/Blancos.Report/definition/pages/page1/`
- Modify: `lab/check_lab.py`

**Interfaces:**
- Produces: las medidas `Media`, `Media por todas las filas`, `Filas`, `Filas con metros` en la entidad `_Medidas` del modelo `Blancos`. La Task 2 las reutiliza.
- Produces: el patrón de `visual.json` que usan las tareas 2–9.

- [ ] **Step 1: Añadir las medidas al modelo**

En `lab/blancos/Blancos.SemanticModel/definition/tables/_Medidas.tmdl`, insertar **antes** de `column Marcador`:

```
	/// El denominador son las TRES filas con valor, no las cinco de la tabla. Hay que leerla
	/// al lado de [Media por todas las filas], que da 120 sobre exactamente los mismos datos.
	measure Media = AVERAGE(Tiendas[Metros])
		formatString: #,0
		lineageTag: b1a70000-0000-4000-8000-000000000511

	/// Divide entre las CINCO filas. 120. Ni esta ni [Media] estan mal: dependen de si "sin
	/// dato" significa "no aplica" o "cero". Lo que esta mal es que la diferencia se esconda.
	measure 'Media por todas las filas' = DIVIDE(SUM(Tiendas[Metros]), COUNTROWS(Tiendas))
		formatString: #,0
		lineageTag: b1a70000-0000-4000-8000-000000000512

	/// Cinco. Cuenta filas sin mirar el contenido.
	measure Filas = COUNTROWS(Tiendas)
		formatString: #,0
		lineageTag: b1a70000-0000-4000-8000-000000000513

	/// Tres. COUNT cuenta VALORES, y el blanco no es un valor.
	measure 'Filas con metros' = COUNT(Tiendas[Metros])
		formatString: #,0
		lineageTag: b1a70000-0000-4000-8000-000000000514

```

El nombre `Filas` y no `Tiendas`: una medida no puede llamarse igual que una tabla del modelo.

- [ ] **Step 2: Escribir la página**

`lab/blancos/Blancos.Report/definition/pages/denominador/page.json`:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
  "name": "denominador",
  "displayName": "1. Quien cuenta y quien no",
  "displayOption": "FitToPage",
  "height": 720,
  "width": 1280
}
```

- [ ] **Step 3: Escribir el gráfico de barras**

`.../visuals/barras-metros/visual.json`. **Este es el visual que carga la lección**: Este y Oeste no dibujan barra, y esa ausencia *es* el blanco.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.11.0/schema.json",
  "name": "barras-metros",
  "position": { "x": 40, "y": 140, "z": 0, "height": 420, "width": 700, "tabOrder": 0 },
  "visual": {
    "visualType": "clusteredColumnChart",
    "query": {
      "queryState": {
        "Category": { "projections": [ {
          "field": { "Column": {
            "Expression": { "SourceRef": { "Entity": "Tiendas" } },
            "Property": "Nombre" } },
          "queryRef": "Tiendas.Nombre",
          "nativeQueryRef": "Nombre",
          "active": true } ] },
        "Y": { "projections": [ {
          "field": { "Column": {
            "Expression": { "SourceRef": { "Entity": "Tiendas" } },
            "Property": "Metros" } },
          "queryRef": "Sum(Tiendas.Metros)",
          "nativeQueryRef": "Metros" } ] }
      }
    },
    "visualContainerObjects": {
      "title": [ { "properties": {
        "show": { "expr": { "Literal": { "Value": "true" } } },
        "text": { "expr": { "Literal": { "Value": "'Metros por tienda — Este y Oeste no dibujan barra'" } } } } } ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

- [ ] **Step 4: Escribir las cuatro tarjetas**

Las cuatro son el mismo fichero cambiando cuatro cosas: el nombre de la carpeta, `name`, la `x` de `position`, y la medida en `Property` / `queryRef` / `nativeQueryRef`.

`.../visuals/card-media/visual.json`:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.11.0/schema.json",
  "name": "card-media",
  "position": { "x": 780, "y": 140, "z": 1, "height": 120, "width": 220, "tabOrder": 1 },
  "visual": {
    "visualType": "card",
    "query": {
      "queryState": {
        "Values": { "projections": [ {
          "field": { "Measure": {
            "Expression": { "SourceRef": { "Entity": "_Medidas" } },
            "Property": "Media" } },
          "queryRef": "_Medidas.Media",
          "nativeQueryRef": "Media" } ] }
      }
    },
    "visualContainerObjects": {
      "title": [ { "properties": {
        "show": { "expr": { "Literal": { "Value": "true" } } },
        "text": { "expr": { "Literal": { "Value": "'AVERAGE — entre 3'" } } } } } ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

Las otras tres, con los mismos campos y estos valores:

| carpeta y `name` | `position.x` / `y` | `Property` | título |
|---|---|---|---|
| `card-media-todas` | 1020 / 140 | `Media por todas las filas` | `'SUM ÷ COUNTROWS — entre 5'` |
| `card-filas` | 780 / 290 | `Filas` | `'Filas de la tabla'` |
| `card-filas-metros` | 1020 / 290 | `Filas con metros` | `'Filas CON metros'` |

En cada una, `queryRef` es `_Medidas.<Property>` y `nativeQueryRef` es `<Property>`.

- [ ] **Step 5: Registrar la página y borrar el lienzo vacío**

`lab/blancos/Blancos.Report/definition/pages/pages.json`:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
  "pageOrder": [
    "denominador"
  ],
  "activePageName": "denominador"
}
```

```bash
rm -rf lab/blancos/Blancos.Report/definition/pages/page1
```

- [ ] **Step 6: LA VERIFICACIÓN QUE JUSTIFICA ESTA TAREA**

Abrir `lab/blancos/Blancos.pbip` en Power BI Desktop y **refrescar**.

Esperado: la página «1. Quien cuenta y quien no» abre con cinco visuales. El gráfico enseña tres barras (Centro 100, Norte 200, Sur 300) y **dos huecos**. Las tarjetas leen **200**, **120**, **5**, **3**.

**Si Power BI Desktop no abre el fichero o un visual sale vacío, PARAR y arreglar el PBIR antes de seguir.** Ese es el propósito entero de la tarea. Las pistas más probables, por orden:
- `name` distinto del nombre de la carpeta
- un literal de texto sin comillas simples internas
- `"Column"` donde tenía que ir `"Measure"`
- el tipo de tarjeta: si `card` sale vacío, probar `cardVisual` con el mismo bloque `Values`

- [ ] **Step 7: El runner comprueba las medidas nuevas**

En `lab/check_lab.py`, añadir a `CHECKS["blancos"]`:

```python
        (
            "las medidas de la pagina denominador",
            """
            EVALUATE
            ROW(
              "Media",                     [Media],
              "Media_por_todas_las_filas",  [Media por todas las filas],
              "Filas",                      [Filas],
              "Filas_con_metros",           [Filas con metros]
            )
            """,
            {
                "Media": 200,
                "Media_por_todas_las_filas": 120,
                "Filas": 5,
                "Filas_con_metros": 3,
            },
        ),
```

- [ ] **Step 8: Ejecutar el runner**

Con el modelo abierto y refrescado, y `<puerto>` el de esa instancia:

```bash
python lab/check_lab.py blancos localhost:<puerto>
```

Esperado: tres líneas `ok`, ninguna `FALLA`.

- [ ] **Step 9: Commit**

```bash
git add lab/blancos lab/check_lab.py
git commit -m "feat(lab): blancos estrena pagina — el blanco que no dibuja barra"
```

---

### Task 2: `blancos/mas-cero`

**Files:**
- Modify: `lab/blancos/Blancos.SemanticModel/definition/tables/_Medidas.tmdl`
- Create: `lab/blancos/Blancos.Report/definition/pages/mas-cero/page.json`
- Create: `lab/blancos/Blancos.Report/definition/pages/mas-cero/visuals/card-{average,averagex,coalesce,mas-cero}/visual.json`
- Modify: `lab/blancos/Blancos.Report/definition/pages/pages.json`
- Modify: `lab/check_lab.py`

**Interfaces:**
- Consumes: la medida `Media` y el patrón de `visual.json` de la Task 1.
- Produces: `Media con AVERAGEX`, `Media con COALESCE`, `Media con mas cero` en `_Medidas`.

- [ ] **Step 1: Las tres medidas que faltan**

En `_Medidas.tmdl`, después de `Media por todas las filas`:

```
	/// AVERAGEX salta el blanco IGUAL que AVERAGE: 200, no 120. La intuicion de que el
	/// iterador "recorre todas las filas y por tanto cuenta las vacias" es falsa.
	measure 'Media con AVERAGEX' = AVERAGEX(Tiendas, Tiendas[Metros])
		formatString: #,0
		lineageTag: b1a70000-0000-4000-8000-000000000515

	/// El COALESCE parece deliberado y defensivo. Lo que hace es cambiar la definicion de la
	/// metrica: convierte el blanco en cero y el denominador pasa de 3 a 5. Da 120.
	measure 'Media con COALESCE' = AVERAGEX(Tiendas, COALESCE(Tiendas[Metros], 0))
		formatString: #,0
		lineageTag: b1a70000-0000-4000-8000-000000000516

	/// Un + 0 que no altera NINGUN valor existente y aun asi mueve la media de 200 a 120.
	/// Es la version de la trampa que nadie ve en una revision de codigo.
	measure 'Media con mas cero' = AVERAGEX(Tiendas, Tiendas[Metros] + 0)
		formatString: #,0
		lineageTag: b1a70000-0000-4000-8000-000000000517

```

- [ ] **Step 2: La página**

`.../pages/mas-cero/page.json`, idéntico al de la Task 1 cambiando:

```json
  "name": "mas-cero",
  "displayName": "2. El + 0 que mueve el denominador",
```

- [ ] **Step 3: Las cuatro tarjetas en fila**

Copiar el envelope de `card-media` de la Task 1. Las cuatro llevan `"y": 260, "height": 200, "width": 280`, y cambian solo carpeta/`name`, `x`, `Property` y título:

| carpeta y `name` | `x` | `Property` | título |
|---|---|---|---|
| `card-average` | 40 | `Media` | `'AVERAGE'` |
| `card-averagex` | 340 | `Media con AVERAGEX` | `'AVERAGEX sobre la columna'` |
| `card-coalesce` | 640 | `Media con COALESCE` | `'AVERAGEX con COALESCE(_, 0)'` |
| `card-mas-cero` | 940 | `Media con mas cero` | `'AVERAGEX con  + 0'` |

Los dos primeros leerán **200** y los dos últimos **120**. Puestos en fila, el salto se ve sin leer nada.

- [ ] **Step 4: Registrar la página**

`pages.json` pasa a:

```json
  "pageOrder": [ "denominador", "mas-cero" ],
  "activePageName": "denominador"
```

- [ ] **Step 5: El runner**

Añadir a `CHECKS["blancos"]`:

```python
        (
            "las medidas de la pagina mas-cero",
            """
            EVALUATE
            ROW(
              "AVERAGEX",  [Media con AVERAGEX],
              "COALESCE",  [Media con COALESCE],
              "mas_cero",  [Media con mas cero]
            )
            """,
            {"AVERAGEX": 200, "COALESCE": 120, "mas_cero": 120},
        ),
```

- [ ] **Step 6: Refrescar, verificar, ejecutar**

Abrir el `.pbip`, refrescar, comprobar que la página 2 lee 200 · 200 · 120 · 120, y:

```bash
python lab/check_lab.py blancos localhost:<puerto>
```

Esperado: cuatro `ok`.

- [ ] **Step 7: Commit**

```bash
git add lab/blancos lab/check_lab.py
git commit -m "feat(lab): blancos, la pagina del + 0 que mueve la media de 200 a 120"
```

---

### Task 3: `claves-huerfanas`, las tres páginas

**Files:**
- Modify: `lab/claves-huerfanas/ClavesHuerfanas.SemanticModel/definition/tables/_Medidas.tmdl`
- Create: `.../ClavesHuerfanas.Report/definition/pages/{de-que-lado,donde-caen,limpiar-pierde}/page.json` y sus `visuals/`
- Modify: `.../pages/pages.json`; Delete: `.../pages/page1/`
- Modify: `lab/check_lab.py`

**Interfaces:**
- Consumes: el patrón de `visual.json` de la Task 1; la medida `Unidades`, que ya existe.
- Produces: `Productos`, `Valores del lado uno`, `Valores del lado muchos`, `Productos sin fila en blanco`, `Suma por producto`, `Suma sin fila en blanco`.

- [ ] **Step 1: Las medidas**

En `_Medidas.tmdl`, después de `measure Unidades`:

```
	/// Tres. La tabla base NO trae la fila en blanco.
	measure Productos = COUNTROWS(DimProducto)
		formatString: #,0
		lineageTag: b1a70000-0000-4000-8000-000000000311

	/// CUATRO. Aqui si aparece la fila en blanco que el motor anadio.
	measure 'Valores del lado uno' = COUNTROWS(VALUES(DimProducto[ProductoKey]))
		formatString: #,0
		lineageTag: b1a70000-0000-4000-8000-000000000312

	/// Cuatro tambien, y NO significa lo mismo: aqui el cuarto elemento es la clave 99 de
	/// verdad. Confundir los dos cuatros fue el error que detecto la review de la nota.
	measure 'Valores del lado muchos' = COUNTROWS(VALUES(Ventas[ProductoKey]))
		formatString: #,0
		lineageTag: b1a70000-0000-4000-8000-000000000313

	/// Tres. Excluye la fila en blanco a proposito.
	measure 'Productos sin fila en blanco' = COUNTROWS(ALLNOBLANKROW(DimProducto[ProductoKey]))
		formatString: #,0
		lineageTag: b1a70000-0000-4000-8000-000000000314

	/// 110: cuadra con el total.
	measure 'Suma por producto' = SUMX(VALUES(DimProducto[Nombre]), CALCULATE(SUM(Ventas[Unidades])))
		formatString: #,0
		lineageTag: b1a70000-0000-4000-8000-000000000315

	/// 60. ALLNOBLANKROW suena a "quitar el ruido" y pierde 50 unidades sin avisar.
	measure 'Suma sin fila en blanco' = SUMX(ALLNOBLANKROW(DimProducto[Nombre]), CALCULATE(SUM(Ventas[Unidades])))
		formatString: #,0
		lineageTag: b1a70000-0000-4000-8000-000000000316

```

- [ ] **Step 2: Página `de-que-lado` — cuatro tarjetas**

`page.json` con `"name": "de-que-lado"`, `"displayName": "1. De que lado se ve la fila en blanco"`.

Cuatro tarjetas, envelope de la Task 1, entidad `_Medidas`, todas con `"y": 240, "height": 200, "width": 280`:

| carpeta y `name` | `x` | `Property` | título | leerá |
|---|---|---|---|---|
| `card-productos` | 40 | `Productos` | `'COUNTROWS(DimProducto)'` | 3 |
| `card-lado-uno` | 340 | `Valores del lado uno` | `'VALUES del lado UNO'` | 4 |
| `card-lado-muchos` | 640 | `Valores del lado muchos` | `'VALUES del lado MUCHOS'` | 4 |
| `card-sin-blanco` | 940 | `Productos sin fila en blanco` | `'ALLNOBLANKROW'` | 3 |

- [ ] **Step 3: Página `donde-caen` — LA página del escenario**

`page.json` con `"name": "donde-caen"`, `"displayName": "2. Donde caen las unidades huerfanas"`.

Un solo visual, `.../visuals/barras-huerfanas/visual.json`, envelope de la Task 1 con:

```json
  "name": "barras-huerfanas",
  "position": { "x": 40, "y": 140, "z": 0, "height": 460, "width": 1200, "tabOrder": 0 },
```

y dentro de `visual`:

```json
    "visualType": "clusteredColumnChart",
    "query": {
      "queryState": {
        "Category": { "projections": [ {
          "field": { "Column": {
            "Expression": { "SourceRef": { "Entity": "DimProducto" } },
            "Property": "Nombre" } },
          "queryRef": "DimProducto.Nombre",
          "nativeQueryRef": "Nombre",
          "active": true } ] },
        "Y": { "projections": [ {
          "field": { "Measure": {
            "Expression": { "SourceRef": { "Entity": "_Medidas" } },
            "Property": "Unidades" } },
          "queryRef": "_Medidas.Unidades",
          "nativeQueryRef": "Unidades" } ] }
      }
    },
```

y de título: `'Unidades por producto — la barra sin nombre son 50 unidades que no estan en DimProducto'`.

Esperado al abrirlo: **cuatro barras, y la primera no tiene etiqueta.** Vale 50. Eso es «la categoría vacía que sale en el gráfico y que nadie sabe de dónde viene» del README, que hasta ahora solo se podía describir.

- [ ] **Step 4: Página `limpiar-pierde` — matriz y tres tarjetas**

`page.json` con `"name": "limpiar-pierde"`, `"displayName": "3. Limpiar la fila en blanco pierde 50"`.

La matriz, `.../visuals/matriz-productos/visual.json`, envelope de la Task 1 con `"position": { "x": 40, "y": 140, "z": 0, "height": 400, "width": 620, "tabOrder": 0 }` y:

```json
    "visualType": "pivotTable",
    "query": {
      "queryState": {
        "Rows": { "projections": [ {
          "field": { "Column": {
            "Expression": { "SourceRef": { "Entity": "DimProducto" } },
            "Property": "Nombre" } },
          "queryRef": "DimProducto.Nombre",
          "nativeQueryRef": "Nombre",
          "active": true } ] },
        "Values": { "projections": [ {
          "field": { "Measure": {
            "Expression": { "SourceRef": { "Entity": "_Medidas" } },
            "Property": "Unidades" } },
          "queryRef": "_Medidas.Unidades",
          "nativeQueryRef": "Unidades" } ] }
      }
    },
```

título: `'Unidades por producto — la fila sin nombre vale 50'`.

Tres tarjetas a la derecha, envelope de la Task 1, `"width": 260, "height": 120`:

| carpeta y `name` | `x` / `y` | `Property` | título | leerá |
|---|---|---|---|---|
| `card-total` | 700 / 140 | `Unidades` | `'Total de Ventas'` | 110 |
| `card-con-values` | 700 / 290 | `Suma por producto` | `'Suma por producto (VALUES)'` | 110 |
| `card-con-allnoblankrow` | 700 / 440 | `Suma sin fila en blanco` | `'Suma con ALLNOBLANKROW'` | 60 |

- [ ] **Step 5: Registrar las tres y borrar el lienzo vacío**

```json
  "pageOrder": [ "de-que-lado", "donde-caen", "limpiar-pierde" ],
  "activePageName": "donde-caen"
```

`activePageName` es `donde-caen` a propósito: es la que enseña la trampa de un vistazo, y es la que debe salir al abrir.

```bash
rm -rf lab/claves-huerfanas/ClavesHuerfanas.Report/definition/pages/page1
```

- [ ] **Step 6: El runner**

Añadir a `CHECKS["claves-huerfanas"]`:

```python
        (
            "las medidas de las tres paginas",
            """
            EVALUATE
            ROW(
              "Productos",         [Productos],
              "lado_uno",          [Valores del lado uno],
              "lado_muchos",       [Valores del lado muchos],
              "sin_fila_blanco",   [Productos sin fila en blanco],
              "total",             [Unidades],
              "suma_por_producto", [Suma por producto],
              "suma_sin_blanco",   [Suma sin fila en blanco]
            )
            """,
            {
                "Productos": 3,
                "lado_uno": 4,
                "lado_muchos": 4,
                "sin_fila_blanco": 3,
                "total": 110,
                "suma_por_producto": 110,
                "suma_sin_blanco": 60,
            },
        ),
```

- [ ] **Step 7: Refrescar y verificar**

Abrir, refrescar, y comprobar **a ojo** lo único que el runner no puede: que en `donde-caen` hay una barra sin etiqueta con 50, y que en `limpiar-pierde` la matriz tiene una fila sin nombre.

```bash
python lab/check_lab.py claves-huerfanas localhost:<puerto>
```

Esperado: tres `ok`.

- [ ] **Step 8: Commit**

```bash
git add lab/claves-huerfanas lab/check_lab.py
git commit -m "feat(lab): claves-huerfanas, la barra sin nombre que vale 50 unidades"
```

---

### Task 4: La tabla `Tiempos`

Sin esto la Task 5 no tiene datos que graficar. **No hay informe en esta tarea**: es dato, publicación y modelo.

**Files:**
- Modify: `lab/build_datasets.py`
- Create: `lab/rendimiento/Rendimiento.SemanticModel/definition/tables/Tiempos.tmdl`
- Modify: `lab/rendimiento/Rendimiento.SemanticModel/definition/model.tmdl`
- Modify (otro repo): `E:\MIS-REPO\SampleDataSets\dax-lab\README.md`

**Interfaces:**
- Produces: la entidad `Tiempos` con las columnas `Caso` (texto), `Grupo` (texto), `MedianaMs` (int64), `PicoMemoriaKB` (int64), `ConsultasSE` (int64), y el parquet `dax-lab/rendimiento/Tiempos.parquet`.

- [ ] **Step 1: Generar la tabla**

En `lab/build_datasets.py`, dentro de `def rendimiento()`, añadir al diccionario que devuelve:

```python
        # Las medianas que publica el README de rendimiento, medidas en frio el 2026-08-12 con
        # ClearCache antes de cada corrida y tres corridas por medida. Estan aqui para que la
        # pagina las grafique desde un DATO versionado en vez de un cuadro de texto que nadie
        # puede auditar.
        #
        # CUATRO filas y no nueve: el grupo A se cronometro con las SEIS medidas juntas, y
        # repartir esos 5 ms entre seis filas serian seis numeros que nadie midio.
        "Tiempos": pa.table(
            {
                "Caso": pa.array([
                    "Grupo A — las seis juntas",
                    "SUMX(Ventas, [Total])",
                    "SUMX(Ventas, Ventas[Importe])",
                    "CALCULATE([Total], FILTER(ALL(Ventas), [Total] > 900))",
                ], pa.string()),
                "Grupo": pa.array(["A", "B", "B", "B"], pa.string()),
                "MedianaMs": pa.array([5, 871, 3, 873], pa.int64()),
                "PicoMemoriaKB": pa.array([1027, 197300, 0, 197342], pa.int64()),
                "ConsultasSE": pa.array([3, 2, 1, 2], pa.int64()),
            }
        ),
```

- [ ] **Step 2: Regenerar y publicar**

```bash
python lab/build_datasets.py /e/MIS-REPO/SampleDataSets/dax-lab
```

Esperado: cinco líneas, la nueva `4 filas` en `rendimiento\Tiempos.parquet`.

Añadir a `E:\MIS-REPO\SampleDataSets\dax-lab\README.md`, al final de la sección `rendimiento/`:

```markdown
`Tiempos.parquet` carries the four measured medians the scenario publishes (cold, `ClearCache`
before each run, median of three). Four rows and not nine: group A was timed with its six
measures together, so splitting those 5 ms across six rows would invent six numbers nobody
measured.
```

Luego, desde `E:\MIS-REPO\SampleDataSets`:

```bash
git add dax-lab && git commit -m "data(dax-lab): add the measured timings behind the rendimiento scenario"
git push origin main
```

- [ ] **Step 3: La tabla en el modelo**

`lab/rendimiento/Rendimiento.SemanticModel/definition/tables/Tiempos.tmdl`:

```
/// Los tiempos MEDIDOS del escenario, no calculados aqui. Un visual de Power BI no puede
/// cronometrarse a si mismo, asi que la pagina "lo-que-cuesta" grafica esta tabla.
///
/// Medidos el 2026-08-12 en Power BI Desktop sobre un portatil: en frio (ClearCache antes de
/// cada corrida), tres corridas por medida, mediana. Metricas del propio motor, no tiempo de
/// pared del cliente. Lo que se publica es la RAZON (~290x), no los milisegundos: un numero
/// absoluto envejece con el hardware.
///
/// Cuatro filas y no nueve porque eso es lo que se midio. El grupo A se cronometro con sus
/// seis medidas juntas.
table Tiempos
	lineageTag: c0de0000-0000-4000-8000-000000000701

	/// La forma medida, escrita como se escribe en DAX.
	column Caso
		dataType: string
		lineageTag: c0de0000-0000-4000-8000-000000000702
		summarizeBy: none
		sourceColumn: Caso

	/// A = lo que el motor empuja al almacenamiento. B = lo que obliga a transitar contexto.
	column Grupo
		dataType: string
		lineageTag: c0de0000-0000-4000-8000-000000000703
		summarizeBy: none
		sourceColumn: Grupo

	/// Mediana de tres corridas en frio, en milisegundos.
	column MedianaMs
		dataType: int64
		formatString: #,0
		lineageTag: c0de0000-0000-4000-8000-000000000704
		summarizeBy: sum
		sourceColumn: MedianaMs

	column PicoMemoriaKB
		dataType: int64
		formatString: #,0
		lineageTag: c0de0000-0000-4000-8000-000000000705
		summarizeBy: sum
		sourceColumn: PicoMemoriaKB

	/// Consultas al motor de almacenamiento.
	column ConsultasSE
		dataType: int64
		lineageTag: c0de0000-0000-4000-8000-000000000706
		summarizeBy: sum
		sourceColumn: ConsultasSE

	partition Tiempos = m
		mode: import
		source =
				let
					Source = Parquet.Document(Web.Contents(DataBaseUrl, [RelativePath="Tiempos.parquet"]))
				in
					Source

	annotation PBI_ResultType = Table
```

En `model.tmdl`, añadir `ref table Tiempos` a la lista de `ref table`.

- [ ] **Step 4: Verificar que carga**

Abrir `lab/rendimiento/Rendimiento.pbip`, refrescar, y ejecutar en la vista de consulta DAX:

```dax
EVALUATE Tiempos ORDER BY Tiempos[MedianaMs]
```

Esperado: cuatro filas; `MedianaMs` 3, 5, 871, 873.

- [ ] **Step 5: Commit**

```bash
git add lab/build_datasets.py lab/rendimiento
git commit -m "feat(lab): la tabla Tiempos — la medicion como dato versionado"
```

---

### Task 5: `rendimiento`, las dos páginas

**Files:**
- Create: `lab/rendimiento/Rendimiento.Report/definition/pages/{mismo-numero,lo-que-cuesta}/` con sus `page.json` y `visuals/`
- Modify: `.../pages/pages.json`; Delete: `.../pages/page1/`
- Modify: `lab/check_lab.py`

**Interfaces:**
- Consumes: la entidad `Tiempos` de la Task 4 y las diez medidas que `_Medidas` ya tiene.

- [ ] **Step 1: Página `mismo-numero` — la matriz de pares**

`page.json` con `"name": "mismo-numero"`, `"displayName": "1. Los pares devuelven el mismo numero"`.

Un `tableEx`, `.../visuals/tabla-pares/visual.json`, envelope de la Task 1, `"position": { "x": 40, "y": 140, "z": 0, "height": 460, "width": 1200, "tabOrder": 0 }`, con **nueve proyecciones en el rol `Values`**, todas de la entidad `_Medidas`, en este orden:

`Alto FILTER`, `Alto predicado`, `Categoria por tabla`, `Categoria por columna`, `Cruce por tabla`, `Cruce por columnas`, `Suma con medida`, `Suma con columna`, `Alto con medida`.

Cada proyección con la forma:

```json
            {
              "field": { "Measure": {
                "Expression": { "SourceRef": { "Entity": "_Medidas" } },
                "Property": "Alto FILTER" } },
              "queryRef": "_Medidas.Alto FILTER",
              "nativeQueryRef": "Alto FILTER"
            },
```

título: `'Cada par devuelve el mismo numero — sin eso, comparar sus tiempos no diria nada'`.

- [ ] **Step 2: Página `lo-que-cuesta`**

`page.json` con `"name": "lo-que-cuesta"`, `"displayName": "2. Lo que cuesta cada forma (medido, no calculado)"`.

Dos barras horizontales. `.../visuals/barras-ms/visual.json`, envelope de la Task 1, `"position": { "x": 40, "y": 160, "z": 0, "height": 240, "width": 1200, "tabOrder": 0 }`:

```json
    "visualType": "clusteredBarChart",
    "query": {
      "queryState": {
        "Category": { "projections": [ {
          "field": { "Column": {
            "Expression": { "SourceRef": { "Entity": "Tiempos" } },
            "Property": "Caso" } },
          "queryRef": "Tiempos.Caso",
          "nativeQueryRef": "Caso",
          "active": true } ] },
        "Y": { "projections": [ {
          "field": { "Column": {
            "Expression": { "SourceRef": { "Entity": "Tiempos" } },
            "Property": "MedianaMs" } },
          "queryRef": "Sum(Tiempos.MedianaMs)",
          "nativeQueryRef": "MedianaMs" } ] }
      }
    },
```

título: `'Mediana en frio, milisegundos — medido el 2026-08-12, NO calculado ahora'`.

`.../visuals/barras-memoria/visual.json`: lo mismo con `"y": 420`, `Property` = `PicoMemoriaKB`, `queryRef` = `Sum(Tiempos.PicoMemoriaKB)`, y título `'Pico de memoria, KB — de cero a ~193 MB'`.

Y un `textbox` que fija el marco, `.../visuals/nota-metodo/visual.json`, sin bloque `query`:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.11.0/schema.json",
  "name": "nota-metodo",
  "position": { "x": 40, "y": 40, "z": 2, "height": 100, "width": 1200, "tabOrder": 2 },
  "visual": {
    "visualType": "textbox",
    "objects": {
      "general": [ { "properties": { "paragraphs": [ { "textRuns": [ { "value":
        "Estos tiempos se MIDIERON el 2026-08-12 en un portatil: en frio, tres corridas, mediana. No se estan calculando ahora y no se pueden calcular en un visual. Lo que se publica es la razon —unas 290 veces— no los milisegundos, porque un numero absoluto envejece con el hardware." } ] } ] } } ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

- [ ] **Step 3: Registrar y borrar el lienzo vacío**

```json
  "pageOrder": [ "mismo-numero", "lo-que-cuesta" ],
  "activePageName": "lo-que-cuesta"
```

```bash
rm -rf lab/rendimiento/Rendimiento.Report/definition/pages/page1
```

- [ ] **Step 4: El runner comprueba la tabla**

Añadir a `CHECKS["rendimiento"]`:

```python
        (
            "la tabla Tiempos trae las cuatro medianas medidas",
            """
            EVALUATE
            ROW(
              "casos",       COUNTROWS(Tiempos),
              "ms_maximo",   MAX(Tiempos[MedianaMs]),
              "ms_minimo",   MIN(Tiempos[MedianaMs]),
              "memoria_max", MAX(Tiempos[PicoMemoriaKB])
            )
            """,
            {"casos": 4, "ms_maximo": 873, "ms_minimo": 3, "memoria_max": 197342},
        ),
```

- [ ] **Step 5: Refrescar, verificar y ejecutar**

```bash
python lab/check_lab.py rendimiento localhost:<puerto>
```

Esperado: cuatro `ok`. Y a ojo: las dos barras largas de la página 2 son las dos formas con medida dentro.

- [ ] **Step 6: Commit**

```bash
git add lab/rendimiento lab/check_lab.py
git commit -m "feat(lab): rendimiento, los pares en vivo y los tiempos medidos"
```

---

### Task 6: Las medidas de Contoso, sin informe todavía

Separada del PBIR a propósito: son seis trampas de DAX que hay que escribir y comprobar **antes** de dibujarlas. Si una medida no hace lo que se cree, se descubre aquí.

**Files:**
- Modify: `lab/contoso/Contoso.SemanticModel/definition/tables/_Measures.tmdl`
- Modify: `lab/check_lab.py`

**Interfaces:**
- Produces, en la entidad `_Measures`: `Ventas ALLSELECTED`, `Ventas ALL`, `Ranking en la matriz`, `Ranking bien`, `Marca seleccionada`, `Suma con medida`, `Suma con columna`, `Margen con DIVIDE`, `Margen con cero`, `Ventas como texto`.

- [ ] **Step 1: Las diez medidas**

Al final de `_Measures.tmdl`, antes de la `partition`:

```
	/// allselected — respeta el filtro EXTERNO (slicer, filtro de pagina) y quita el interno.
	/// Al lado de [Ventas ALL] en una matriz con slicer, la diferencia es la nota entera.
	measure 'Ventas ALLSELECTED' = CALCULATE([Total Sales], ALLSELECTED(DimProduct[Brand]))
		formatString: #,0.00

	/// La misma forma con ALL: ignora TAMBIEN lo que el usuario selecciono en el slicer.
	measure 'Ventas ALL' = CALCULATE([Total Sales], ALL(DimProduct[Brand]))
		formatString: #,0.00

	/// rankx — en una matriz por Brand el contexto ya trae UNA sola marca, asi que
	/// VALUES(DimProduct[Brand]) es una tabla de una fila y el ranking es 1 en todas.
	measure 'Ranking en la matriz' = RANKX(VALUES(DimProduct[Brand]), [Total Sales])
		formatString: #,0

	/// La version que si rankea: ALL abre la tabla entera antes de ordenar.
	measure 'Ranking bien' = RANKX(ALL(DimProduct[Brand]), [Total Sales])
		formatString: #,0

	/// selectedvalue — devuelve la marca SOLO si queda exactamente una. Con ninguna y con dos
	/// o mas devuelve la alternativa, asi que la tarjeta no distingue los dos casos.
	measure 'Marca seleccionada' = SELECTEDVALUE(DimProduct[Brand], "(sin un valor unico)")

	/// sumx — referenciar una MEDIDA dentro del iterador provoca transicion de contexto. En la
	/// fila de Total de una matriz el resultado NO es la suma de las filas que se ven.
	measure 'Suma con medida' = SUMX(DimProduct, [Total Sales])
		formatString: #,0.00

	/// La misma forma sin medida dentro. Aqui el Total si cuadra con sus filas.
	measure 'Suma con columna' = SUMX(FactSales, FactSales[Quantity] * FactSales[NetPrice])
		formatString: #,0.00

	/// divide — al dividir por cero devuelve BLANCO, y el blanco BORRA la categoria del visual.
	measure 'Margen con DIVIDE' = DIVIDE([Gross Margin], [Total Sales])
		formatString: #,0.00 %

	/// La misma division protegida con un cero. El cero DIBUJA la categoria a ras de suelo.
	/// Los dos se leen igual en una tabla y distinto en un grafico: esa es la nota.
	measure 'Margen con cero' = COALESCE(DIVIDE([Gross Margin], [Total Sales]), 0)
		formatString: #,0.00 %

	/// format — convierte el numero en CADENA. A partir de ahi el visual ordena
	/// alfabeticamente, donde el 9 va despues del 10.
	measure 'Ventas como texto' = FORMAT([Total Sales], "#,0")

```

- [ ] **Step 2: Comprobar que hacen lo que se cree**

Abrir `lab/contoso/Contoso.pbip`, refrescar, y ejecutar en la vista de consulta DAX:

```dax
EVALUATE
SUMMARIZECOLUMNS(
  DimProduct[Brand],
  "ventas",          [Total Sales],
  "rank_matriz",     [Ranking en la matriz],
  "rank_bien",       [Ranking bien],
  "marca_sel",       [Marca seleccionada],
  "como_texto",      [Ventas como texto]
)
ORDER BY [ventas] DESC
```

Esperado, y **hay que mirarlo**: `rank_matriz` vale **1 en todas las filas** y `rank_bien` va 1, 2, 3… Si `rank_matriz` no sale 1 en todas, la medida no monta la trampa y hay que arreglarla antes de dibujar nada.

- [ ] **Step 3: El runner**

Añadir a `CHECKS["contoso"]`:

```python
        (
            "las medidas de las paginas de informe",
            """
            EVALUATE
            ROW(
              "rank_matriz_distintos", COUNTROWS(DISTINCT(
                  SELECTCOLUMNS(VALUES(DimProduct[Brand]), "r", [Ranking en la matriz]))),
              "rank_bien_distintos",   COUNTROWS(DISTINCT(
                  SELECTCOLUMNS(VALUES(DimProduct[Brand]), "r", [Ranking bien]))),
              "marca_sin_seleccion",   [Marca seleccionada],
              "suma_con_columna",      ROUND([Suma con columna], 2)
            )
            """,
            {
                "rank_matriz_distintos": 1,
                "marca_sin_seleccion": "(sin un valor unico)",
            },
        ),
```

`rank_matriz_distintos` = **1** es la afirmación entera: hay un solo valor de ranking distinto en todas las marcas, y ese valor es 1. `rank_bien_distintos` y `suma_con_columna` se dejan **fuera** del diccionario esperado porque dependen de cuántas marcas tenga el modelo y de una cifra con decimales; se ejecutan para que un error las haga fallar, pero no se afirma su valor.

- [ ] **Step 4: Ejecutar**

```bash
python lab/check_lab.py contoso localhost:<puerto>
```

Esperado: los `ok` de siempre más el nuevo, y las 34 consultas de las notas siguen verdes.

- [ ] **Step 5: Commit**

```bash
git add lab/contoso lab/check_lab.py
git commit -m "feat(lab): las diez medidas que montan las trampas visuales de Contoso"
```

---

### Task 7: Contoso — las dos páginas con slicer

**Files:**
- Create: `lab/contoso/Contoso.Report/definition/pages/{allselected-slicer,selectedvalue-tarjeta}/`
- Modify: `.../pages/pages.json`; Delete: `.../pages/page1/`

**Interfaces:**
- Consumes: `Ventas ALLSELECTED`, `Ventas ALL`, `Marca seleccionada` de la Task 6; el patrón de la Task 1.

- [ ] **Step 1: El slicer, que es el visual nuevo de esta tarea**

`.../pages/allselected-slicer/visuals/slicer-marca/visual.json`:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.11.0/schema.json",
  "name": "slicer-marca",
  "position": { "x": 40, "y": 140, "z": 0, "height": 460, "width": 260, "tabOrder": 0 },
  "visual": {
    "visualType": "slicer",
    "query": {
      "queryState": {
        "Values": { "projections": [ {
          "field": { "Column": {
            "Expression": { "SourceRef": { "Entity": "DimProduct" } },
            "Property": "Brand" } },
          "queryRef": "DimProduct.Brand",
          "nativeQueryRef": "Brand",
          "active": true } ] }
      }
    },
    "visualContainerObjects": {
      "title": [ { "properties": {
        "show": { "expr": { "Literal": { "Value": "true" } } },
        "text": { "expr": { "Literal": { "Value": "'Selecciona marcas aqui'" } } } } } ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

- [ ] **Step 2: La matriz que enseña la diferencia**

`page.json` con `"name": "allselected-slicer"`, `"displayName": "ALLSELECTED — respeta el slicer, ignora el interno"`.

`.../visuals/matriz-allselected/visual.json`, `pivotTable` como en la Task 3, `"position": { "x": 320, "y": 140, "z": 1, "height": 460, "width": 920, "tabOrder": 1 }`, con:
- `Rows`: columna `DimProduct[Brand]`
- `Values`: tres proyecciones de `_Measures` — `Total Sales`, `Ventas ALLSELECTED`, `Ventas ALL`

título: `'Selecciona 2-3 marcas: ALLSELECTED cambia con el slicer y ALL no'`.

- [ ] **Step 3: La página de la tarjeta ambigua**

`page.json` con `"name": "selectedvalue-tarjeta"`, `"displayName": "SELECTEDVALUE — la tarjeta que no distingue dos casos"`.

Un slicer idéntico al del Step 1 (carpeta `slicer-marca-2`, `name` a juego), y a su derecha una tarjeta, envelope de la Task 1, `"position": { "x": 320, "y": 240, "z": 1, "height": 200, "width": 500 }`, `Property` = `Marca seleccionada`, entidad `_Measures`, título `'Marca seleccionada'`.

Y un `textbox` (envelope del Step 2 de la Task 5) en `"y": 470`, con el texto:

```
Prueba las tres cosas: no selecciones nada, selecciona UNA marca, y selecciona DOS. La tarjeta da el mismo "(sin un valor unico)" en el primer caso y en el tercero. No distingue "el usuario no eligio" de "el usuario eligio varias", y esa ambiguedad es la trampa.
```

- [ ] **Step 4: Registrar y borrar el lienzo vacío**

```json
  "pageOrder": [ "allselected-slicer", "selectedvalue-tarjeta" ],
  "activePageName": "allselected-slicer"
```

```bash
rm -rf lab/contoso/Contoso.Report/definition/pages/page1
```

- [ ] **Step 5: Verificar interactuando**

Abrir, refrescar, y **usar el slicer**, que es lo único que prueba estas dos páginas:
- En `allselected-slicer`, seleccionar 2-3 marcas: la columna `Ventas ALLSELECTED` cambia y `Ventas ALL` no se mueve.
- En `selectedvalue-tarjeta`, comprobar los tres casos del textbox.

El runner **no puede** comprobar esto: no hay slicer en una consulta DAX. Es exactamente la razón por la que estas dos páginas existen.

- [ ] **Step 6: Commit**

```bash
git add lab/contoso
git commit -m "feat(lab): contoso, las dos trampas que necesitan un slicer para existir"
```

---

### Task 8: Contoso — las dos páginas de matriz

**Files:**
- Create: `lab/contoso/Contoso.Report/definition/pages/{rankx-matriz,sumx-total}/`
- Modify: `.../pages/pages.json`

**Interfaces:**
- Consumes: `Ranking en la matriz`, `Ranking bien`, `Suma con medida`, `Suma con columna` de la Task 6.

- [ ] **Step 1: `rankx-matriz`**

`page.json` con `"name": "rankx-matriz"`, `"displayName": "RANKX — 1 en todas las filas de la matriz"`.

Una `pivotTable` (patrón de la Task 3), `"position": { "x": 40, "y": 200, "z": 0, "height": 460, "width": 1200, "tabOrder": 0 }`:
- `Rows`: `DimProduct[Brand]`
- `Values`: `Total Sales`, `Ranking en la matriz`, `Ranking bien`

título: `'La columna del medio vale 1 en TODAS las filas'`.

Un `textbox` en `"y": 60, "height": 120`:

```
La matriz ya trae UNA sola marca al contexto de cada fila, asi que VALUES(DimProduct[Brand]) dentro de RANKX es una tabla de una fila y todo el mundo queda primero. La tercera columna usa ALL, que abre la tabla entera antes de ordenar, y esa si rankea.
```

- [ ] **Step 2: `sumx-total`**

`page.json` con `"name": "sumx-total"`, `"displayName": "SUMX — el Total que no cuadra con sus filas"`.

Una `pivotTable`, misma posición:
- `Rows`: `DimProduct[Brand]`
- `Values`: `Suma con medida`, `Suma con columna`

título: `'Mira la fila de Total: la primera columna no suma sus propias filas'`.

Un `textbox` en `"y": 60, "height": 120`:

```
Referenciar una MEDIDA dentro de SUMX provoca transicion de contexto: cada fila se convierte en filtro. En la fila de Total el iterador recorre la tabla entera de una vez, y el numero que sale no es la suma de las filas que ves encima. La segunda columna escribe la agregacion a mano y su Total si cuadra.
```

- [ ] **Step 3: Registrar**

```json
  "pageOrder": [ "allselected-slicer", "selectedvalue-tarjeta", "rankx-matriz", "sumx-total" ],
```

- [ ] **Step 4: Verificar**

Abrir, refrescar, y comprobar a ojo lo que la consulta ya confirmó en la Task 6: `Ranking en la matriz` vale 1 en todas las filas, y en `sumx-total` la fila de Total de la primera columna no coincide con la suma de las de arriba.

- [ ] **Step 5: Commit**

```bash
git add lab/contoso
git commit -m "feat(lab): contoso, las dos trampas que solo aparecen dentro de una matriz"
```

---

### Task 9: Contoso — las dos páginas de comparación lado a lado

**Files:**
- Create: `lab/contoso/Contoso.Report/definition/pages/{blanco-desaparece,format-ordena-mal}/`
- Modify: `.../pages/pages.json`

**Interfaces:**
- Consumes: `Margen con DIVIDE`, `Margen con cero`, `Ventas como texto`, `Total Sales` de la Task 6.

- [ ] **Step 1: `blanco-desaparece` — dos gráficos idénticos**

`page.json` con `"name": "blanco-desaparece"`, `"displayName": "El blanco borra la categoria; el cero la dibuja"`.

Dos `clusteredColumnChart` (patrón de la Task 1), **idénticos salvo la medida**:

| carpeta y `name` | `position` | `Y` → `Property` | título |
|---|---|---|---|
| `barras-blanco` | x 40, y 200, w 590, h 420 | `Margen con DIVIDE` | `'Con DIVIDE — las categorias sin ventas DESAPARECEN'` |
| `barras-cero` | x 650, y 200, w 590, h 420 | `Margen con cero` | `'Con COALESCE(_, 0) — las mismas categorias se DIBUJAN'` |

Los dos con `Category` = columna `DimProduct[CategoryName]`, entidad de la medida `_Measures`.

Un `textbox` en `"y": 60, "height": 130`:

```
Los dos graficos usan los mismos datos y la misma division. El de la izquierda devuelve BLANCO donde no hay ventas y el de la derecha devuelve cero. En una tabla los dos ocupan una celda y se leen igual; aqui uno tiene menos barras que el otro. Ninguno esta mal: el blanco dice "no lo medi" y el cero dice "lo medi y dio cero". Lo que esta mal es no saber cual estas publicando.
```

- [ ] **Step 2: `format-ordena-mal` — dos tablas**

`page.json` con `"name": "format-ordena-mal"`, `"displayName": "FORMAT — el 9 va despues del 10"`.

Dos `tableEx` (patrón del Step 1 de la Task 5), lado a lado:

| carpeta y `name` | `position` | `Values` | título |
|---|---|---|---|
| `tabla-numero` | x 40, y 200, w 590, h 420 | `DimProduct[Brand]` + medida `Total Sales` | `'Numero — se ordena por magnitud'` |
| `tabla-texto` | x 650, y 200, w 590, h 420 | `DimProduct[Brand]` + medida `Ventas como texto` | `'Cadena — se ordena alfabeticamente'` |

Un `textbox` en `"y": 60, "height": 130`:

```
FORMAT no cambia como se ve un numero: lo convierte en una CADENA. Ordena la segunda tabla por su columna de ventas y mira el orden que sale: alfabetico, donde "9" va despues de "10" porque "9" > "1". A partir de FORMAT tampoco se suma ni se compara como numero.
```

- [ ] **Step 3: Registrar las seis páginas de Contoso**

```json
  "pageOrder": [
    "allselected-slicer", "selectedvalue-tarjeta",
    "rankx-matriz", "sumx-total",
    "blanco-desaparece", "format-ordena-mal"
  ],
  "activePageName": "allselected-slicer"
```

- [ ] **Step 4: Verificar**

Abrir, refrescar, y comprobar que el gráfico de la izquierda de `blanco-desaparece` tiene **menos barras** que el de la derecha. Si tienen las mismas, el modelo no tiene ninguna categoría sin ventas y la página no demuestra nada: en ese caso hay que filtrar la página a un rango de fechas donde alguna categoría quede vacía, y decirlo en el textbox.

En `format-ordena-mal`, ordenar la segunda tabla por su columna de ventas haciendo clic en la cabecera y comprobar el orden alfabético.

- [ ] **Step 5: Commit**

```bash
git add lab/contoso
git commit -m "feat(lab): contoso, el blanco que borra la barra y el FORMAT que ordena mal"
```

---

### Task 10: La documentación cierra el círculo

**Files:**
- Modify: `lab/README.md`
- Modify: `lab/{blancos,claves-huerfanas,rendimiento,contoso}/README.md`
- Modify: `docs/REVIEW.md`

- [ ] **Step 1: Cada README enlaza su página**

En el README de cada escenario, al final de la sección de cada trampa que ahora tiene página, una línea:

```markdown
> Esta trampa también está **dibujada**: página «<displayName>» del informe. Ábrela con el
> `.pbip` y míralo, que es donde se ve lo que el resultado de la consulta no enseña.
```

- [ ] **Step 2: `lab/README.md` dice qué verifica el runner y qué no**

Añadir una sección después de «Cómo usarlos»:

```markdown
## Los informes, y el límite de lo que se comprueba

Los cuatro escenarios traen **trece páginas**, una por trampa, y existen para las trampas que
**solo viven dentro de un visual**: el blanco que borra una barra mientras el cero la dibuja, la
categoría sin nombre de una relación rota, `ALLSELECTED` cambiando según el filtro venga de un
slicer, `RANKX` devolviendo 1 en todas las filas de una matriz. De esas el README puede hablar;
no puede enseñarlas.

Lo que se comprueba solo: **las medidas**. Cada una de las veintitrés que alimentan las páginas está
en [`check_lab.py`](./check_lab.py) con su valor esperado, así que si un número cambia, sale rojo.

Lo que **no** se comprueba solo: **el dibujo**. Ningún test sabe si la barra se pintó. Eso se
verifica abriendo el `.pbip`, y en las dos páginas con slicer hace falta además mover el slicer —
en una consulta DAX no hay slicer, que es justo por lo que esas páginas existen.
```

- [ ] **Step 3: `docs/REVIEW.md`, en «Lo que NO está hecho»**

```markdown
- **El renderizado de los informes no está en ningún test.** Las veintitrés medidas que alimentan
  las trece páginas sí están en `check_lab.py`; que el visual se pinte se comprueba abriéndolo a
  mano. No hay forma de automatizarlo sin un Power BI Desktop en CI, y no lo hay.
```

- [ ] **Step 4: Los gates**

```bash
python scripts/check_doc_claims.py
python scripts/check_examples.py
python -m unittest discover -s scripts -t scripts
```

Esperado: `OK` los tres. `check_doc_claims` cuenta escenarios de laboratorio y **no** páginas de informe, así que trece no le afecta; si alguna frase nueva dice «cuatro escenarios» tiene que seguir siendo cierta.

- [ ] **Step 5: Commit**

```bash
git add lab docs/REVIEW.md
git commit -m "docs(lab): los README enlazan sus paginas y dicen que no se comprueba solo"
```

## Notas de ejecución

**El orden importa en un sitio:** la Task 4 (`Tiempos`) va antes de la Task 5, y la Task 6 (las
medidas de Contoso) antes de las tareas 7, 8 y 9. El resto es independiente.

**La Task 1 es un gate.** Si el PBIR escrito a mano no renderiza, las tareas 2–9 no tienen
sentido hasta arreglarlo. No empezar la Task 2 sin haber visto la página 1 dibujada.

**Cada verificación necesita Power BI Desktop abierto y refrescado**, y el puerto sale de:

```bash
python lab/check_lab.py <escenario>
```

sin puerto, que lista las instancias locales con el comando ya montado.
