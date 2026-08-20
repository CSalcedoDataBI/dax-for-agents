# lab — evidencia que se puede ejecutar

Las notas de campo de [`dax-reference/notes/`](../dax-reference/notes/) traen la consulta que
demuestra cada trampa y el número que devolvió. Este directorio es el otro lado de esa
promesa: **los modelos donde ejecutarlas**.

## Por qué existe

Por dos razones distintas, y conviene no mezclarlas.

**La primera: el modelo base.** Veintinueve de las treinta notas se midieron sobre Contoso
Retail, y ese modelo vivía en una máquina. El lector tenía la consulta y el número, y ninguna
forma de ejecutarlos. Ahora está aquí: [`contoso`](./contoso/).

**La segunda: lo que Contoso no puede enseñar.** Al escribir las primeras notas hubo tres que
no se escribieron porque el modelo base no podía demostrarlas — y una nota sin demostrar no se
escribe:

| No se pudo demostrar | Por qué | Escenario que lo resuelve |
|---|---|---|
| La fila en blanco de una relación con claves huérfanas | Contoso tiene la integridad referencial intacta | [`claves-huerfanas`](./claves-huerfanas/) |
| `AVERAGE` vs `AVERAGEX` con blancos | Ninguna columna numérica tiene blancos | [`blancos`](./blancos/) |
| Cualquier cifra de rendimiento | 126.524 filas se resuelven en milisegundos | [`rendimiento`](./rendimiento/) |

Las tres tienen ya su escenario. El de rendimiento además **desmintió** lo que se fue a
buscar: se construyó para enseñar que `FILTER` sobre una tabla entera es caro, y resultó no
serlo. Lo que cuesta es la transición de contexto. Los números están en su
[README](./rendimiento/README.md).

## Cómo son los modelos

