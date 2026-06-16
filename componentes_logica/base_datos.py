# ── componentes_logica/base_datos.py ─────────────────────────
import os
import sqlite3

# Ruta absoluta al archivo del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "gymtracker.db")


def get_db() -> sqlite3.Connection:
    """Retorna una conexión limpia a SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Crea la tabla exactamente con tu esquema original."""
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS entrenamientos (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha         TEXT    NOT NULL,
                tipo          TEXT    NOT NULL,
                ejercicio     TEXT    NOT NULL,
                musculo       TEXT,
                duracion      INTEGER NOT NULL,
                series        INTEGER,
                repeticiones  INTEGER,
                peso          REAL,
                calorias      INTEGER,
                esfuerzo      INTEGER DEFAULT 5,
                notas         TEXT,
                creado_en     TEXT    DEFAULT (datetime('now','localtime'))
            )
        """
        )
        conn.commit()


def guardar_entrenamiento_completo(fecha, tipo, ejercicio, musculo, duracion, series, repeticiones, peso, esfuerzo, notas) -> None:
    """Inserta absolutamente todos los campos capturados del formulario."""
    sql = """
        INSERT INTO entrenamientos (fecha, tipo, ejercicio, musculo, duracion, series, repeticiones, peso, calorias, esfuerzo, notas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    calorias_defecto = 0  # Mantenemos este valor fijo por defecto ya que no lo pide el form

    with get_db() as conn:
        conn.execute(
            sql,
            (
                fecha,
                tipo,
                ejercicio,
                musculo,
                duracion,
                series,
                repeticiones,
                peso,
                calorias_defecto,
                esfuerzo,
                notas,
            ),
        )
        conn.commit()
    print(f"💾 [BD ESCRITURA] ¡Historial completo guardado!: {ejercicio} ({peso}kg) - Tipo: {tipo} - RPE: {esfuerzo}")


def obtener_estadisticas_por_ejercicio():
    """Trae TODO el historial de entrenamientos ordenado por fecha para poder comparar."""
    query = """
        SELECT *
        FROM entrenamientos 
        ORDER BY fecha ASC
    """
    with get_db() as conn:
        filas = conn.execute(query).fetchall()
        return [dict(row) for row in filas]