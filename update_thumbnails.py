import json
import os
import requests
import urllib.parse

# Configuration
GAMES_JSON_PATH = 'metadata.json'
THUMBNAILS_DIR = 'thumbnails'
BG_COLOR = '1e293b' # Dark blue/slate from the screenshot
TEXT_COLOR = 'ffffff'
WIDTH = 600
HEIGHT = 400

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False

def main():
    ensure_dir(THUMBNAILS_DIR)
    
    with open(GAMES_JSON_PATH, 'r', encoding='utf-8') as f:
        games = json.load(f)
    
    updated_count = 0
    
    for game in games:
        game_id = game.get('id')
        title = game.get('title', game_id)
        
        # Clean title for URL
        # Remove special chars or long subtitles if needed
        clean_title = title.split('|')[0].strip() # Remove "| Play Free..."
        clean_title = clean_title.split('(')[0].strip() # Remove "(Clone)"
        
        # URL Encode
        encoded_title = urllib.parse.quote(clean_title)
        
        # Construct Placeholder URL
        # Using placehold.co as it supports text and colors
        image_url = f"https://placehold.co/{WIDTH}x{HEIGHT}/{BG_COLOR}/{TEXT_COLOR}/png?text={encoded_title}"
        
        filename = f"{game_id}.png"
        local_path = os.path.join(THUMBNAILS_DIR, filename)
        
        # Check if we should replace the image
        # We replace if:
        # 1. It's external
        # 2. It's a favicon (too small)
        # 3. It doesn't exist locally
        # 4. We want to enforce uniformity (User asked for "general images")
        
        print(f"Processing {title}...")
        
        # Download the generated image
        if download_image(image_url, local_path):
            # Update the game entry
            game['image'] = f"{THUMBNAILS_DIR}/{filename}"
            updated_count += 1
        else:
            print(f"Failed to generate thumbnail for {title}")

    # Save updated games.json
    with open(GAMES_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(games, f, indent=2)
        
    print(f"Finished! Updated {updated_count} games.")

if __name__ == "__main__":
    main()
