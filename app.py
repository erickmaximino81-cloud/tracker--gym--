import os
from flask import Flask, render_template, redirect, url_for, request
# Importamos todas las funciones necesarias desde la carpeta correcta 'logica'
from logica.base_datos import init_db, guardar_entrenamiento_completo, obtener_estadisticas_por_ejercicio, get_db

# 1. Detectar la ubicación exacta del proyecto
ruta_base = os.path.abspath(os.path.dirname(__file__))

# 2. Configurar Flask con rutas absolutas
app = Flask(__name__, 
            template_folder=os.path.join(ruta_base, 'templates'),
            static_folder=os.path.join(ruta_base, 'static'))

# 🚨 DIAGNÓSTICO DE CARPETAS 🚨
print("\n" + "🔍" * 20)
print("SISTEMA DE DIAGNÓSTICO DE CARPETAS:")
print(f"Ruta static: {app.static_folder}")
print(f"¿Existe la carpeta?: {os.path.exists(app.static_folder)}")

if os.path.exists(app.static_folder):
    archivos = os.listdir(app.static_folder)
    print(f"Archivos encontrados dentro de 'static': {archivos}")
else:
    print("La carpeta static no existe en esa ruta.")
print("🔍" * 20 + "\n")

# Inicializar la base de datos al arrancar
init_db()

# ─── RUTA PRINCIPAL: INICIO ───
@app.route('/')
def inicio():
    historial_crudo = []
    ejercicios_agrupados = {}
    
    try:
        # 1. Traemos todo el historial limpio desde la base de datos
        historial_crudo = obtener_estadisticas_por_ejercicio()
        print(f"📦 Python leyó esto de la BD: {len(historial_crudo)} registros.")
        
        # 2. Agrupamos manualmente en Python para las gráficas de estadísticas
        for serie in historial_crudo:
            nombre = serie.get('ejercicio')
            if nombre:
                if nombre not in ejercicios_agrupados:
                    ejercicios_agrupados[nombre] = []
                ejercicios_agrupados[nombre].append(serie)
                
        print(f"📊 [DIAGNÓSTICO] Ejercicios detectados para gráficas: {list(ejercicios_agrupados.keys())}\n")
        
    except Exception as e:
        print(f"\n❌ [ERROR EN INICIO - LECTURA BD]: {e}\n")
        historial_crudo = []
        ejercicios_agrupados = {}

    # Cargamos el index.html pasando los datos limpios
    return render_template('index.html', 
                           lista_stats=ejercicios_agrupados,
                           registros=historial_crudo)


# ─── RUTA: PROCESAR FORMULARIO (POST) ───
@app.route('/ejecutar-accion', methods=['POST'])
def ejecutar_accion():
    # 📥 Capturamos los datos que vienen desde el HTML (Usando los 'name' del nuevo formulario)
    fecha = request.form.get('fecha')
    tipo = request.form.get('tipo', 'Fuerza') 
    ejercicio = request.form.get('ejercicio')
    musculo = request.form.get('musculo', 'General')
    duracion = int(request.form.get('duracion', 0) or 0)
    series = int(request.form.get('series', 1) or 1)
    repeticiones = int(request.form.get('repeticiones', 0) or 0)
    peso = float(request.form.get('peso', 0.0) or 0.0)
    esfuerzo = int(request.form.get('esfuerzo', 5) or 5)
    notes = request.form.get('notas', '')

    print(f"\n📥 [ESPÍA 1] El navegador mandó: {ejercicio}, {peso}kg, {repeticiones}reps, RPE: {esfuerzo}")

    # 2. Guardamos de forma segura en la base de datos con la función completa
    if ejercicio:
        try:
            guardar_entrenamiento_completo(fecha, tipo, ejercicio, musculo, duracion, series, repeticiones, peso, esfuerzo, notes)
            print(f"✅ ¡Guardado con éxito en la BD!: {ejercicio}")
        except Exception as e:
            print(f"❌ Error al escribir en la BD: {e}")

    # 3. Diagnóstico inmediato post-guardado
    try:
        chequeo_inmediato = obtener_estadisticas_por_ejercicio()
        print(f"🔎 [ESPÍA 2] ¿Filas totales en la BD tras guardar?: {len(chequeo_inmediato)}\n")
    except Exception as e:
        print(f"❌ Falló el espía de revisión: {e}\n")
        
    return redirect(url_for('inicio'))


# ─── RUTA: ELIMINAR REGISTRO ───
@app.route('/eliminar/<int:eid>', methods=['POST'])
def eliminar(eid):
    """Borra un entrenamiento por ID de forma segura desde la tabla."""
    print(f"\n🗑️ [SOLICITUD BORRADO] Intentando eliminar el registro con ID: {eid}")
    try:
        # Usamos la conexión limpia que ya importamos correctamente de logica.base_datos
        with get_db() as conn:
            conn.execute("DELETE FROM entrenamientos WHERE id = ?", (eid,))
            conn.commit()
        print(f"✅ [BD BORRADO] Registro {eid} eliminado exitosamente.")
    except Exception as e:
        print(f"❌ [ERROR AL BORRAR]: {e}")
        
    return redirect(url_for("inicio"))


if __name__ == '__main__':
    app.run(debug=True)