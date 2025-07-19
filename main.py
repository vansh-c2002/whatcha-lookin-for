import sqlite3
from pathlib import Path
from extractor import detect_instrument_presence_song, detect_basic_info
from database_methods import create_tables, insert_song, is_song_already_processed
from separate_stems import separate_stems

# for song_file in Path(parent_folder).glob("*.mp3"):
    # separate_stems(song_file)
    # for stem in stems:
        # piano = instrument_detector(stem)
        # 
    # insert_song(conn, title, artist, duration, vocals, bass, drums, others):

parent_folder = "/Users/vanshc/Desktop/Songs"

conn = sqlite3.connect('song_database.db')

create_tables(conn)

# Running stem separation
for song_file in Path(parent_folder).glob("*.mp3"):
    if is_song_already_processed(conn, song_file.name):
        continue
    separate_stems(song_file)

# Extracting and adding metadata to database
for folder in (Path(parent_folder) / 'htdemucs').iterdir():
    if folder.is_dir():
        title, artist, duration = detect_basic_info(folder)
        filename = f"{artist} - {title}.mp3"

        if is_song_already_processed(conn, filename):
            continue

        vocals, drums, bass, other = detect_instrument_presence_song(folder)
        insert_song(conn, title, artist, duration, vocals, bass, drums, other, filename)

print("Done!")
conn.close()