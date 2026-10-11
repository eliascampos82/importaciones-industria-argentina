"""Descarga las bases anuales de importaciones y exportaciones del sistema comex de INDEC.

Uso:  python src/download_comex.py            (años 2016-2025)
      python src/download_comex.py 2019 2025  (rango)

El patrón de URL sale del código del propio sitio (comex.indec.gob.ar): /files/zips/{tipo}_{año}_Y.zip.
Es idempotente: si los CSV de un año ya están, no vuelve a descargar. Se extraen solo las tablas
principales y sus totales de control (no las bases por provincia ni los Excel auxiliares).
"""
import io
import re
import sys
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://comex.indec.gob.ar/files/zips/{tipo}_{anio}_Y.zip"
RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "comercio_exterior"

# importaciones: impot16.csv / impoa19.csv (+ itott16 / itota19 = totales de control)
# exportaciones: expot16.csv / expona18.csv (priorizan producto) (+ etott16 / etotna18)
ARCHIVOS = {
    "imports": ("importaciones", re.compile(r"^(impo[at]|itot[at])\d{2}\.csv$", re.I)),
    "exports": ("exportaciones", re.compile(r"^(expo(t|na)|etot(t|na))\d{2}\.csv$", re.I)),
}


def descargar(tipo: str, anio: int) -> list[str]:
    carpeta, patron = ARCHIVOS[tipo]
    destino = RAW / carpeta
    destino.mkdir(parents=True, exist_ok=True)
    aa = str(anio)[-2:]
    if any(f.name.endswith(f"{aa}.csv") for f in destino.glob("*.csv")):
        return [f"{tipo} {anio}: ya estaba"]

    req = Request(URL.format(tipo=tipo, anio=anio), headers={"User-Agent": "Mozilla/5.0"})
    datos = urlopen(req, timeout=120).read()
    if datos[:2] != b"PK":   # el sitio devuelve HTML (con HTTP 200) cuando el archivo no existe
        raise ValueError(f"{tipo} {anio}: la respuesta no es un zip")

    guardados = []
    with zipfile.ZipFile(io.BytesIO(datos)) as zf:
        for info in zf.infolist():
            if patron.match(info.filename) and info.filename.endswith(f"{aa}.csv"):
                (destino / info.filename.lower()).write_bytes(zf.read(info))
                guardados.append(info.filename.lower())
    return [f"{tipo} {anio}: {', '.join(guardados)}"]


if __name__ == "__main__":
    args = [int(a) for a in sys.argv[1:]]
    desde, hasta = (args[0], args[1]) if len(args) == 2 else (2016, 2025)
    for tipo in ARCHIVOS:
        for anio in range(desde, hasta + 1):
            for linea in descargar(tipo, anio):
                print(linea)
