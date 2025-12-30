import os
import requests
import json

# Define the thumbnails directory
THUMBNAILS_DIR = "thumbnails"

# Ensure the directory exists
if not os.path.exists(THUMBNAILS_DIR):
    os.makedirs(THUMBNAILS_DIR)

# Map of Game IDs to verified Wikimedia URLs
SCREENSHOT_URLS = {
    "minecraft": "https://upload.wikimedia.org/wikipedia/en/1/17/Minecraft_explore_landscape.png",
    "2048": "https://upload.wikimedia.org/wikipedia/commons/f/f9/2048_win.png",
    "flappybird": "https://upload.wikimedia.org/wikipedia/en/5/52/Flappy_Bird_gameplay.png",
    "geometrydash": "https://upload.wikimedia.org/wikipedia/en/8/8d/Geometry_Dash_gameplay.PNG",
    "subway-surfers": "https://upload.wikimedia.org/wikipedia/en/b/b1/Subway_Surfers_gameplay.png",
    "tetris": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Typical_Tetris_Game.svg/288px-Typical_Tetris_Game.svg.png",
    "pacman": "https://upload.wikimedia.org/wikipedia/commons/c/c0/Pac-Man_gameplay_%281x_pixel-perfect_recreation%29.png",
    "chromedino": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Google_Dinosaur_game_dark_shading.png",
    # Add more here if found
}

def download_image(game_id, url):
    try:
        print(f"Downloading {game_id} from {url}...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Determine extension from URL or content-type
        ext = "png"
        if url.lower().endswith(".jpg") or url.lower().endswith(".jpeg"):
            ext = "jpg"
        elif url.lower().endswith(".svg"):
            ext = "svg"
        elif url.lower().endswith(".gif"):
            ext = "gif"
            
        filename = f"{game_id}.{ext}"
        filepath = os.path.join(THUMBNAILS_DIR, filename)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"Successfully saved to {filepath}")
        return filename
    except Exception as e:
        print(f"Failed to download {game_id}: {e}")
        return None

def update_games_json(downloaded_map):
    json_path = "games.json"
    if not os.path.exists(json_path):
        print("games.json not found!")
        return

    with open(json_path, 'r') as f:
        games = json.load(f)

    updated_count = 0
    for game in games:
        game_id = game.get('id')
        if game_id in downloaded_map:
            game['image'] = f"thumbnails/{downloaded_map[game_id]}"
            updated_count += 1

    with open(json_path, 'w') as f:
        json.dump(games, f, indent=4)
    
    print(f"Updated {updated_count} games in games.json")

def main():
    downloaded_files = {}
    
    for game_id, url in SCREENSHOT_URLS.items():
        filename = download_image(game_id, url)
        if filename:
            downloaded_files[game_id] = filename
            
    update_games_json(downloaded_files)

if __name__ == "__main__":
    main()
