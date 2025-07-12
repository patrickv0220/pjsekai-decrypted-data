import os
import requests
import json

# Servers and their URLs
LANGUAGES = {
    "JP": {
        "master": "https://sekai-world.github.io/sekai-master-db-diff/musics.json",
        "asset": "https://storage.sekai.best/sekai-jp-assets"
    },
    "EN": {
        "master": "https://sekai-world.github.io/sekai-master-db-en-diff/musics.json",
        "asset": "https://storage.sekai.best/sekai-en-assets"
    },
    "KR": {
        "master": "https://sekai-world.github.io/sekai-master-db-kr-diff/musics.json",
        "asset": "https://storage.sekai.best/sekai-kr-assets"
    },
    "ZHT": {
        "master": "https://sekai-world.github.io/sekai-master-db-tc-diff/musics.json",
        "asset": "https://storage.sekai.best/sekai-tc-assets"
    }
}

# Set the base download directory
DOWNLOAD_DIR = "pjsekai-decrypted-data-omg"

# Download file helper
def download_file(url, path):
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                f.write(response.content)
            print(f"✅ Downloaded: {path}")
        else:
            print(f"⚠️ Not found: {url}")
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")

# Go through each language
for lang, urls in LANGUAGES.items():
    print(f"\n🌐 Syncing {lang} assets...")
    try:
        response = requests.get(urls["master"], timeout=30)
        music_data = response.json()
    except Exception as e:
        print(f"❌ Failed to fetch master for {lang}: {e}")
        continue

    for song in music_data:
        song_id = song.get("id")
        jacket_id = song.get("assetbundleName")
        vocal_id = song.get("musicVocalAssetBundleName")

        if not jacket_id:
            print(f"⚠️ Skipping song {song_id} (no jacket ID)")
            continue
        if not vocal_id:
            print(f"⚠️ Skipping song {song_id} (no vocal ID)")
            continue

        # Download jacket
        download_file(
            f"{urls['asset']}/music/jacket/{jacket_id}/{jacket_id}.png",
            f"{DOWNLOAD_DIR}/{lang}/jacket/{jacket_id}.png"
        )

        # Download full song
        download_file(
            f"{urls['asset']}/music/long/{vocal_id}/{vocal_id}.mp3",
            f"{DOWNLOAD_DIR}/{lang}/long/{vocal_id}.mp3"
        )

        # Download short preview
        download_file(
            f"{urls['asset']}/music/short/{vocal_id}/{vocal_id}_short.mp3",
            f"{DOWNLOAD_DIR}/{lang}/short/{vocal_id}_short.mp3"
        )

        # Download chart (id_01)
        chart_folder = f"{str(song_id).zfill(4)}_01"
        download_file(
            f"{urls['asset']}/music/music_score/{chart_folder}/difficulty.txt",
            f"{DOWNLOAD_DIR}/{lang}/music_score/{chart_folder}/difficulty.txt"
        )