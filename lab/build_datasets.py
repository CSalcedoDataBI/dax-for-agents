"""Genera los parquet de los tres escenarios sinteticos del laboratorio.

Los cuatro modelos de `lab/` leen sus filas de parquet publicados en el repo PUBLICO
`CSalcedoDataBI/SampleDataSets`, por `raw.githubusercontent.com` y sin autenticacion. Este
script es el que produce los de `blancos`, `claves-huerfanas` y `rendimiento`; los de
`contoso-retail` vienen de otro sitio y no se tocan aqui.

Existe para que los ficheros publicados no sean un binario opaco: quien quiera comprobar que
el parquet dice lo que el README dice, lo regenera y compara. La generacion es DETERMINISTA
--sin aleatoriedad, sin fechas-- asi que dos ejecuciones dan el mismo contenido.

    python lab/build_datasets.py <directorio-destino>
    python lab/build_datasets.py ../SampleDataSets/dax-lab

Despues hay que commitear y empujar el destino a mano: este script escribe ficheros, no
publica nada.
"""

from __future__ import annotations

import os
import sys

import pyarrow as pa
import pyarrow.parquet as pq

# Los tres escenarios en un solo sitio, para que el fichero se pueda leer como la
# especificacion de los datos y no haya que abrir tres TMDL para saber que hay dentro.
FILAS_RENDIMIENTO = 2_000_000
PASO = 7919  # primo: reparte Importe sobre 1..1000 sin dejar un orden que el motor aproveche
CATEGORIAS = 20


def blancos() -> dict[str, pa.Table]:
    """Cinco tiendas; DOS con los metros en blanco. 100+200+300=600: entre 3 son 200,
    entre 5 son 120. Los numeros estan elegidos para que se distinga de un vistazo cual
    de los dos denominadores uso una media."""
    return {
        "Tiendas": pa.table(
            {
                "TiendaKey": pa.array([1, 2, 3, 4, 5], pa.int64()),
                "Nombre": pa.array(["Centro", "Norte", "Sur", "Este", "Oeste"], pa.string()),
                "Metros": pa.array([100, 200, 300, None, None], pa.int64()),
            }
        )
    }


def claves_huerfanas() -> dict[str, pa.Table]:
    """Tres productos (1, 2, 3) y cuatro ventas, la ultima contra el producto 99, QUE NO
    EXISTE. Esa sola fila es todo el escenario."""
    return {
        "DimProducto": pa.table(
            {
                "ProductoKey": pa.array([1, 2, 3], pa.int64()),
                "Nombre": pa.array(["Alfa", "Beta", "Gamma"], pa.string()),
            }
        ),
        "Ventas": pa.table(
            {
                "ProductoKey": pa.array([1, 2, 3, 99], pa.int64()),
                "Unidades": pa.array([10, 20, 30, 50], pa.int64()),
            }
        ),
    }


def rendimiento() -> dict[str, pa.Table]:
    """Dos millones de filas. Es el unico escenario donde el volumen ES el punto: sin el,
    un plan malo y uno bueno cuestan lo mismo y la comparacion no dice nada."""
    indices = range(1, FILAS_RENDIMIENTO + 1)
    return {
        "Ventas": pa.table(
            {
                "VentaKey": pa.array(indices, pa.int64()),
                "Importe": pa.array([(i * PASO) % 1000 + 1 for i in indices], pa.int64()),
                "CategoriaKey": pa.array([i % CATEGORIAS + 1 for i in indices], pa.int64()),
            }
        ),
        # Las medianas que publica el README de rendimiento, medidas en frio el 2026-08-12 con
        # ClearCache antes de cada corrida y tres corridas por medida. Estan aqui para que la
        # pagina las grafique desde un DATO versionado en vez de un cuadro de texto que nadie
        # puede auditar.
        #
        # CUATRO filas y no nueve: el grupo A se cronometro con las SEIS medidas juntas, y
        # repartir esos 5 ms entre seis filas serian seis numeros que nadie midio.
        "Tiempos": pa.table(
            {
                "Caso": pa.array([
                    "Grupo A - las seis juntas",
                    "SUMX(Ventas, [Total])",
                    "SUMX(Ventas, Ventas[Importe])",
                    "CALCULATE([Total], FILTER(ALL(Ventas), [Total] > 900))",
                ], pa.string()),
                "Grupo": pa.array(["A", "B", "B", "B"], pa.string()),
                "MedianaMs": pa.array([5, 871, 3, 873], pa.int64()),
                "PicoMemoriaKB": pa.array([1027, 197300, 0, 197342], pa.int64()),
                "ConsultasSE": pa.array([3, 2, 1, 2], pa.int64()),
            }
        ),
    }


# VentaKey son 2.000.000 de valores distintos y consecutivos: el diccionario no le sirve de
# nada y con snappy a secas el fichero pesa 8,9 MB, cuatro veces el Contoso entero. Codificada
# como diferencias baja a 385 KB --23 veces menos-- porque la diferencia entre una fila y la
# siguiente es siempre 1. La columna NO se puede quitar en su lugar: los tiempos publicados en
# el README de `rendimiento` se midieron con ella, y un modelo sin ella seria otro modelo.
#
# La clave es (escenario, TABLA) y no solo el escenario: estas opciones nombran columnas
# concretas, y aplicarselas a una tabla que no las tiene --Tiempos, sin ir mas lejos-- hace
# fallar la escritura. Se descubrio al anadir la segunda tabla al escenario.
CODIFICACION = {
    ("rendimiento", "Ventas"): dict(
        column_encoding={"VentaKey": "DELTA_BINARY_PACKED"},
        use_dictionary=["Importe", "CategoriaKey"],
    )
}


ESCENARIOS = {
    "blancos": blancos,
    "claves-huerfanas": claves_huerfanas,
    "rendimiento": rendimiento,
}


def main(destino: str) -> int:
    for escenario, construir in ESCENARIOS.items():
        carpeta = os.path.join(destino, escenario)
        os.makedirs(carpeta, exist_ok=True)
        for nombre, tabla in construir().items():
            ruta = os.path.join(carpeta, f"{nombre}.parquet")
            # snappy y no zstd: es lo que el lector de Parquet de Power Query admite
            # con seguridad en todas las versiones que nos importan.
            pq.write_table(tabla, ruta, compression="snappy", **CODIFICACION.get((escenario, nombre), {}))
            print(f"{tabla.num_rows:>9,} filas  {os.path.getsize(ruta):>9,} bytes  {ruta}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
