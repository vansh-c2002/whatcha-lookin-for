# Instantiates the database

songs_db = '''
CREATE TABLE IF NOT EXISTS songs (
    song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT,
    duration_in_seconds REAL,
    vocals BOOLEAN,
    bass BOOLEAN,
    drums BOOLEAN,
    others BOOLEAN,
    filename TEXT UNIQUE,
    genre TEXT
)
'''

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute(songs_db)
    conn.commit()

def insert_song(conn, title, artist, duration_in_seconds, vocals, bass, drums, others, filename):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO songs (title, artist, duration_in_seconds, vocals, bass, drums, others, filename)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, artist, duration_in_seconds, vocals, bass, drums, others, filename))
    conn.commit()
    return cursor.lastrowid  # Returns the song_id

def insert_genres(conn, paths_n_genres):
    cursor = conn.cursor()
    for i in paths_n_genres:
        cursor.execute('UPDATE songs SET genre = ? WHERE filename = ?', (paths_n_genres[i], i))
        conn.commit()

def is_song_already_processed(conn, filename):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM songs WHERE filename = ?", (filename,))
    return cursor.fetchone() is not None

def fetch_all_songs(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM songs')
    return cursor.fetchall()