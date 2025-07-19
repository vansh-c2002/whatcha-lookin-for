# Instantiates the database

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        song_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist TEXT,
        duration REAL,
        vocals BOOLEAN,
        bass BOOLEAN,
        drums BOOLEAN,
        others BOOLEAN,
        filename TEXT UNIQUE
    )
    ''')
    conn.commit()

def insert_song(conn, title, artist, duration, vocals, bass, drums, others, filename):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO songs (title, artist, duration, vocals, bass, drums, others, filename)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, artist, duration, vocals, bass, drums, others, filename))
    conn.commit()
    return cursor.lastrowid  # Returns the song_id

def is_song_already_processed(conn, filename):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM songs WHERE filename = ?", (filename,))
    return cursor.fetchone() is not None

def fetch_all_songs(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM songs')
    return cursor.fetchall()