**Los cuatro se conectan igual.** Lo que se versiona aquí son `.pbip` de kilobytes; las filas
viven fuera, en parquet publicados en
[`CSalcedoDataBI/SampleDataSets`](https://github.com/CSalcedoDataBI/SampleDataSets) — repo
**público**, licencia **MIT**, datos **100% sintéticos**. Cada modelo los lee por
`raw.githubusercontent.com`:

```
Parquet.Document(Web.Contents(DataBaseUrl, [RelativePath="Ventas.parquet"]))
```

`DataBaseUrl` es un **parámetro M de verdad** (`IsParameterQuery`), así que cada partición
queda a salvo del cortafuegos de privacidad y apuntar a un fork, una rama o un espejo local es
cambiar un solo valor.

| escenario | carpeta publicada | tamaño | filas |
|---|---|---|---|
| [`blancos`](./blancos/) | `dax-lab/blancos` | 1 KB | 5 |
| [`claves-huerfanas`](./claves-huerfanas/) | `dax-lab/claves-huerfanas` | 2 KB | 3 + 4 |
| [`rendimiento`](./rendimiento/) | `dax-lab/rendimiento` | 385 KB | 2.000.000 |
| [`contoso`](./contoso/) | `contoso-retail` | 2,2 MB | 126.524 + dimensiones |

Que sea el mismo patrón en los cuatro no es cosmética. **Lo que se publica de este repo son
los `.pbip`**, y un `.pbip` solo vale si refresca en la máquina del que lo descarga: sin
autenticación, sin SQL Server, sin rutas locales, sin credenciales que pedir. Un origen por
escenario sería un origen que arreglar por escenario.

**El precio es que los cuatro necesitan internet para refrescar.** Si
`raw.githubusercontent.com` no es alcanzable, no hay datos. Se acepta a cambio de que el repo
no cargue con los megabytes y de que no haya nada que configurar.

Los datos siguen siendo legibles sin abrir Power BI: los dos escenarios de comportamiento son
cinco y siete filas elegidas a mano y están escritas en el README de cada uno, fila a fila.
Que estén en un parquet en vez de en el TMDL no las esconde — las publica.

## Cómo usarlos

1. Abre el `.pbip` del escenario en Power BI Desktop y **refresca**. Al abrir un PBIP el
   modelo carga sin datos: hay que pedirlo. No hay nada que configurar; la primera vez Power
   BI pregunta por el nivel de privacidad del origen web y basta con **Anónimo/Público**.
2. Ejecuta las consultas del `README.md` de ese escenario en la vista de consulta DAX.
3. Compara con la tabla de resultados publicada.

En `contoso` el paso 2 son las consultas de las **notas de campo**, que están en
[`dax-reference/notes/`](../dax-reference/notes/) y no repetidas en su README.

El `.gitignore` de cada escenario excluye `.pbi/`, que es la caché local de Power BI Desktop
(unos megas de binario por modelo). Solo se versiona el texto.

## Los informes, y el límite de lo que se comprueba

Los cuatro escenarios traen **trece páginas**, una por trampa, y existen para las trampas que
**solo viven dentro de un visual**: el blanco que borra una barra mientras el cero la dibuja, la
categoría sin nombre de una relación rota, `ALLSELECTED` cambiando según el filtro venga de un
slicer, `RANKX` devolviendo 1 en todas las filas de una matriz. De esas el README puede hablar;
no puede enseñarlas.

Lo que se comprueba solo: **las medidas**. Cada una de las veintitrés que alimentan las páginas
está en [`check_lab.py`](./check_lab.py) con su valor esperado, así que si un número cambia, sale
rojo.

Lo que **no** se comprueba solo: **el dibujo**. Ningún test sabe si la barra se pintó. Eso se
verifica abriendo el `.pbip`, y en las dos páginas con slicer hace falta además mover el slicer —
en una consulta DAX no hay slicer, que es justo por lo que esas páginas existen.

Y no es una precaución teórica. Al construirlas, mirar el dibujo encontró tres cosas que ninguna
consulta habría encontrado: un gráfico que salía **vacío** porque a una columna en el pozo de
valores le faltaba el envoltorio `Aggregation`, una tabla que se quedaba en la cabecera por un
`"active": true` de más, y dos páginas cuyo diseño daba por hecho un contraste que los datos no
tenían. Las tres abren el informe **sin un solo error**.


## Estructura

```
lab/
  check_lab.py              ejecuta y compara — el runner
  notes_expected.py         lo que devuelve la consulta de cada nota sobre contoso
  dump_notes.py             regenera notes_expected.py contra un modelo abierto
  build_datasets.py         produce los parquet de los tres escenarios sintéticos
  <escenario>/
    README.md               qué demuestra, las consultas y los resultados medidos
    <Nombre>.pbip           el proyecto que se abre
    <Nombre>.SemanticModel/ TMDL: tablas, relaciones y expressions.tmdl (DataBaseUrl)
    <Nombre>.Report/        informe vacío de una página
    .gitignore              excluye .pbi/
```

[`build_datasets.py`](./build_datasets.py) es lo que produce los parquet de `blancos`,
`claves-huerfanas` y `rendimiento`. Existe para que los ficheros publicados no sean un binario
opaco: quien dude de que el parquet dice lo que dice el README, lo regenera y compara. La
generación es **determinista** —sin azar y sin fechas—, así que dos ejecuciones dan lo mismo.

```bash
python lab/build_datasets.py <directorio-destino>
```

Escribe ficheros y nada más; publicar el destino es un paso aparte y a mano.

El informe está vacío a propósito: un `.pbip` declara artefactos de **informe**, y es el
informe el que enlaza al modelo por `definition.pbir`. Un `.pbip` que apunta directo al
`SemanticModel` abre Power BI Desktop en un estado sin tablas — comprobado al construir el
primer escenario.

## Comprobar sin abrir nada a mano

[`check_lab.py`](./check_lab.py) ejecuta las consultas de cada escenario y las compara con el
resultado publicado. Si un número cambia, falla.

```bash
python lab/check_lab.py claves-huerfanas localhost:<puerto>
```

Sin puerto, busca las instancias locales de Power BI Desktop que **estén escuchando** y las
lista con el comando ya montado.

`contoso` hace además otra cosa: ejecuta **las 34 consultas publicadas en las notas de
campo** y las compara con [`notes_expected.py`](./notes_expected.py). Las consultas no están
copiadas ahí — las lee del propio `.md` de cada nota, así que editar una nota cambia lo que
se ejecuta. Es lo que convierte una nota de «afirmación con evidencia citada» en test.

```bash
python lab/check_lab.py contoso localhost:<puerto>
```

Necesita `pyadomd` **y** el proveedor ADOMD.NET, que no viene con pip: lo instalan Power BI
Desktop y SSMS. El runner lo busca solo en el GAC; si falta, lo dice por su nombre.

**No corre en CI**, y es deliberado: necesita un motor tabular con los datos cargados, y CI no
tiene Power BI Desktop. Es una herramienta local para cuando se toca un escenario o se
sospecha de una nota.

### Validar la estructura del proyecto

Que el modelo cargue en tu máquina no prueba que el `.pbip` sea válido. Si tienes
[`pbir-cli`](https://github.com/pbir-cli/pbir-cli):

```bash
pbir validate "lab/claves-huerfanas/ClavesHuerfanas.Report"
```

Los cuatro escenarios pasan como **Valid**. Mereció la pena comprobarlo: la primera versión
cargaba y refrescaba perfectamente en Power BI Desktop y aun así tenía **dos errores de
esquema** (`themeCollection` ausente en `report.json`, `$schema` ausente en
`definition.pbism`). Tolerado hoy no es lo mismo que correcto mañana.
