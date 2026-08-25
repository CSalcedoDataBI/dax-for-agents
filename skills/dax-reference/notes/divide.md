## Trampa: `/` no protege, y el "0" que devuelves cambia el gráfico

`DIVIDE` devuelve **(en blanco)** al dividir por cero, no un error. Ese blanco es
deliberado: hace que la categoría desaparezca del visual en lugar de dibujar un cero que
nadie midió.

```dax
EVALUATE
ROW(
  "DIVIDE_1_0_es_blank", ISBLANK(DIVIDE(1,0)),
  "DIVIDE_1_0_alt0",     DIVIDE(1,0,0)
)
```

| expresión | resultado |
|---|---|
| `ISBLANK(DIVIDE(1,0))` | **TRUE** |
| `DIVIDE(1,0,0)` | 0 |

El tercer argumento es una decisión de negocio, no una medida de seguridad: pon `0` solo si
"no había divisor" y "el resultado fue cero" significan lo mismo para quien lee el informe.
Casi nunca lo significan.

## Lo que dice Microsoft, y no está en la ficha
Recomiendan `DIVIDE` frente a `IF(divisor = 0, BLANK(), a/b)` porque el `IF` evalúa el divisor
dos veces. Está en
[su página de buenas prácticas](https://learn.microsoft.com/en-us/dax/best-practices/dax-divide-function-operator),
no en la página de la función, que es por lo que existe esta nota.

Es una recomendación **suya**, citada, no una medición de este repo: sobre este modelo las
dos formas tardan lo mismo dentro del ruido.

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
