import sqlite3
import shutil
from pathlib import Path
from tqdm import tqdm

from extractor import detect_instrument_presence_song
from separate_stems import separate_stems
from database_methods import is_song_already_processed, update_instrument_presence

DB_PATH = "backend/song_database_trial.db"
MP3_FOLDER = Path("mp3s")
STEMS_FOLDER = MP3_FOLDER/"htdemucs_6s" 

def delete_stems(folder_path):
    try:
        shutil.rmtree(folder_path)
    except Exception as e:
        print(f"⚠️ Couldn't delete stems in {folder_path}: {e}")

def process_single_song(file_name):
    song_file = MP3_FOLDER / file_name
    stem_folder = STEMS_FOLDER / song_file.stem

    try:
        separate_stems(song_file)

        if not stem_folder.exists():
            raise FileNotFoundError(f"Stems not found for {file_name}")

        instruments = detect_instrument_presence_song(stem_folder)
        print(f"Detected instruments for {file_name}: {instruments}")


        conn = sqlite3.connect(DB_PATH)
        update_instrument_presence(conn, file_name, instruments)
        conn.close()


        if stem_folder.exists():
            delete_stems(stem_folder)
        else:
            print(f"⚠️ Stem folder doesn't exist at time of deletion: {stem_folder}")

        return (file_name, True, instruments)

    except Exception as e:
        return (file_name, False, str(e))

def process_all_unprocessed_songs():
    conn = sqlite3.connect(DB_PATH)
    unprocessed = [
        song_file.name
        for song_file in MP3_FOLDER.glob("*.mp3")
        if not is_song_already_processed(conn, song_file.name)
    ]
    conn.close()

    print(f"\n🎧 Found {len(unprocessed)} unprocessed songs.")

    if not unprocessed:
        return

    failed = []
    
    for file_name in tqdm(unprocessed, desc="Processing songs"):
        try:
            process_single_song(file_name)
        except Exception as e:
            failed.append((file_name, str(e)))

    if failed:
        print(f"\n❌ {len(failed)} tracks failed. Writing to failed_tracks.txt...")
        with open("failed_tracks.txt", "w") as f:
            for name, err in failed:
                f.write(f"{name}: {err}\n")
    else:
        print("\n🎉 All tracks processed successfully!")

if __name__ == "__main__":
    process_all_unprocessed_songs()