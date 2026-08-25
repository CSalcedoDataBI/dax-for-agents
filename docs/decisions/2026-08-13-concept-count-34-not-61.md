# Las páginas conceptuales son 34, no 61

**Fecha:** 2026-08-13 · **Estado:** aceptada · **Afecta a:** el spec de diseño y la épica de la biblioteca

## El problema

El [spec de diseño](../superpowers/specs/2026-08-06-dax-for-agents-design.md) y los
entregables del épico dicen **61 páginas conceptuales**. El árbol generado tiene **34**, y
nada en el repo reconciliaba las dos cifras. Quien leyera el spec contra el artefacto
encontraba 27 páginas de diferencia y ninguna explicación.

## De dónde salía el 61

De restar. El estudio previo contó **540 ficheros `.md`** en el árbol DAX de `query-docs` y
**479 funciones**, y llamó "conceptuales" a la diferencia:

```
540 − 479 = 61
```

Medido sobre `query-docs@c6a9a72`, esos 540 se reparten así:

| dónde | cuántos | qué son | ¿ficha de concepto? |
|---|---|---|---|
| raíz | 479 | `*-function-dax.md`, una por función | no, son fichas de función |
| raíz | 15 | `*-functions-dax.md`, índices de categoría | **no** — alimentan `catalog.md` |
| raíz | 23 | glosario, operadores, `EVALUATE`, `DEFINE`, `VAR`… | **sí** |
| `best-practices/` | 11 | guías de Microsoft | **sí** |
| `includes/` | 12 | fragmentos compartidos (`[!INCLUDE]`) | **no** — no son páginas |
| | **540** | | **34** |

`23 + 11 + 15 + 12 = 61`. El 61 nunca fueron 61 páginas conceptuales: era **todo lo que no
es una función**, con los índices de categoría y los includes dentro.

Los includes son la parte más clara: son los fragmentos que el propio sync lee para resolver
`appliesTo` y el flag de desaconsejada. No son documentos, son piezas de otros documentos.
Convertirlos en fichas habría producido 12 páginas que solo dicen "esta función se aplica
a…".

## La decisión

**34 es la cifra correcta**, y es la que sale del descubrimiento real. La regla tiene dos
partes, y hay que decir las dos: *en la raíz y en `best-practices/`* —las dos carpetas de
`CONCEPT_DIRS`— *todo `.md` que no sea una ficha de función ni un índice de categoría*.

Sin la primera mitad la cuenta no sale: `includes/` tiene 12 `.md`, y bajar a él daría **46**
en vez de 34. Por eso el sync no recorre el árbol entero, sino dos carpetas nombradas.

`media/` y `breadcrumb/` están excluidos por nombre junto a `includes/` aunque hoy no
contengan ni un markdown —12 imágenes y un `toc.yml`—, y la propia aritmética de aquí abajo lo
demuestra: 517 + 11 + 12 = 540, el total. Se nombran igualmente para que un `.md` que
aparezca ahí mañana no se convierta en ficha por accidente. Y cuando aparece una carpeta con
markdown que **nadie** está leyendo, el sync avisa en vez de ignorarla en silencio.

Esa regla es mecánica, así que una página nueva de Microsoft en cualquiera de las dos entra
sola en el siguiente sync — que es justo lo que un número fijo en un spec no puede hacer.

El spec queda corregido con una nota, no reescrito: el 61 formó parte del razonamiento que
justificó el proyecto y borrarlo escondería que la estimación estaba mal.

## Cómo se comprueba

```bash
D=<checkout>/query-languages/dax
ls $D/*.md | wc -l                       # 517 en la raíz
ls $D/*-function-dax.md | wc -l          # 479
ls $D/*-functions-dax.md | wc -l         # 15
ls $D/best-practices/*.md | wc -l        # 11
ls $D/includes/*.md | wc -l              # 12
find $D -name '*.md' | wc -l             # 540
```

517 − 479 − 15 = 23 en la raíz, más 11 de `best-practices/`, son las 34 que publica
`generated/concepts/`.
