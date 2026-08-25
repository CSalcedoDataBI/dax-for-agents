# Informes del laboratorio: la trampa, dibujada

**Fecha:** 2026-08-17
**Estado:** diseño aprobado, pendiente de plan

## El problema

Los cuatro escenarios de `lab/` tienen el `.Report` vacío: un lienzo de 1280×720 con el título
«Lienzo vacío» y ni un visual. Está así a propósito —las consultas se ejecutan contra el modelo,
no contra el informe— y esa decisión sigue siendo correcta para *ejecutar* el laboratorio.

Lo que deja fuera es otra cosa. **Varias de las trampas que documenta este repositorio solo
existen dentro de un visual.** Un blanco y un cero se leen igual en el resultado de una consulta;
en un gráfico, el blanco borra la barra y el cero la dibuja a ras de suelo. `ALLSELECTED` cambia
de respuesta según el filtro venga de un *slicer* o de la propia consulta, y en una consulta no
hay slicer. `RANKX` en una matriz devuelve 1 en todas las filas por una razón que la matriz
provoca. De esas trampas el README puede *hablar*; no puede **enseñarlas**.

Un informe con esas páginas no es decoración: es la única forma de evidencia disponible para una
clase entera de comportamientos.

## Alcance

**Trece páginas**, una por trampa. Una página se lee sola, se enlaza desde su nota o su ejemplo, y
si su trampa se puede enseñar bien en texto, **no existe**. Ese filtro deja fuera 24 de las 30
notas de campo y es deliberado.

Solo **visuales nativos**. Un Deneb o cualquier visual del marketplace obligaría a quien descargue
el `.pbip` a instalarlo antes de ver nada, y eso rompe la promesa que sostiene todo el
laboratorio: que el proyecto abre y funciona en la máquina de cualquiera.

### blancos — 2 páginas

| página | visual | lo que monta |
|---|---|---|
| `denominador` | columnas `Metros` por `Nombre` + 4 tarjetas | Este y Oeste **no dibujan barra**. Las tarjetas dan 200 y 120 sobre los mismos datos |
| `mas-cero` | 4 tarjetas en fila | `AVERAGE` 200 · `AVERAGEX` 200 · con `COALESCE` 120 · con `+ 0` **120** |

La primera página es la que el README no puede dar: la ausencia de barra **es** el blanco. En la
tabla de cinco filas el hueco es una celda vacía que se lee; en el gráfico es una tienda que
desapareció.

### claves-huerfanas — 3 páginas

| página | visual | lo que monta |
|---|---|---|
| `de-que-lado` | 4 tarjetas | 3 · 4 · 4 · 3. Los dos cuatros **no significan lo mismo** |
| `donde-caen` | barras `Unidades` por `Nombre` | una barra **sin nombre** con 50 unidades, que no está en los datos |
| `limpiar-pierde` | matriz + 3 tarjetas | 110 · 110 · **60**. La matriz enseña de dónde salen los 50 que faltan |

`donde-caen` es la página con más valor del escenario. «La categoría vacía que sale en el gráfico
y que nadie sabe de dónde viene» es literalmente lo que el README describe y no puede mostrar.

### rendimiento — 2 páginas

| página | visual | lo que monta |
|---|---|---|
| `mismo-numero` | matriz de las 9 medidas por pares | la precondición: las dos formas de cada par devuelven lo mismo. **Calculado en vivo** |
| `lo-que-cuesta` | barras horizontales desde `Tiempos` | 871 ms contra 3 ms, y 197.300 KB contra 0. **Medido el 2026-08-12, no calculado aquí** |

Un visual de Power BI no puede cronometrarse a sí mismo, así que la segunda página grafica una
**tabla `Tiempos` nueva en el modelo** con las medianas ya publicadas en el README, su fecha y su
método escritos en el TMDL. Eso convierte la medición en un dato versionado —revisable en el
diff, regenerable con `build_datasets.py`— en vez de un cuadro de texto que nadie puede auditar.

La tabla tiene **cuatro filas, no nueve**, porque eso es lo que se midió: el grupo A se cronometró
con las seis medidas juntas y en frío, y repartir esos 5 ms entre seis filas sería inventarse seis
números que nadie midió.

| Caso | MedianaMs | PicoMemoriaKB | ConsultasSE |
|---|---|---|---|
| Grupo A — las seis juntas | 5 | 1.027 | 3 |
| `SUMX(Ventas, [Total])` | 871 | 197.300 | 2 |
| `SUMX(Ventas, Ventas[Importe])` | 3 | 0 | 1 |
| `CALCULATE([Total], FILTER(ALL(Ventas), [Total] > 900))` | 873 | 197.342 | 2 |

La página lleva escrito en el título que son tiempos medidos en una máquina concreta y que lo que
se publica es la **razón**, no los milisegundos.

### contoso — 6 páginas

