import requests
import os
import time

# Config
SERVER_CONFIGS = {
    "JP": {
        "music_url": "https://sekai-world.github.io/sekai-master-db-diff/musics.json",
        "vocals_url": "https://sekai-world.github.io/sekai-master-db-diff/musicVocals.json",
        "asset_base": "https://storage.sekai.best/sekai-jp-assets",
    },
    "EN": {
        "music_url": "https://sekai-world.github.io/sekai-master-db-en-diff/musics.json",
        "vocals_url": "https://sekai-world.github.io/sekai-master-db-en-diff/musicVocals.json",
        "asset_base": "https://storage.sekai.best/sekai-en-assets",
    },
    "KR": {
        "music_url": "https://sekai-world.github.io/sekai-master-db-kr-diff/musics.json",
        "vocals_url": "https://sekai-world.github.io/sekai-master-db-kr-diff/musicVocals.json",
        "asset_base": "https://storage.sekai.best/sekai-kr-assets",
    },
    "ZHT": {
        "music_url": "https://sekai-world.github.io/sekai-master-db-tc-diff/musics.json",
        "vocals_url": "https://sekai-world.github.io/sekai-master-db-tc-diff/musicVocals.json",
        "asset_base": "https://storage.sekai.best/sekai-tc-assets",
    },
}

DOWNLOAD_DIR = "pjsekai-decrypted-data-omg"

def download_file(url, path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                f.write(response.content)
            print(f"✅ Downloaded: {path}")
        else:
            print(f"⚠️ Failed to download {url} ({response.status_code})")
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")

for server, config in SERVER_CONFIGS.items():
    print(f"\n📦 Processing server: {server}")

    try:
        music_data = requests.get(config["music_url"]).json()
        vocals_data = requests.get(config["vocals_url"]).json()
    except Exception as e:
        print(f"❌ Failed to fetch data for {server}: {e}")
        continue

    vocal_map = {v["id"]: v.get("assetbundleName") for v in vocals_data if "id" in v}

    for song in music_data:
        song_id = str(song.get("id", "")).zfill(4)
        jacket_id = song.get("assetbundleName")
        vocal_id = vocal_map.get(song.get("id"))

        if not jacket_id or not vocal_id:
            print(f"⚠️ Skipping song {song_id} (missing jacket or vocal ID)")
            continue

        # Jacket
        jacket_url = f"{config['asset_base']}/music/jacket/{jacket_id}/{jacket_id}.png"
        jacket_path = f"{DOWNLOAD_DIR}/{server}/jacket/{jacket_id}.png"
        download_file(jacket_url, jacket_path)

        # Long song
        long_url = f"{config['asset_base']}/music/long/{vocal_id}/{vocal_id}.mp3"
        long_path = f"{DOWNLOAD_DIR}/{server}/long/{vocal_id}.mp3"
        download_file(long_url, long_path)

        # Short preview
        short_url = f"{config['asset_base']}/music/short/{vocal_id}/{vocal_id}_short.mp3"
        short_path = f"{DOWNLOAD_DIR}/{server}/short/{vocal_id}_short.mp3"
        download_file(short_url, short_path)

        # Charts
        chart_folder = song_id + "_01"
        difficulties = ["easy", "normal", "hard", "expert", "master", "append"]
        for diff in difficulties:
            chart_url = f"{config['asset_base']}/music/music_score/{chart_folder}/{diff}.txt"
            chart_path = f"{DOWNLOAD_DIR}/{server}/music_score/{chart_folder}/{diff}.txt"
            download_file(chart_url, chart_path)

        time.sleep(0.5)  # Be nice to the server

print("\n✨ Done downloading all available assets!")