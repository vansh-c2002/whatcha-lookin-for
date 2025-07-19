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
        others BOOLEAN
    )
    ''')
    conn.commit()

def insert_song(conn, title, artist, duration, vocals, bass, drums, others):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO songs (title, artist, duration, vocals, bass, drums, others)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, artist, duration, vocals, bass, drums, others))
    conn.commit()
    return cursor.lastrowid  # Returns the song_id

def fetch_all_songs(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM songs')
    return cursor.fetchall()