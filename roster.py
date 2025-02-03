import json
import sqlite3

# Conectar a la base de datos SQLite
try:
    conn = sqlite3.connect('roster.db')
    cur = conn.cursor()
except sqlite3.Error as e:
    print(f"Error al conectar con la base de datos: {e}")
    exit(1)

# Crear las tablas si no existen
try:
    cur.execute('''
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Course (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT
    )''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Member (
        user_id INTEGER,
        course_id INTEGER,
        role TEXT,
        PRIMARY KEY (user_id, course_id),
        FOREIGN KEY (user_id) REFERENCES User (id),
        FOREIGN KEY (course_id) REFERENCES Course (id)
    )''')
except sqlite3.Error as e:
    print(f"Error al crear las tablas: {e}")
    exit(1)

# Cargar el archivo JSON
try:
    with open('roster_data.json') as file:
        data = json.load(file)
    print("Datos cargados correctamente:")
    print(data)  # Verificar cómo se ve el JSON cargado
except json.JSONDecodeError as e:
    print(f"Error al cargar JSON: {e}")
    exit(1)

# Procesar los datos y agregar a las tablas
for item in data:
    name = item[0]
    course_title = item[1]
    role = item[2]

    # Insertar usuario si no existe
    cur.execute('INSERT OR IGNORE INTO User (name) VALUES (?)', (name,))
    # Obtener el id del usuario recién insertado o existente
    cur.execute('SELECT id FROM User WHERE name = ?', (name,))
    user_id = cur.fetchone()[0]

    # Insertar curso si no existe
    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)', (course_title,))
    # Obtener el id del curso recién insertado o existente
    cur.execute('SELECT id FROM Course WHERE title = ?', (course_title,))
    course_id = cur.fetchone()[0]

    # Insertar miembro (relación entre usuario y curso)
    cur.execute('INSERT OR REPLACE INTO Member (user_id, course_id, role) VALUES (?, ?, ?)', (user_id, course_id, role))

# Confirmar los cambios
conn.commit()

# Consultar los resultados
try:
    cur.execute('''
    SELECT 'XYZZY' || hex(User.name || Course.title || Member.role) AS X
    FROM User
    JOIN Member ON User.id = Member.user_id
    JOIN Course ON Member.course_id = Course.id
    ORDER BY X
    LIMIT 1;
    ''')
    rows = cur.fetchall()
    for row in rows:
        print(row)
except sqlite3.Error as e:
    print(f"Error al ejecutar la consulta SQL: {e}")

# Cerrar la conexión
conn.close()
