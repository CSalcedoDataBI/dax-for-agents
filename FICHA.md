# Ficha — dax-for-agents

> Ficha de esta herramienta. La lee su experto (`.claude/agents/experto.md`) en cada PR.
> Se mantiene con las reglas internas del mantenedor.
> La aprueba el mantenedor (línea `Aprobada:`); cambiarla exige una nueva aprobación.

## Qué es

- **Qué construye y para quién:** un plugin de Claude Code que lleva el **lenguaje DAX** a un
  agente — 479 fichas de función, 34 páginas conceptuales, notas de campo escritas a mano, el
  catálogo de [daxlib.org](https://daxlib.org), autoría de UDF y la familia `WINDOW`. Seis skills,
  cinco sobre el lenguaje y una para reportar cuando se equivocan.
- **Papel** (`repo-roles`): tool (plugin del directorio de Anthropic).
- **Gemelo público/privado:** `dax-for-agents-pro` (privado).

## Norte

- **Plan vigente:** [#47 — dax-for-agents — Roadmap](https://github.com/users/CSalcedoDataBI/projects/47)
  (épica abierta: [#6 — runnable examples library](https://github.com/CSalcedoDataBI/dax-for-agents/issues/6)).
- **Lo que esta herramienta NO es:** no es ajuste de rendimiento (para eso, el plugin de
  data-goblin que enlaza el README), no es modelado, no son visuales, no son operaciones. No
  redistribuye el código de los paquetes de daxlib: solo los indexa.

## Zonas protegidas

Lo que no se toca sin un paso del plan que lo nombre:

- **Rama `stable` y `.claude-plugin/plugin.json` en la raíz** — el directorio de Anthropic rastrea
  `stable` y busca el manifiesto en la raíz; moverlo o tocar `stable` fuera de un release rompe la
  revisión del directorio. Ver los PR #24/#26 (no se fusionan hasta que Anthropic responda sobre la
  ruta del manifiesto).
- **El conjunto publicado de skills, el prefijo `dax-` y el enlace cruzado por nombre** — renombrar
  una skill o un cross-link rompe las referencias ya instaladas (INDEX.md, convención 5). El
  manifiesto debe listar exactamente las skills en disco: lo verifica `check_plugin_manifest.py`.
- **El contrato de las compuertas de CI y la lista «Checking it yourself» del README** —
  `check_documented_gates.py` exige que el README enumere cada check que CI corre; `check_examples`,
  `check_eval_claims`, `check_doc_claims` y `refresh_local_metadata.py --check` cuidan que las
  afirmaciones del repo coincidan con el árbol. Quitar una compuerta sin ajustar su prosa falla CI.

## Capa y feedback

- **Capa de nodo** (ADR 0023): `dax` (pendiente de declarar `node.json`: issue
  [#34](https://github.com/CSalcedoDataBI/dax-for-agents/issues/34)).
- **Skill de feedback:** `dax-for-agents:dax-feedback` (reporta de vuelta una ficha, nota o ejemplo
  equivocado como un issue público saneado en este mismo repo).

## Check y experto

- **Check de CI requerido:** `validate` y `static` (ambos en el ruleset de `main`).
- **Suite de pruebas:** `validate` (workflow *Validate skills* → `scripts/validate_skills.py`, las
  compuertas de `scripts/` y `python -m unittest discover` sobre `skills/dax-reference/scripts`,
  `scripts` y `evals`) y `static` (workflow *Evals* → `python evals/run_evals.py`).
- **Runner:** GitHub (repo público — minutos gratis, R8; no hay runner local).
- **Formato de tag:** `vX.Y.Z` (un solo componente; gestionado por `release-please`).
- **Experto:** `.claude/agents/experto.md`
- **¿Plugin del directorio?:** sí — `stable` no se toca y fusionar en `main` no es publicar;
  publicar sigue R5 (skill `plugin-directory-submit` y OK de Cristóbal).
- **Partes visibles que aprueba Cristóbal:** ninguna pieza desplegada; el README y los informes de
  `lab/` se regeneran del árbol y CI los verifica (no se aprueban mirándolos).

## Aprobación

Aprobada: 2026-10-23
