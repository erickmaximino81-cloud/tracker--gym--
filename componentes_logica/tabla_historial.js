/* ── tabla_historial.js ───────────────────────────────────────
   Filtro de búsqueda en tiempo real sobre la tabla
   ─────────────────────────────────────────────────────────── */

function filtrarTabla() {
  const q = document.getElementById('buscar').value.toLowerCase();
  document.querySelectorAll('#tablaHistorial tbody tr').forEach(row => {
    row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
  });
}