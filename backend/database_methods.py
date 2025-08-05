# backend/database_methods.py

tracks_schema = '''
CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY,
    title TEXT,
    artist TEXT,
    album TEXT,
    listen_count INTEGER,
    file_name TEXT UNIQUE,
    file_url TEXT UNIQUE,
    scraped_from_genre TEXT,
    vocals INTEGER,
    drums INTEGER,
    bass INTEGER,
    guitar INTEGER,
    piano INTEGER,
    others INTEGER
)
'''

genres_schema = '''
CREATE TABLE IF NOT EXISTS genres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
'''

track_genres_schema = '''
CREATE TABLE IF NOT EXISTS track_genres (
    track_id INTEGER,
    genre_id INTEGER,
    PRIMARY KEY (track_id, genre_id),
    FOREIGN KEY (track_id) REFERENCES tracks(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id)
)
'''

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute(tracks_schema)
    cursor.execute(genres_schema)
    cursor.execute(track_genres_schema)
    conn.commit()

def get_all_genres(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM genres")
    genre_rows = cursor.fetchall()
    genre_mapping = {genre_id: genre_name for genre_id, genre_name in genre_rows}
    genre_list_text = "\n".join([f"{gid}: {gname}" for gid, gname in genre_mapping.items()])
    return genre_list_text

def insert_track_metadata(conn, track_info):
    """
    Insert a new track row into the database (without instrument info yet).
    track_info: tuple of (id, title, artist, album, listen_count, file_name, file_url, scraped_from_genre)
    """
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tracks (
            id, title, artist, album, listen_count,
            file_name, file_url, scraped_from_genre,
            vocals, drums, bass, guitar, piano, others
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL)
    ''', track_info)
    conn.commit()

def update_instrument_presence(conn, file_name, instruments):
    """
    Updates the 6 instrument columns for a given track.
    instruments should be (vocals, drums, bass, piano, guitar, others)
    """
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tracks
        SET vocals = ?, drums = ?, bass = ?, piano = ?, guitar = ?, others = ?
        WHERE file_name = ?
    """, (*instruments, file_name))
    conn.commit()
    print(f"Updating DB for {file_name}: {instruments}")


def is_song_already_processed(conn, file_name):
    """
    Checks whether the track's `vocals` field is already set — 
    indicating the song has been processed.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT vocals FROM tracks WHERE file_name = ?", (file_name,))
    row = cursor.fetchone()
    return row is not None and row[0] is not None

def insert_genre_if_missing(conn, genre_name):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM genres WHERE name = ?", (genre_name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute("INSERT INTO genres (name) VALUES (?)", (genre_name,))
    conn.commit()
    return cursor.lastrowid

def insert_track_genre_mapping(conn, track_id, genre_id):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO track_genres (track_id, genre_id)
        VALUES (?, ?)
    """, (track_id, genre_id))
    conn.commit()

def fetch_all_tracks(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks")
    return cursor.fetchall()

def get_track_genres(conn, track_id):
    """Get all genres for a specific track"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT g.name 
        FROM genres g
        JOIN track_genres tg ON g.id = tg.genre_id
        WHERE tg.track_id = ?
    """, (track_id,))
    return [row[0] for row in cursor.fetchall()]