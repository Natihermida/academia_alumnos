from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Ruta para inicializar la base de datos
def init_db():
    conn = sqlite3.connect('academia.db')
    c = conn.cursor()
    
    # Crear la tabla 'asignaturas' si no existe
    c.execute('''
    CREATE TABLE IF NOT EXISTS asignaturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )''')

    # Crear la tabla 'alumnos' si no existe
    c.execute('''
    CREATE TABLE IF NOT EXISTS alumnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        asignatura_id INTEGER,
        calificacion REAL,
        FOREIGN KEY (asignatura_id) REFERENCES asignaturas(id)
    )''')

    conn.commit()
    conn.close()

# Inicializar la base de datos cuando se ejecuta la aplicación
init_db()

# Ruta para mostrar alumnos registrados
@app.route('/')
def index():
    conn = sqlite3.connect('academia.db')
    c = conn.cursor()
    c.execute('SELECT * FROM alumnos')
    alumnos = c.fetchall()
    conn.close()
    return render_template('index.html', alumnos=alumnos)

# Ruta para registrar un alumno
@app.route('/registrar_alumno', methods=['GET', 'POST'])
def registrar_alumno():
    if request.method == 'POST':
        nombre = request.form['nombre']
        asignatura_id = request.form['asignatura_id']
        calificacion = request.form['calificacion']
        
        conn = sqlite3.connect('academia.db')
        c = conn.cursor()
        c.execute('INSERT INTO alumnos (nombre, asignatura_id, calificacion) VALUES (?, ?, ?)', 
                  (nombre, asignatura_id, calificacion))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    return render_template('registrar_alumno.html')

# Ruta para mostrar las asignaturas (opcional, si deseas agregar más funcionalidades)
@app.route('/asignaturas')
def asignaturas():
    conn = sqlite3.connect('academia.db')
    c = conn.cursor()
    c.execute('SELECT * FROM asignaturas')
    asignaturas = c.fetchall()
    conn.close()
    return render_template('asignaturas.html', asignaturas=asignaturas)

if __name__ == '__main__':
    app.run(debug=True)

