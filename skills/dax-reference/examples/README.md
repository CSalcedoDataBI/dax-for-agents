# examples — el contrato

Un fichero por función, con **al menos tres ejemplos**, y cada ejemplo trae **la consulta y el
número que devolvió el motor**.

Un *ejemplo* es exactamente eso: **una consulta con su resultado medido**. Es la unidad que
cuenta el gate y la que anuncia la ficha, así que una sección de prosa que enseñe dos
consultas cuenta como dos. La numeración `## 1.`, `## 2.` organiza la lectura, no el conteo.

Esto existe porque las fichas ya traen ejemplos —los de Microsoft, medidos sobre *Adventure
Works DW 2020*— y ese modelo no está en este repositorio. Sus cifras nadie de aquí las ha
ejecutado. Lo que se escribe en este árbol es lo contrario: **ejemplos que se ejecutan**.

## Dónde va cada cosa

```
dax-reference/examples/<primaryCategory>/<stem>.md
```

El `<stem>` es el mismo que el de la ficha en `generated/library/` — `if.md`, `if-eager.md`,
`bitlshift.md`. No es el nombre de la función: `IF.EAGER` vive en `if-eager.md`.

**Este árbol es escrito a mano y el sync nunca lo toca**, igual que `notes/`. Los ejemplos no
pueden vivir dentro de la ficha porque la ficha se regenera entera cada vez que `query-docs`
se mueve, y se los llevaría por delante.

## El fichero

```markdown
---
function: IF
model: ninguno
---

# IF — ejemplos

## 1. Sin el tercer argumento el resultado es BLANCO, no cero

Una frase que diga qué se está enseñando. No repitas la sintaxis: para eso está la ficha.

​```dax
EVALUATE ROW("sin_else", IF(1 = 2, "sí"))
​```

​```result
sin_else
(blank)
​```

Y debajo, si hace falta, por qué eso importa.
```

### El frontmatter

| clave | qué es |
|---|---|
| `function` | el nombre tal cual lo escribe DAX — `IF`, `IF.EAGER`, `BITLSHIFT` |
| `model` | contra qué escenario de `lab/` corre |

`model: ninguno` significa **no lee datos del modelo**: aritmética pura, texto, lógica. Se
ejecuta contra `contoso` porque hace falta un motor, no porque haga falta ese modelo. La
distinción importa para saber qué se rompe cuando un modelo cambia.

Cualquier otro valor tiene que ser un directorio real de `lab/`: `contoso`, `blancos`,
`claves-huerfanas`, `rendimiento`.

### El bloque `result`

Es lo que hace ejecutable al ejemplo. La primera línea son los nombres de columna; las
siguientes, las filas, con las celdas separadas por ` | `.

```
sin_else | con_else
(blank) | 0
```

| valor | se escribe |
|---|---|
| blanco | `(blank)` |
| verdadero / falso | `True` / `False` |
| número | tal cual, redondeado a **6 decimales** |
| texto | tal cual, sin comillas |

Si la consulta **aborta a propósito** —hay funciones que solo se entienden viendo el error—
el bloque lleva el mensaje:

```
ERROR: The value for column X cannot be determined
```

Cada bloque ` ```dax ` tiene que ir seguido de su ` ```result `. Un ejemplo sin resultado
medido no es un ejemplo: es una afirmación, y de esas ya viene el catálogo lleno.

## Cómo se comprueba

```bash
python scripts/check_examples.py                      # estructura: 3 por función, modelo real, todo con result
python lab/check_lab.py examples localhost:<puerto>   # ejecuta cada consulta y compara con su result
```

El primero corre en CI. El segundo **no**, y es deliberado: necesita un motor tabular con
datos y CI no tiene Power BI Desktop.

Para registrar el resultado de un ejemplo nuevo sin copiarlo a mano:

```bash
python lab/dump_examples.py localhost:<puerto> dax-reference/examples/logical/if.md
```

Escribe el bloque `result` de cada consulta que no lo tenga. Lo que escriba hay que
**mirarlo**: traslada lo que devolvió el motor, no decide si el ejemplo era buena idea.

## Qué es un buen ejemplo

Tres es el **suelo**, no el objetivo. `BITLSHIFT` con tres ya está servida; `CALCULATE` con
tres se queda corta.

- **Enseña algo que la sintaxis no dice.** Si el ejemplo se deduce leyendo la firma, sobra.
- **El número sorprende, o no hace falta el ejemplo.** El valor está en el caso donde la
  intuición falla.
- **Se lee entero de un vistazo.** Una consulta de cuarenta líneas no es un ejemplo.
- **No repite al de al lado.** Tres variantes del mismo caso son un ejemplo, no tres.
