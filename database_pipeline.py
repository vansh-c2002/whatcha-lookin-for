import sqlite3
from pathlib import Path
from extractor import detect_instrument_presence_song, detect_basic_info
from database_methods import create_tables, insert_song
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

separate_stems(parent_folder)

# for file in htdemucs subfolder, do all this
# then run a for loop through the files in the subfolder

for folder in (Path(parent_folder) / 'htdemucs').iterdir() :
    if folder.is_dir():
        vocals, drums, bass, other = detect_instrument_presence_song(folder)
        title, artist, duration = detect_basic_info(folder)
        insert_song(conn, title, artist, duration, vocals, bass, drums, other)

print("Done!")
conn.close()