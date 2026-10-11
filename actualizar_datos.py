"""Regenera todos los datos procesados (data/processed/) desde los archivos originales (data/raw/).

Ejecuta los tres cuadernos en orden y después corre los controles de datos (tests/test_datos.py):
  01  comercio exterior: importaciones y exportaciones por rama y país, con los totales de control del INDEC
  02  empleo, salarios, producción, empresas y capacidad instalada por rama
  03  análisis: cambios por rama, la respuesta a la pregunta central, uso económico, correlaciones y panel

Uso, desde la carpeta del proyecto (tarda unos minutos):
    .\\.venv\\Scripts\\python.exe actualizar_datos.py
Para correr solo algunos cuadernos (por ejemplo, si solo cambió el empleo):
    .\\.venv\\Scripts\\python.exe actualizar_datos.py 02 03
"""
import subprocess
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

RAIZ = Path(__file__).resolve().parent
CUADERNOS = {"01": "01_limpieza_comercio_exterior.ipynb", "02": "02_limpieza_empleo_salarios_industria.ipynb", "03": "03_analisis_por_rama.ipynb"}


def correr(codigo: str) -> None:
    ruta = RAIZ / "notebooks" / CUADERNOS[codigo]
    inicio = time.time()
    print(f"Cuaderno {codigo} ({ruta.name})... ", end="", flush=True)
    nb = nbformat.read(ruta, as_version=4)
    NotebookClient(nb, timeout=1800, kernel_name="python3", resources={"metadata": {"path": str(ruta.parent)}}).execute()
    nbformat.write(nb, ruta)
    print(f"listo en {time.time() - inicio:.0f} s")


if __name__ == "__main__":
    if sys.platform == "win32":
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())   # evita un aviso de jupyter en Windows
    pedidos = sys.argv[1:] or list(CUADERNOS)
    for codigo in pedidos:
        correr(codigo)
    print("Controles de los datos:")
    sys.exit(subprocess.call([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(RAIZ / "tests" / "test_datos.py")]))
