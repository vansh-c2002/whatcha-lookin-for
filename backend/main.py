import importlib
import extractor
import database_methods
import separate_stems
import sqlite3

importlib.reload(extractor)
importlib.reload(database_methods)
importlib.reload(separate_stems)

from pathlib import Path
from extractor import detect_instrument_presence_song, detect_basic_info, detect_genre
from database_methods import create_tables, insert_song, is_song_already_processed, insert_genres
from separate_stems import separate_stems

# for song_file in Path(parent_folder).glob("*.mp3"):
    # separate_stems(song_file)
    # for stem in stems:
        # piano = instrument_detector(stem)
        # 
    # insert_song(conn, title, artist, duration, vocals, bass, drums, others):

parent_folder = "/Users/vanshc/Desktop/Songs"

conn = sqlite3.connect("backend/song_database.db")

create_tables(conn)

paths_n_genres = {}

# TODO: Perform each step song-wise!

# Running stem separation
for song_file in Path(parent_folder).glob("*.mp3"):
    if is_song_already_processed(conn, song_file.name):
        continue
    separate_stems(song_file)
    paths_n_genres[song_file.name] = detect_genre(song_file)

# Extracting and adding metadata to database
for folder in (Path(parent_folder) / 'htdemucs').iterdir():
    if folder.is_dir():
        title, artist, duration_in_seconds = detect_basic_info(folder)
        filename = f"{artist} - {title}.mp3"

        if is_song_already_processed(conn, filename):
            continue

        vocals, drums, bass, other = detect_instrument_presence_song(folder)
        insert_song(conn, title, artist, duration_in_seconds, vocals, bass, drums, other, filename) # Add something for image path

insert_genres(conn, paths_n_genres)

print("Done!")
conn.close()