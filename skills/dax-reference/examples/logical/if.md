---
function: IF
model: ninguno
---

# IF — ejemplos

## 1. Sin el tercer argumento el resultado es BLANCO, no cero

Omitir el `else` no significa «cero». Significa **blanco**, que es otra cosa: no aparece en el
visual, no cuenta en un `COUNT`, y en cuanto alguien le suma cero deja de ser blanco.

```dax
EVALUATE
ROW(
  "sin_else",        IF(1 = 2, 10),
  "es_blanco",       ISBLANK(IF(1 = 2, 10)),
  "sin_else_mas_0",  IF(1 = 2, 10) + 0,
  "con_else_cero",   IF(1 = 2, 10, 0)
)
```

```result
sin_else | es_blanco | sin_else_mas_0 | con_else_cero
(blank) | True | 0 | 0
```

`sin_else + 0` y `con_else_cero` dan lo mismo — y esa es justo la confusión. El primero
convierte un blanco en cero sin decirlo; el segundo lo decide.

## 2. Una condición en blanco es FALSA

`IF` no distingue entre «falso» y «no hay dato». Un blanco entra por la rama del `else` sin
avisar, así que una columna con huecos se clasifica entera como si fuese `FALSE`.

```dax
EVALUATE
ROW(
  "condicion_blanca", IF(BLANK(), "rama SI", "rama NO"),
  "condicion_cero",   IF(0, "rama SI", "rama NO"),
  "condicion_uno",    IF(1, "rama SI", "rama NO"),
  "cero_es_falso",    BLANK() = FALSE()
)
```

```result
condicion_blanca | condicion_cero | condicion_uno | cero_es_falso
rama NO | rama NO | rama SI | True
```

El cero también es falso, y por la misma razón: `IF` convierte a booleano, y en DAX el cero y
el blanco se convierten los dos en `FALSE`.

## 3. Las dos ramas no tienen por qué devolver el mismo tipo

`IF` puede devolver texto por una rama y número por la otra. Lo que sale es un valor de tipo
variante, y quien lo consuma después —una comparación, un `SUM`, un formato— es quien se
lleva la sorpresa.

```dax
EVALUATE
ROW(
  "rama_numero", IF(1 = 1, 42, "cuarenta y dos"),
  "rama_texto",  IF(1 = 2, 42, "cuarenta y dos"),
  "suma_mixta",  IF(1 = 1, 42, "x") + 1
)
```

```result
rama_numero | rama_texto | suma_mixta
42 | cuarenta y dos | 43
```

Ver [`coalesce`](./coalesce.md) para el caso concreto de «si está en blanco, usa este otro»,
que es donde casi siempre se acaba usando un `IF` de más.
