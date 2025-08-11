import os
import time
import json
import sqlite3
import requests
from pathlib import Path
from tqdm import tqdm
from bs4 import BeautifulSoup

from database_methods import (
    create_tables,
    insert_track_metadata,
    insert_genre_if_missing,
    insert_track_genre_mapping,
)

# === CONFIG ===
DB_PATH = "backend/song_database_trial.db"
MP3_FOLDER = Path("mp3s")
MP3_FOLDER.mkdir(exist_ok=True)
GENRE_IDS = [3, 4, 9, 10, 12, 14, 17, 21]
BASE_URL = "https://freemusicarchive.org/music/charts/all"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# === DATABASE SETUP ===
conn = sqlite3.connect(DB_PATH)
create_tables(conn)

# === SCRAPING START ===
for genre_id in GENRE_IDS:
    url = f"{BASE_URL}?genre={genre_id}&sort=listens&pageSize=100"
    print(f"\n Scraping genre ID {genre_id}")
    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
    except Exception as e:
        print(f"Failed to load genre page {genre_id}: {e}")
        continue

    soup = BeautifulSoup(res.text, "html.parser")
    track_divs = soup.select("div.play-item")

    for track_div in tqdm(track_divs, desc=f"Genre {genre_id}"):
        raw_data = track_div.get("data-track-info")
        if not raw_data:
            continue

        try:
            track_info = json.loads(raw_data)
        except Exception as e:
            print("JSON parse error:", e)
            continue

        track_id = track_info.get("id")
        title = track_info.get("title")
        artist = track_info.get("artistName")
        album = track_info.get("albumTitle")
        file_url = track_info.get("fileUrl")
        file_name = track_info.get("fileName")
        download_url = track_info.get("downloadUrl")

        # Find the hyperlink and then we're pretty much good to go!

        print(f"Processing {title}")

        # Skip if already in DB
        cur = conn.cursor()
        cur.execute("SELECT id FROM tracks WHERE id = ?", (track_id,))
        if cur.fetchone():
            print(f"{title} already in database")
            continue

        # Listen count
        listen_tag = track_div.select_one(".chartcol-listens")
        listen_count = int(listen_tag.text.replace(",", "").strip()) if listen_tag else None

        # Insert into tracks
        try:
            insert_track_metadata(conn, (
                track_id, title, artist, album, listen_count,
                file_name, file_url, str(genre_id)
            ))
        except Exception as e:
            print(f"Failed to insert {file_name} into DB: {e}")
            continue

        # Insert genre mappings
        genre_links = track_div.select(".chartcol-genre a")
        for link in genre_links:
            genre_name = link.text.strip()
            genre_id_fk = insert_genre_if_missing(conn, genre_name)
            insert_track_genre_mapping(conn, track_id, genre_id_fk)

        # Download MP3
        mp3_path = MP3_FOLDER / file_name
        if not mp3_path.exists():
            try:
                with requests.get(file_url, headers=HEADERS, stream=True) as r:
                    r.raise_for_status()
                    with open(mp3_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                time.sleep(3)
            except Exception as e:
                print(f"⚠️ Download failed for {file_name}: {e}")
                continue

conn.close()
print("\n We're done scraping!")
