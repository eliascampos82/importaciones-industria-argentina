"""
Clasificación única de ramas industriales para cruzar todas las fuentes.

Cada fuente usa una clasificación distinta:
  - Comercio exterior: NCM (producto, 8 dígitos; los 2 primeros = capítulo)
  - Empleo / salarios / empresas (OEDE): CIIU rev.3 a 2 dígitos
  - Producción industrial (IPI manufacturero, INDEC): divisiones y agrupaciones CLaNAE

Se usan como "rama" las 16 agrupaciones del IPI manufacturero (nivel de
desagregación más grueso de las tres fuentes), y las demás se mapean a ellas.
"""

RAMA_LABELS = {
    "15": "Alimentos y bebidas",
    "16": "Tabaco",
    "17": "Textiles (hilados y tejidos)",
    "18-19": "Prendas de vestir, cuero y calzado",
    "20-22": "Madera, papel, edición e impresión",
    "23": "Refinación de petróleo",
    "24": "Químicos (incl. farmacéuticos)",
    "25": "Caucho y plástico",
    "26": "Minerales no metálicos",
    "27": "Metálicas básicas",
    "28": "Productos de metal",
    "29": "Maquinaria y equipo",
    "30-33": "Informática, electrónica, eléctricos e instrumentos",
    "34": "Automotores y autopartes",
    "35": "Otro equipo de transporte",
    "36-38": "Muebles y otras manufacturas",
}
RAMAS = list(RAMA_LABELS)
TOTAL = "TOTAL"
TOTAL_LABEL = "Total industria manufacturera"

_CIIU2_A_RAMA = {
    15: "15", 16: "16", 17: "17", 18: "18-19", 19: "18-19",
    20: "20-22", 21: "20-22", 22: "20-22", 23: "23", 24: "24", 25: "25", 26: "26",
    27: "27", 28: "28", 29: "29", 30: "30-33", 31: "30-33", 32: "30-33", 33: "30-33",
    34: "34", 35: "35", 36: "36-38", 37: "36-38",
}


def ciiu2_to_rama(code):
    """Rama de un código CIIU de 2 dígitos; None si no es manufactura (agro, servicios, etc.)."""
    try:
        return _CIIU2_A_RAMA.get(int(float(code)))
    except (TypeError, ValueError):
        return None


# Capítulos NCM -> rama. None = no es manufactura (primario, minería) o no clasificable.
_CAP_A_RAMA = {
    **{c: "15" for c in range(15, 24)},
    24: "16",
    25: "26",
    **{c: "24" for c in range(28, 39)},
    39: "25", 40: "25",
    **{c: "18-19" for c in range(41, 44)},
    **{c: "20-22" for c in range(44, 50)},
    **{c: "17" for c in range(50, 61)},
    61: "18-19", 62: "18-19", 63: "17",
    64: "18-19", 65: "18-19", 66: "36-38", 67: "36-38",
    **{c: "26" for c in range(68, 71)},
    72: "27", 73: "28", **{c: "27" for c in range(74, 77)}, **{c: "27" for c in range(78, 82)},
    82: "28", 83: "28",
    84: "29", 85: "30-33",
    86: "35", 87: "34", 88: "35", 89: "35",
    90: "30-33", 91: "30-33", 92: "36-38", 93: "29",
    94: "36-38", 95: "36-38", 96: "36-38",
}


def ncm_to_rama(ncm):
    """Rama de un código NCM de 8 dígitos (nivel capítulo, con excepciones a 4 dígitos)."""
    code = str(ncm).zfill(8)
    cap, part = int(code[:2]), int(code[:4])
    if cap == 84 and 8469 <= part <= 8473:   # máquinas de oficina y computadoras
        return "30-33"
    if cap == 87 and 8711 <= part <= 8716:   # motos, bicicletas, sillas de ruedas
        return "35"
    if part == 9405:                          # artefactos de iluminación
        return "30-33"
    if cap == 27:                             # solo derivados refinados; crudo, gas, carbón y electricidad no son refinación
        return "23" if (2706 <= part <= 2708 or part == 2710 or 2712 <= part <= 2715) else None
    if cap == 71:                             # solo joyería; oro, plata y piedras sin trabajar son minería
        return "36-38" if 7113 <= part <= 7118 else None
    return _CAP_A_RAMA.get(cap)


# Bloques de "utilización de la capacidad instalada" (INDEC) que contienen a cada rama.
# Son bloques más gruesos que las ramas: donde un bloque agrupa varias ramas, es aproximado.
RAMA_A_UCI = {
    "15": "Productos alimenticios y bebidas",
    "16": "Productos del tabaco",
    "17": "Productos textiles",
    "18-19": "Productos textiles",
    "23": "Refinación del petróleo",
    "24": "Sustancias y productos químicos",
    "25": "Productos de caucho y plástico",
    "26": "Productos minerales no metálicos",
    "27": "Industrias metálicas básicas",
    "28": "Metalmecánica excluida industria automotriz",
    "29": "Metalmecánica excluida industria automotriz",
    "30-33": "Metalmecánica excluida industria automotriz",
    "34": "Industria automotriz",
    "35": "Metalmecánica excluida industria automotriz",
}
UCI_APROXIMADO = {"18-19", "28", "29", "30-33", "35"}