El criterio, aplicado a las 30 notas: entra la que **necesita** un visual para existir.

| página | nota | visual | por qué no cabe en una consulta |
|---|---|---|---|
| `allselected-slicer` | [`allselected`](../../../skills/dax-reference/notes/allselected.md) | slicer de `Brand` + matriz + tarjetas | respeta el filtro **externo** y quita el interno. Sin slicer no hay filtro externo que respetar |
| `rankx-matriz` | [`rankx`](../../../skills/dax-reference/notes/rankx.md) | matriz por `Brand` con la medida de ranking | la matriz trae **una sola marca** al contexto de cada fila, así que rankea 1 en todas |
| `selectedvalue-tarjeta` | [`selectedvalue`](../../../skills/dax-reference/notes/selectedvalue.md) | slicer + tarjeta | la tarjeta vacía **no distingue** «seleccionó varios» de «no seleccionó nada» |
| `sumx-total` | [`sumx`](../../../skills/dax-reference/notes/sumx.md) | matriz con fila de Total | el **Total** no cuadra con la suma de las filas que ves. En una consulta no hay fila de total |
| `blanco-desaparece` | [`divide`](../../../skills/dax-reference/notes/divide.md) · [`count`](../../../skills/dax-reference/notes/count.md) | dos gráficos idénticos, uno con blanco y otro con cero | el blanco **borra la categoría**; el cero la dibuja. En un resultado tabular los dos ocupan una celda |
| `format-ordena-mal` | [`format`](../../../skills/dax-reference/notes/format.md) | dos tablas, número contra cadena | el visual ordena la cadena alfabéticamente: **el 9 va después del 10** |

## Lo que hay que tocar además del PBIR

Esta es la parte que no se ve en el enunciado y es la mitad del trabajo.

**Medidas nuevas.** Una tarjeta no acepta `AVERAGE(Tiendas[Metros])` escrito dentro: consume una
medida. Salen unas catorce repartidas entre los cuatro modelos, y cada una lleva su `///`
diciendo qué trampa monta y contra qué otra medida hay que leerla. Son parte del contenido
didáctico, no andamiaje: `Media con mas cero` existe **para** salir 120 al lado de un 200.

**La tabla `Tiempos`** en el modelo de rendimiento, producida por `build_datasets.py` como los
demás parquet y publicada en `SampleDataSets/dax-lab/rendimiento` junto a `Ventas.parquet`.

**`check_lab.py` crece.** Cada medida nueva es una consulta más con su valor esperado. Una medida
que cambie de resultado pone el escenario en rojo igual que hoy. Es lo que impide que estas
catorce medidas se conviertan en código que nadie comprueba.

**Los README enlazan a su página.** Cada trampa que ahora tiene una página lo dice donde el lector
ya está mirando.

## Riesgos, dichos antes de empezar

**No hay CLI.** La skill `powerbi-report-authoring` se apoya en `powerbi-report-author`, que no
está instalada y no existe con ese nombre en npm. El PBIR va escrito a mano.

La respuesta a eso es el orden del plan, no una promesa: **se construye una sola página primero**
—`blancos/denominador`, la más simple—, se abre en Power BI Desktop y se comprueba que renderiza
**antes** de fabricar las otras doce. Si el `visual.json` escrito a mano no vuela, se sabe en la
página uno.

Tampoco hay plantilla que copiar. El informe del maestro de Contoso son cinco imágenes y cuatro
cuadros de texto —una portada de marca, la misma que se dejó fuera al traer el modelo— y no
contiene ni un visual de datos. Lo que sí da es el **sobre** confirmado: `visualContainer` 2.11.0,
`position` con `x/y/z/height/width/tabOrder`, y `visual.objects` con expresiones. Lo que falta por
verificar es el bloque `query.queryState` con sus proyecciones, y eso es exactamente lo que
comprueba la página uno.

**El runner no puede verificar el dibujo.** Comprueba que las medidas devuelven lo publicado, que
es lo que puede comprobar. Que el visual se vea como debe se verifica abriéndolo y con captura, y
eso queda dicho en el README del laboratorio en vez de insinuar una cobertura que no existe.

**El tema `CY25SU11`** viene del `report.json` actual y se conserva. No se define tema propio: un
tema es una decisión de marca y este repositorio no tiene marca a propósito.

## Lo que este diseño NO hace

- **No convierte los escenarios en dashboards.** No hay KPIs, ni tendencias, ni portadas. Una
  página, una trampa, y lo mínimo alrededor para que se entienda sola.
- **No cubre las 30 notas.** Veinticuatro se enseñan mejor en texto y se quedan en texto.
- **No mide rendimiento en vivo.** La página de tiempos grafica lo medido y lo dice.
- **No toca el modelo de Contoso más allá de `_Measures`.** Ni relaciones nuevas, ni marcar la
  tabla de fechas: los números publicados por 29 notas salen del modelo tal como está.
