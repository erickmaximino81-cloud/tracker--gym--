# ── estadisticas.py ───────────────────────────────────────────
# Lógica de negocio: calcula estadísticas agregadas.
# Usado por la ruta principal (index) en base_datos/routes.
# ──────────────────────────────────────────────────────────────

from collections import Counter


def calcular_stats(registros: list[dict]) -> dict:
    """Calcula estadísticas agregadas a partir de los registros."""
    if not registros:
        return {
            "total_sesiones":    0,
            "total_minutos":     0,
            "total_calorias":    0,
            "peso_maximo":       0,
            "esfuerzo_promedio": 0,
            "tipo_favorito":     None,
            "por_tipo":          {},
        }

    total_sesiones = len(registros)
    contador_tipos = Counter(r["tipo"] for r in registros)

    return {
        "total_sesiones":    total_sesiones,
        "total_minutos":     sum(r["duracion"]  or 0 for r in registros),
        "total_calorias":    sum(r["calorias"]  or 0 for r in registros),
        "peso_maximo":       max((r["peso"]     or 0 for r in registros), default=0),
        "esfuerzo_promedio": round(
            sum(r["esfuerzo"] or 5 for r in registros) / total_sesiones, 1
        ),
        "tipo_favorito":     contador_tipos.most_common(1)[0][0],
        "por_tipo":          dict(contador_tipos.most_common()),
    }