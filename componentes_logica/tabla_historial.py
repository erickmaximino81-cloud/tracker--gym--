# ── tabla_historial.py ────────────────────────────────────────
# Ruta Flask para eliminar un registro de la tabla historial.
# ──────────────────────────────────────────────────────────────

from flask import redirect, url_for
from base_datos.base_datos import get_db


def eliminar(eid: int):
    """POST /eliminar/<eid> — borra un entrenamiento por ID."""
    with get_db() as conn:
        conn.execute("DELETE FROM entrenamientos WHERE id = ?", (eid,))
        conn.commit()
    return redirect(url_for("main.index", msg="🗑️ Registro eliminado."))