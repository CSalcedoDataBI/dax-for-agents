# Skills — índice y routing

Cinco skills, una sola idea: **el lenguaje DAX**. Nada de modelado, visuales ni operaciones —
para eso hay otros repos mejores, enlazados en el [README](README.md).

---

## Routing

```
Pregunta sobre DAX
  ├─ ¿qué hace esta función? ¿cuál uso?  → dax-reference
  ├─ ¿ya existe un UDF para esto?        → dax-lib
  ├─ ese UDF ya existe: instálalo        → dax-lib-install
  ├─ voy a escribir un UDF               → dax-udf-authoring
  └─ rolling / running total / ranking   → dax-window-functions

¿Rendimiento? → no está aquí. Usa el plugin de data-goblin (ver README).
```

## Catálogo

| Skill | Cuándo usarla | Estado |
|---|---|---|
| **`dax-reference`** | Referencia del lenguaje: qué hace una función, su firma, en qué contexto aplica, si está desaconsejada, y las trampas que los docs no cuentan. **479 fichas + 34 páginas conceptuales** (contexto de evaluación, sentencias de consulta, operadores, glosario, buenas prácticas) derivadas de `MicrosoftDocs/query-docs`, y **31 notas de campo** medidas contra un modelo real. | ✅ |
| **`dax-lib`** | Índice del catálogo de [daxlib.org](https://daxlib.org): qué existe, quién lo escribió y dónde obtenerlo. **Búscala antes de escribir un UDF.** No redistribuye el código. | ✅ |
| **`dax-lib-install`** | Trae de verdad el código de un UDF que `dax-lib` ya encontró: lo instala contra el modelo, lo prueba con una consulta real, y lo deja atribuido (autor, licencia, URL) en el propio `FUNCTION`. | ✅ |
| **`dax-udf-authoring`** | Mecánica de un `FUNCTION` correcto: tipos de parámetro, `VAL` vs `EXPR`, `TABLEOF`/`NAMEOF`, parámetros opcionales, límites GA y bugs del parser. | ✅ |
| **`dax-window-functions`** | `WINDOW` / `OFFSET` / `INDEX` / `RANK` / `ROWNUMBER` / `MOVINGAVERAGE` / `RUNNINGSUM`. ABS vs REL, `MATCHBY`, gotcha del relation por defecto. | ✅ |

## Convenciones

Toda skill sigue el estándar de [agentskills.io](https://agentskills.io/specification):

1. **Una skill = una carpeta bajo `skills/`** con `SKILL.md`. Apoyo en `scripts/`,
   `references/`, `evals/` dentro de la propia carpeta.
2. **Frontmatter YAML** con `name` (kebab-case, idéntico a la carpeta) y `description` (tercera
   persona, empieza con **"Use when …"**, describe *cuándo* usarla).
3. **Token-eficiente:** el `SKILL.md` es conciso; el detalle pesado vive en archivos aparte que
   el agente lee solo cuando los necesita.
4. **Cross-links por nombre** (`` `dax-lib` ``), no por ruta.
5. **El prefijo `dax-` se conserva** aunque el plugin ya se llame `dax` y aunque `skills/`
   ya dé contexto. Renombrar a `skills/reference/` tocaría los cross-links de las cinco
   `SKILL.md`, `evals/cases.yaml` y cualquier referencia ya instalada; el prefijo cuesta
   cuatro caracteres y no se paga solo. Instaladas quedan `dax:dax-reference`,
   `dax:dax-lib`, `dax:dax-lib-install`, `dax:dax-udf-authoring` y `dax:dax-window-functions`.
6. **Las cinco skills van listadas por ruta en `.claude-plugin/plugin.json`.** Bajo `skills/`
   el escaneo por defecto ya las encontraría, así que la lista dejó de ser la diferencia
   entre cinco skills y ninguna — pero sigue siendo lo que hace revisable en un diff el
   conjunto que se publica. Lo comprueba CI.
7. **El layout es el de [`microsoft/skills-for-fabric`](https://github.com/microsoft/skills-for-fabric):**
   `skills/` como fuente única y el manifiesto del plugin en la raíz. Es también lo que
   deja añadir un segundo plugin más adelante sin duplicar ninguna skill.
