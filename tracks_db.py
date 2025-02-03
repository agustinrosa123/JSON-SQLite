import sqlite3
import csv

# Conectar a la base de datos SQLite
conn = sqlite3.connect('tracks.sqlite')
cur = conn.cursor()

# Eliminar tablas si ya existen para evitar duplicados
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

# Abrir el archivo CSV y leer los datos
with open('tracks.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Saltar la primera fila (encabezados)

    for row in reader:
        track_title, artist_name, album_title, genre_name, length, rating, count = row

        # Insertar o ignorar en Artist
        cur.execute('''INSERT OR IGNORE INTO Artist (name) VALUES (?)''', (artist_name,))
        cur.execute('SELECT id FROM Artist WHERE name = ?', (artist_name,))
        artist_id = cur.fetchone()[0]

        # Insertar o ignorar en Genre
        cur.execute('''INSERT OR IGNORE INTO Genre (name) VALUES (?)''', (genre_name,))
        cur.execute('SELECT id FROM Genre WHERE name = ?', (genre_name,))
        genre_id = cur.fetchone()[0]

        # Insertar o ignorar en Album
        cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)''', (album_title, artist_id))
        cur.execute('SELECT id FROM Album WHERE title = ?', (album_title,))
        album_id = cur.fetchone()[0]

        # Insertar en Track
        cur.execute('''INSERT OR IGNORE INTO Track (title, album_id, genre_id, len, rating, count)
                       VALUES (?, ?, ?, ?, ?, ?)''',
                    (track_title, album_id, genre_id, length, rating, count))

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("Base de datos creada exitosamente.")
