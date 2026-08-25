# Diseño — biblioteca de ejemplos ejecutables (3 por función, 479 funciones)

Fecha: 2026-08-17. Estado: **diseño aprobado, sin implementar**.

## El problema, dicho con precisión

No es que falten ejemplos. **Las 479 fichas ya traen un `## Examples`** — el de Microsoft, que
viene con el `.md` de `query-docs` y se publica tal cual. `calculate.md` publica esto:

| Category | Sales Amount | Blue Revenue |
|---|---|---|
| Bikes | $94,620,526.21 | $8,374,313.88 |
| **Total** | **$109,809,274.20** | **$9,602,850.97** |

Esas cifras salen de **Adventure Works DW 2020**. Ese modelo no está en este repo, nadie de
aquí ha ejecutado esas consultas, y no hay forma de saber si siguen dando eso.

Es exactamente la enfermedad que se acaba de curar en las notas de campo —una cifra citada que
el lector no puede reproducir— multiplicada por 479. La diferencia es que las notas eran 30 y
las escribimos nosotros; esto viene de fuera y es todo el catálogo.

**El objetivo no es añadir ejemplos. Es que cada ejemplo se ejecute y su número salga del
motor.** Ninguna otra referencia de DAX publica la consulta, el modelo y el número juntos. Ahí
es donde esta biblioteca deja de ser una copia de la documentación.

## Decisión 1 — el eje de los modelos es la FORMA DE LOS DATOS, no la categoría

La propuesta inicial era una copia del modelo por grupo de funciones (escalares, tabla…). Se
descarta, y por una razón medida, no estética.

Lo que obliga a un modelo nuevo no es a qué categoría pertenece una función: es que necesite
una **forma de datos que Contoso no tiene**. Dieciséis copias de Contoso (una por categoría)
son dieciséis modelos casi idénticos: sesenta y cuatro ficheros TMDL más que mantener,
dieciséis refrescos, y **cero cobertura añadida**.

Y el cuello de botella real no es el disco —el TMDL pesa kilobytes— sino **las instancias de
Power BI Desktop**: verificar exige abrir y refrescar cada modelo. Cuantos menos modelos,
antes se verifica todo el catálogo.

El repo ya tomó esta decisión una vez y salió bien: `claves-huerfanas`, `blancos` y
`rendimiento` existen por **forma** (integridad rota, blancos, volumen), no por categoría.

### Los modelos

| modelo | forma que aporta | desbloquea |
|---|---|---|
| `contoso` ✅ | star schema, fechas, texto, números, divisa | la mayor parte de lo relacional |
| `claves-huerfanas` ✅ | integridad referencial rota | fila en blanco, `ALLNOBLANKROW` |
| `blancos` ✅ | blancos en columnas numéricas | `AVERAGE`/`AVERAGEX` y familia |
| `rendimiento` ✅ | dos millones de filas | coste, transición de contexto |
| **`relaciones`** | relación **inactiva**, muchos-a-muchos, bidireccional | `USERELATIONSHIP`, `CROSSFILTER` — las 4 de `relationship` |
| **`jerarquia`** | padre-hijo | las 5 de `parent-and-child` (`PATH`, `PATHITEM`, `PATHLENGTH`…) |
| **`seguridad`** | RLS y grupos de cálculo | `USERNAME`, `USERPRINCIPALNAME`, `USEROBJECTID`, `SELECTEDMEASURE*` |

Siete, no dieciséis. Cada uno nuevo se justifica por funciones que **hoy es imposible
demostrar** — la misma regla que produjo los tres primeros. `relaciones` además cierra el
hueco ya conocido y anotado en su momento: «`USERELATIONSHIP` no tiene nota».

## Decisión 2 — un tercio del catálogo no necesita modelo

De las 479 funciones, **331 devuelven escalar**. Y cuatro categorías enteras son matemáticas
puras: no leen datos del modelo.

| categoría | funciones | ejemplo |
|---|---:|---|
| `financial` | 51 | `PMT`, `XIRR`, `XNPV` |
| `math-and-trig` | 49 | `ROUND`, `POWER`, `MOD` |
| `text` | 21 | `SUBSTITUTE`, `FORMAT`, `LEFT` |
| `logical` | 15 | `IF`, `SWITCH`, `COALESCE` |
| **total** | **136** | **408 ejemplos** |

```dax
EVALUATE ROW("cuota", PMT(0.05/12, 60, 10000))
```

