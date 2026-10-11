"""Formato de números y fechas en español (punto de miles, coma decimal)."""

MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def fmt_mes(fecha) -> str:
    """Timestamp -> 'ago-2020'."""
    return f"{MESES[fecha.month - 1]}-{fecha.year}"


def fmt_miles(x: float) -> str:
    return f"{x:,.0f}".replace(",", ".")


def fmt_pct(x: float, signo: bool = True) -> str:
    s = f"{x:+.1f}" if signo else f"{x:.1f}"
    return s.replace(".", ",") + "%"


def fmt_signed(x: float) -> str:
    return f"{x:+,.0f}".replace(",", ".")


def fmt_num(x: float, dec: int = 1) -> str:
    return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_p(p: float) -> str:
    """p-valor para insertar después de 'p': '< 0,001' o '= 0,031'."""
    return "< 0,001" if p < 0.001 else f"= {fmt_num(p, 3)}"
