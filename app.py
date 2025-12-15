from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'my-postgres-postgresql.carloscabreravas-dev.svc.cluster.local')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'microservicio')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS producto (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            descripcion TEXT NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/health', methods=['GET'])
def health():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM producto')
        productos = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/productos', methods=['POST'])
def create_producto():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        
        if not nombre or not descripcion:
            return jsonify({'error': 'nombre y descripcion son requeridos'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO producto (nombre, descripcion) VALUES (%s, %s) RETURNING id, nombre, descripcion',
            (nombre, descripcion)
        )
        producto = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'id': producto[0], 'nombre': producto[1], 'descripcion': producto[2]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