Eso corre contra **cualquier** modelo. Son 136 funciones —el 28% del catálogo— verificables
sin construir nada. Por ahí se empieza: es la mitad del trabajo con un décimo del riesgo, y
rueda la maquinaria antes de tocar lo relacional.

## Decisión 3 — los ejemplos no pueden vivir dentro de la ficha

Restricción dura: **las fichas son generadas** y el sync las reescribe entera cada vez que
`query-docs` se mueve. Un ejemplo escrito a mano dentro de una ficha se pierde en el siguiente
sync.

El repo ya resolvió esto con `notes/`: un árbol paralelo escrito a mano, que la ficha enlaza
por frontmatter (`notes: true`). Los ejemplos siguen el mismo patrón.

```
dax-reference/examples/
  INDEX.md
  <primaryCategory>/
    <funcion>.md
```

Cada fichero declara en frontmatter contra qué modelo corre:

```markdown
---
function: PMT
model: ninguno          # ninguno | contoso | relaciones | jerarquia | seguridad | ...
---
```

`model: ninguno` significa «no lee datos»: se ejecuta contra `contoso` porque hace falta un
motor, no porque haga falta ese modelo. La distinción importa para saber qué se rompe si un
modelo cambia.

## Decisión 4 — los ejemplos de Microsoft se quedan, marcados

Son CC BY 4.0 legítimos y aportan contexto que nosotros no vamos a reescribir. Pero llevan
cifras de un modelo que no está aquí, así que:

1. **Nuestros ejemplos van primero** en la ficha. El agente lee lo ejecutable antes que lo
   citado.
2. El `## Examples` de Microsoft queda **debajo y con un aviso** de que su modelo (Adventure
   Works DW 2020) no está en este repositorio y sus cifras no se han verificado aquí.

Es el mismo criterio que el resto del repo: no se borra lo que otro afirma, se dice de dónde
sale y qué se ha comprobado.

## Cómo se vuelve real: el gate

Sin esto, «3 ejemplos por función» es una cifra en prosa que se pudre — contra lo que este
repo lleva peleando desde el principio.

`scripts/check_examples.py` falla si:

- una función tiene **menos de 3** ejemplos;
- un ejemplo nombra un `model:` que no existe en `lab/`;
- un ejemplo no trae **resultado medido**;
- un ejemplo referencia una función que no está en el catálogo.

Y el runner que ya existe (`lab/check_lab.py`, construido para las notas) se extiende de 30
notas a los ejemplos: **lee la consulta del propio `.md`**, no de una copia, así que editar un
ejemplo cambia lo que se ejecuta.

### Lo que el gate NO puede comprobar

Que un ejemplo sea **útil**. Tres ejemplos de `BITLSHIFT` es relleno y tres de `CALCULATE` es
poco. El 3 es un **suelo**, no un objetivo: las funciones de más tráfico crecen por encima. Eso
lo decide quien escribe, y no hay checker que lo sustituya.

## Fases

| fase | qué | funciones | ejemplos |
|---|---|---:|---:|
| **0** | la maquinaria: estructura, frontmatter, runner, gate — sobre **una** categoría piloto | ~15 | ~45 |
| **1** | escalares puros: `financial`, `math-and-trig`, `text`, `logical` | 136 | 408 |
| **2** | sobre `contoso`: filtro, agregación, tiempo, tabla, estadística, fecha, información | ~207 | ~621 |
| **3** | los tres modelos nuevos: `relaciones`, `jerarquia`, `seguridad` | ~90 | ~270 |
| | **total** | **479** | **1.437** |

Una PR por categoría, no una por fase: 15 PRs revisables en vez de 4 imposibles de revisar.

## Riesgos, dichos antes de empezar

- **1.437 ejemplos escritos por un agente pueden ser plausibles y falsos.** La única defensa es
  que cada uno se ejecute y su resultado se registre desde el motor. Un ejemplo que no corre no
  entra.
- **16 funciones no tienen categoría** en el catálogo, así que no tienen carpeta donde caer. Hay
  que resolverlo en la fase 0, no descubrirlo en la 2.
- **El laboratorio no corre en CI** y esto no lo cambia: sigue haciendo falta Power BI Desktop.
  El gate de estructura sí corre en CI; la ejecución es local.
- **Volumen de revisión.** 1.437 ejemplos no se revisan a ojo. El gate y el runner son lo que
  hace la revisión posible; sin ellos esto es un montón de markdown sin respaldo.
