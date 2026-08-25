# Las 16 funciones sin categoría van a `sin-categoria/`

Fecha: 2026-08-17. Contexto: fase 0 de la biblioteca de ejemplos.

## El hecho

De las 479 funciones del catálogo, **16 no tienen `primaryCategory`**:

```
ALLSELECTEDAPPLY  ALLSELECTEDREMOVE  ALWAYSAPPLY  COLLAPSE  COLLAPSEALL
DEPENDON  EXPAND  EXPANDALL  FILTERCLUSTER  GROUPCROSSAPPLY
GROUPCROSSAPPLYTABLE  ISATLEVEL  NONFILTER  SAMPLEAXISWITHLOCALMINMAX
SHADOWCLUSTER  TOPNSKIP
```

No es un fallo del sync. El sync ya intenta **cuatro vías** para resolver la categoría
(índice de categoría, prosa, `overrides.json`, `toc.yml`) y estas dieciséis no aparecen en
ninguna: `query-docs` documenta sus páginas pero no las lista en ningún índice de categoría.
Son funciones de cálculo visual y funciones internas que el cliente genera, no cosas que se
escriban a mano en una medida.

## Por qué había que decidirlo ahora

Los ejemplos viven en `dax-reference/examples/<primaryCategory>/<stem>.md`. Sin categoría no
hay carpeta, así que estas dieciséis no tienen sitio donde caer. Descubrirlo en la fase 2,
con doscientos ficheros ya escritos, sería peor.

## La decisión

Van a **`dax-reference/examples/sin-categoria/`**.

Se descartaron dos alternativas:

- **Inventarles una categoría** (`visual-calculation`, `internal`). Sería una afirmación
  nuestra disfrazada de dato de Microsoft, y este repo distingue esas dos cosas en todas
  partes. Si upstream las categoriza algún día, el sync lo recogerá solo.
- **Dejarlas fuera del árbol de ejemplos.** Rompe la promesa de «3 ejemplos por función» sin
  decirlo. Un hueco silencioso es justo lo que los gates existen para impedir.

`sin-categoria` es feo a propósito: se lee como lo que es, un cajón para lo que upstream no
clasifica, y no como una categoría de verdad.

## Consecuencia

Cuando llegue su turno, estas dieciséis se escriben igual que las demás — y varias de ellas
solo se pueden demostrar dentro de un cálculo visual, así que probablemente necesiten su
propio escenario de laboratorio. Eso se decide entonces, no ahora.
