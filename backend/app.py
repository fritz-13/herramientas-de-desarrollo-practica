from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "incidentes.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS incidentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            categoria TEXT NOT NULL DEFAULT 'incidente',
            prioridad TEXT NOT NULL DEFAULT 'media',
            estado TEXT NOT NULL DEFAULT 'abierto',
            creado_por TEXT DEFAULT 'anónimo',
            fecha_creacion TEXT NOT NULL,
            fecha_actualizacion TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/api/incidentes", methods=["GET"])
def listar_incidentes():
    conn = get_db()
    rows = conn.execute("SELECT * FROM incidentes ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/incidentes/<int:id>", methods=["GET"])
def obtener_incidente(id):
    conn = get_db()
    row = conn.execute("SELECT * FROM incidentes WHERE id = ?", (id,)).fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "Incidente no encontrado"}), 404
    return jsonify(dict(row))


@app.route("/api/incidentes", methods=["POST"])
def crear_incidente():
    data = request.get_json()
    now = datetime.now().isoformat()
    conn = get_db()
    cursor = conn.execute(
        """INSERT INTO incidentes
        (titulo, descripcion, categoria, prioridad, estado, creado_por, fecha_creacion, fecha_actualizacion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            data.get("titulo", "Sin título"),
            data.get("descripcion", ""),
            data.get("categoria", "incidente"),
            data.get("prioridad", "media"),
            data.get("estado", "abierto"),
            data.get("creado_por", "anónimo"),
            now,
            now,
        ),
    )
    conn.commit()
    incidente = dict(
        conn.execute(
            "SELECT * FROM incidentes WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    )
    conn.close()
    return jsonify(incidente), 201


@app.route("/api/incidentes/<int:id>", methods=["PUT"])
def actualizar_incidente(id):
    data = request.get_json()
    now = datetime.now().isoformat()
    conn = get_db()
    row = conn.execute("SELECT * FROM incidentes WHERE id = ?", (id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({"error": "Incidente no encontrado"}), 404
    conn.execute(
        """UPDATE incidentes SET
        titulo = ?, descripcion = ?, categoria = ?, prioridad = ?, estado = ?,
        creado_por = ?, fecha_actualizacion = ?
        WHERE id = ?""",
        (
            data.get("titulo", row["titulo"]),
            data.get("descripcion", row["descripcion"]),
            data.get("categoria", row["categoria"]),
            data.get("prioridad", row["prioridad"]),
            data.get("estado", row["estado"]),
            data.get("creado_por", row["creado_por"]),
            now,
            id,
        ),
    )
    conn.commit()
    incidente = dict(
        conn.execute("SELECT * FROM incidentes WHERE id = ?", (id,)).fetchone()
    )
    conn.close()
    return jsonify(incidente)


@app.route("/api/incidentes/<int:id>", methods=["DELETE"])
def eliminar_incidente(id):
    conn = get_db()
    row = conn.execute("SELECT * FROM incidentes WHERE id = ?", (id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({"error": "Incidente no encontrado"}), 404
    conn.execute("DELETE FROM incidentes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Incidente eliminado"}), 200


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
