import requests
import os

SERVERS = {
    "JP": {
        "master": "https://sekai-world.github.io/sekai-master-db-diff",
        "assets": "https://storage.sekai.best/sekai-jp-assets"
    },
    "EN": {
        "master": "https://sekai-world.github.io/sekai-master-db-en-diff",
        "assets": "https://storage.sekai.best/sekai-en-assets"
    },
    "KR": {
        "master": "https://sekai-world.github.io/sekai-master-db-kr-diff",
        "assets": "https://storage.sekai.best/sekai-kr-assets"
    },
    "ZHT": {
        "master": "https://sekai-world.github.io/sekai-master-db-tc-diff",
        "assets": "https://storage.sekai.best/sekai-tc-assets"
    }
}

DOWNLOAD_DIR = "."  # Root of your repo folder (e.g., pjsekai-decrypted-data)

CHARTS = ["easy", "normal", "hard", "expert", "master"]

def fetch_json(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch: {url} — {e}")
        return []

def download_file(url, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(r.content)
            print(f"✅ Downloaded: {url}")
        else:
            print(f"⚠️ Not found: {url}")
    except Exception as e:
        print(f"❌ Error downloading {url} — {e}")

def process_server(code, config):
    print(f"\n🌐 Processing server: {code}")
    
    music = fetch_json(f"{config['master']}/music.json")
    vocals = fetch_json(f"{config['master']}/musicVocals.json")
    vocal_map = {v["id"]: v for v in vocals}

    for song in music:
        music_id = str(song["id"]).zfill(4)
        chart_id = f"{music_id}_01"
        vocal = vocal_map.get(song["id"])
        if not vocal:
            continue

        asset_name = song["assetbundleName"]
        vocal_bundle = vocal["assetbundleName"]

        base = f"{DOWNLOAD_DIR}/{code}"

        # Jacket (simplified path)
        jacket_url = f"{config['assets']}/music/jacket/{asset_name}/{asset_name}.png"
        jacket_path = f"{base}/jacket/{asset_name}/{asset_name}.png"
        download_file(jacket_url, jacket_path)

        # Full song
        full_url = f"{config['assets']}/music/long/{vocal_bundle}/{vocal_bundle}.mp3"
        full_path = f"{base}/long/{vocal_bundle}/{vocal_bundle}.mp3"
        download_file(full_url, full_path)

        # Preview
        preview_url = f"{config['assets']}/music/short/{vocal_bundle}/{vocal_bundle}_short.mp3"
        preview_path = f"{base}/short/{vocal_bundle}/{vocal_bundle}_short.mp3"
        download_file(preview_url, preview_path)

        # Charts
        for diff in CHARTS:
            chart_url = f"{config['assets']}/music/music_score/{chart_id}/{diff}.txt"
            chart_path = f"{base}/music_score/{chart_id}/{diff}.txt"
            download_file(chart_url, chart_path)

def main():
    for code, config in SERVERS.items():
        process_server(code, config)

if __name__ == "__main__":
    main()