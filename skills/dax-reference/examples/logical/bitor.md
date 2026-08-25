---
function: BITOR
model: ninguno
---

# BITOR — ejemplos

## 1. Encender una bandera sin tocar las demás

Es el complemento de [`bitand`](./bitand.md): aquel pregunta, este pone. Y es idempotente —
encender dos veces la misma bandera deja el valor igual.

```dax
EVALUATE
VAR Permisos = 5
RETURN
ROW(
  "valor",           Permisos,
  "enciende_el_2",   BITOR(Permisos, 2),
  "enciende_el_1",   BITOR(Permisos, 1),
  "dos_veces_el_2",  BITOR(BITOR(Permisos, 2), 2)
)
```

```result
valor | enciende_el_2 | enciende_el_1 | dos_veces_el_2
5 | 7 | 5 | 7
```

`enciende_el_1` devuelve 5 otra vez porque el bit ya estaba puesto. Sumar no valdría: `5 + 1`
daría 6 y habría corrompido la máscara.

## 2. Por eso no se hace con una suma

La diferencia solo aparece cuando la bandera ya estaba encendida — es decir, en producción y
no en la prueba.

```dax
EVALUATE
VAR Permisos = 5
RETURN
ROW(
  "bitor_con_4",  BITOR(Permisos, 4),
  "suma_con_4",   Permisos + 4,
  "bitor_con_2",  BITOR(Permisos, 2),
  "suma_con_2",   Permisos + 2
)
```

```result
bitor_con_4 | suma_con_4 | bitor_con_2 | suma_con_2
5 | 9 | 7 | 7
```

Con el bit 2 (que faltaba) los dos coinciden. Con el bit 4 (que ya estaba) no.

## 3. Con negativos, un solo cero manda

`-1` tiene todos los bits a uno, así que absorbe cualquier `BITOR`.

```dax
EVALUATE
ROW(
  "con_menos_uno",  BITOR(5, -1),
  "menos_dos_y_1",  BITOR(-2, 1),
  "cero_y_cero",    BITOR(0, 0),
  "decimal",        BITOR(5.9, 2.9)
)
```

```result
con_menos_uno | menos_dos_y_1 | cero_y_cero | decimal
-1 | -1 | 0 | 7
```
