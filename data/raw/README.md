# Datos crudos

Archivos originales, sin modificar, organizados por tema.

| Carpeta | Contenido | Fuente | Cobertura |
|---|---|---|---|
| `comercio_exterior/importaciones/` | Importaciones por producto (NCM) y país de origen, una tabla por año (`impot16-18.csv` solo CIF; `impoa19-25.csv` con FOB, flete, seguro y CIF) + totales de control (`itot*.csv`) | INDEC, sistema comex | 2016-2025 |
| `comercio_exterior/exportaciones/` | Exportaciones por producto y país de destino (`expot16-17.csv`, `expona18-25.csv`) + totales de control (`etot*.csv`) | INDEC, sistema comex | 2016-2025 |
| `comercio_exterior/Tablas-Paises-F2668.xls` | Tabla oficial de códigos de país | ARCA | vigente |
| `comercio_exterior/clasificaciones/` | Correspondencia de productos (HS 6 dígitos, versiones 2012, 2017 y 2022) con uso económico (BEC rev. 4): consumo, insumos y capital | Banco Mundial, WITS | vigente |
| `empleo/` | Empleo asalariado privado registrado por rama CIIU (trimestral y anual) | Ministerio de Trabajo, OEDE | 1996-1T 2026 |
| `empresas/` | Empresas privadas activas por rama CIIU | Ministerio de Trabajo, OEDE | 1996-2024 |
| `salarios/` | Remuneraciones por rama CIIU (mensual y anual) e índice de salarios | OEDE / INDEC | 1995-2026 |
| `precios/` | IPC por región y división | INDEC | dic 2016-ago 2026 |
| `industria/` | IPI manufacturero por rama y subrama, y utilización de la capacidad instalada | INDEC | 2016-2026 |

Los CSV de `comercio_exterior/importaciones/` y `exportaciones/` pesan ~100 MB y no se suben al repositorio: se descargan con
`python src/download_comex.py`. El resto de los archivos de esta carpeta son livianos.
