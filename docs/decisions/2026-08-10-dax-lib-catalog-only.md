# `dax-lib`: catálogo, no espejo. Y cómo construir biblioteca propia sin derivar de nadie

**Fecha:** 2026-08-10
**Estado:** decidido por el owner
**Afecta a:** issues #9, #18 · PR #16

---

## La decisión

`dax-lib` en el repo público **indexa** el catálogo de [daxlib.org](https://daxlib.org) y
**no redistribuye** el código TMDL de terceros. El agente aprende qué existe y a dónde ir; el
código se obtiene de la fuente.

Se descarta el espejo completo (55 paquetes, 116 versiones, 232 archivos, ~90.000 líneas de
40 autores) que se había construido en la PR #16.

## Los hechos que llevaron a ella

Verificado el 2026-08-10 contra `daxlib/daxlib@9a1c2cc`:

| | |
|---|---|
| Licencia del repo origen | **MIT**, `Copyright (c) 2025 SQLBI` (vía REST; el campo GraphQL devuelve null) |
| Paquetes / autores | 55 paquetes, 116 versiones, 1.649 funciones, **40 autores distintos** |
| Licencia por paquete | **No existe.** El schema del manifiesto no tiene campo `license`, ni opcional |
| Política de contribución | **No hay.** Sin `CONTRIBUTING.md`, sin CLA, sin DCO |

## Por qué, si MIT permite espejar

**Espejar era legal.** MIT autoriza copiar, modificar y redistribuir; la única obligación es
conservar el aviso de copyright — que el espejo original no incluía, y eso sí era un
incumplimiento real, no una zona gris.

Se descarta por tres razones que no son legales:

1. **Envejece mal.** Es una foto congelada de un registro vivo. El espejo era del 2026-05-28;
   para cuando se detectó ya llevaba dos meses y medio de retraso, con el repo aún sin
   publicar.
2. **Superficie de redistribución ajena.** 90.000 líneas de 40 autores dentro de un repo que
   se presenta como referencia del lenguaje. Cualquier problema de licencia, contenido o
   atribución de cualquiera de esos 40 pasa a ser problema nuestro.
3. **Posicionamiento.** El valor de la skill es *"búscala antes de escribirla"*. Para eso
   basta el índice. Cargar el código convierte el repo en un segundo registro, y ese ya
   existe y es de otros.

## El aprendizaje: qué se puede documentar y qué no

La pregunta de fondo era si el conocimiento de daxlib sirve para construir biblioteca propia
sin infringir. Sí, y el límite es nítido.

**El copyright protege la expresión, no las ideas.** Está protegido el texto concreto de una
función. **No** están protegidos:

- que exista una función que resuelve un problema, y cuál es ese problema
- la técnica (`WINDOW` rinde más que `TOPN + CALCULATETABLE` para un moving average)
- el algoritmo, el patrón de parámetros, la trampa de rendimiento
- el hecho de que un paquete existe, quién lo firma y qué hace

Todo eso es **conocimiento** y documentarlo es libre. Se puede escribir "estas son las
familias de UDF que la comunidad construyó y estos los problemas que atacan" sin tocar una
línea ajena.

**Para que una biblioteca propia sea propia**, se escribe desde el *problema*, no desde el
código de otro. Con MIT no hace falta sala limpia ni ceremonia: si derivas, arrastras su
copyright y quedas como obra derivada con atribución permanente; si escribes tu solución, el
copyright es tuyo y lo licencias como quieras.

## Lo que este repo publica, y por qué cada capa es segura

| Capa | Qué es | Base legal |
|---|---|---|
| Referencia del lenguaje | 479 fichas desde `MicrosoftDocs/query-docs` | CC BY 4.0, atribuido en `dax-reference/NOTICE` |
| Índice de daxlib | Nombres, autores, descripciones, enlaces | Hechos y enlaces; atribución en `dax-lib/NOTICE` |
| Notas de campo | Trampas, costes, "usa aquello en vez de esto" | Obra propia — y el diferenciador del repo |
| Criterio de cuándo un UDF se justifica | El criterio, no el código | Obra propia, nacida de medir en producción |
| UDFs propios | Escritos desde el problema | Obra propia |

## Recomendación abierta (no decidida)

**No construir un registro que compita con daxlib.** 55 paquetes, 40 autores, SQLBI detrás y
el dominio. Un segundo registro fragmenta el ecosistema.

Lo contrario rinde más: **publicar los UDFs propios *en* daxlib**, con namespace propio, junto
a SQLBI y Kurt Buhler. Distribución gratis, cero infraestructura, y posiciona como parte del
ecosistema en vez de como quien hizo su propia versión.

Materia prima ya existente en el repo privado: `dax-fp-udf-patterns`. Hoy atado al contexto
de un cliente, pero el patrón (rolling/trailing sobre un eje arbitrario, double-REMOVEFILTERS,
evitar dependencia circular) es generalizable y publicable una vez desatado.

## Consecuencias

- La PR #16 se reduce a catálogo + `NOTICE` + evals. Se eliminan `dax-lib/library/` y el
  script de espejo, o el script se reorienta a regenerar solo el catálogo.
- `dax-lib/SKILL.md` deja de prometer TMDL instalable local y pasa a enrutar a daxlib.org.
- Sigue pendiente por #18: quitar de `dax-lib/SKILL.md` la recomendación dirigida a una medida
  concreta de un modelo de cliente. La guarda `scripts/check_no_client_leaks.py` la detecta.
