from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Función para inicializar la base de datos
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

# Ruta para la página principal (index)
@app.route('/')
def index():
    conn = sqlite3.connect('academia.db')
    c = conn.cursor()

    # Obtener alumnos
    c.execute('SELECT * FROM alumnos')
    alumnos = c.fetchall()

    # Obtener asignaturas
    c.execute('SELECT * FROM asignaturas')
    asignaturas = c.fetchall()

    conn.close()

    # Pasar asignaturas y alumnos a la plantilla
    return render_template('index.html', asignaturas=asignaturas, alumnos=alumnos)

# Ruta para registrar un alumno
@app.route('/registrar_alumno', methods=['GET', 'POST'])
def registrar_alumno():
    conn = sqlite3.connect('academia.db')
    c = conn.cursor()
    c.execute('SELECT * FROM asignaturas')  # Obtener asignaturas
    asignaturas = c.fetchall()
    conn.close()

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

    return render_template('registrar_alumno.html', asignaturas=asignaturas)

# Ruta para añadir una asignatura
@app.route('/añadir_asignatura', methods=['GET', 'POST'])
def añadir_asignatura():
    if request.method == 'POST':
        nombre = request.form['nombre_asignatura']
        
        conn = sqlite3.connect('academia.db')
        c = conn.cursor()
        c.execute('INSERT INTO asignaturas (nombre) VALUES (?)', (nombre,))
        conn.commit()
        conn.close()
        
        return redirect(url_for('asignaturas'))

    return render_template('añadir_asignatura.html')

# Ruta para ver las asignaturas y eliminarlas
@app.route('/asignaturas')
def asignaturas():
    conn = sqlite3.connect('academia.db')
    c = conn.cursor()

    # Obtener asignaturas
    c.execute('SELECT * FROM asignaturas')
    asignaturas = c.fetchall()
    conn.close()

    return render_template('asignaturas.html', asignaturas=asignaturas)

from flask import request

@app.route('/eliminar_asignatura/<int:id>', methods=['POST'])
def eliminar_asignatura(id):
    if request.method == 'POST':
        conn = sqlite3.connect('academia.db')
        c = conn.cursor()

        # Eliminar asignatura
        c.execute('DELETE FROM asignaturas WHERE id = ?', (id,))
        conn.commit()
        conn.close()

        return redirect(url_for('asignaturas'))
@app.route('/area_profesor')
def area_profesor():
    conn = sqlite3.connect('academia.db')
    c = conn.cursor()

    # Obtener los alumnos con sus asignaturas
    c.execute('''
        SELECT alumnos.id, alumnos.nombre, asignaturas.nombre, alumnos.calificacion
        FROM alumnos
        JOIN asignaturas ON alumnos.asignatura_id = asignaturas.id
    ''')
    alumnos = c.fetchall()

    conn.close()

    return render_template('area_profesor.html', alumnos=alumnos)


    return render_template('area_profesor.html', alumnos=alumnos)
@app.route('/editar_alumno/<int:id>', methods=['GET', 'POST'])
def editar_alumno(id):
    conn = sqlite3.connect('academia.db')
    c = conn.cursor()

    # Obtener los datos del alumno
    c.execute('SELECT * FROM alumnos WHERE id = ?', (id,))
    alumno = c.fetchone()

    # Si no existe el alumno, redirigir a área profesor
    if not alumno:
        conn.close()
        return redirect(url_for('area_profesor'))

    # Obtener todas las asignaturas
    c.execute('SELECT * FROM asignaturas')
    asignaturas = c.fetchall()

    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        asignatura_id = request.form['asignatura_id']
        calificacion = request.form['calificacion']

        # Actualizar en la base de datos
        c.execute('UPDATE alumnos SET nombre = ?, asignatura_id = ?, calificacion = ? WHERE id = ?',
                  (nombre, asignatura_id, calificacion, id))
        conn.commit()
        conn.close()

        return redirect(url_for('area_profesor'))

    conn.close()
    return render_template('editar_alumno.html', alumno=alumno, asignaturas=asignaturas)
@app.route('/eliminar_alumno/<int:id>', methods=['GET'])
def eliminar_alumno(id):
    conn = sqlite3.connect('academia.db')
    c = conn.cursor()

    # Verificar si el alumno existe antes de eliminar
    c.execute('SELECT * FROM alumnos WHERE id = ?', (id,))
    alumno = c.fetchone()

    if alumno:
        c.execute('DELETE FROM alumnos WHERE id = ?', (id,))
        conn.commit()

    conn.close()
    return redirect(url_for('area_profesor'))



if __name__ == '__main__':
    app.run(debug=True)

