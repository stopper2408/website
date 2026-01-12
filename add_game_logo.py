import json
import shutil
import os
import sys

def add_game_logo():
    # Configuration
    GAMES_JSON_PATH = 'metadata.json'
    THUMBNAILS_DIR = 'thumbnails'

    # Ensure thumbnails directory exists
    if not os.path.exists(THUMBNAILS_DIR):
        os.makedirs(THUMBNAILS_DIR)

    # 1. Get Game ID
    game_id = input("Enter the Game ID (e.g., 'subway-surfers'): ").strip()
    if not game_id:
        print("Game ID cannot be empty.")
        return

    # 2. Load games.json to check if game exists
    try:
        with open(GAMES_JSON_PATH, 'r', encoding='utf-8') as f:
            games_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {GAMES_JSON_PATH} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Failed to decode {GAMES_JSON_PATH}.")
        return

    # Find the game entry
    game_entry = next((g for g in games_data if g['id'] == game_id), None)

    if not game_entry:
        print(f"Warning: Game ID '{game_id}' not found in {GAMES_JSON_PATH}.")
        create_new = input("Do you want to continue and just copy the image? (y/n): ").lower()
        if create_new != 'y':
            return
    else:
        print(f"Found game: {game_entry.get('title', 'Unknown Title')}")

    # 3. Get Source Image Path
    source_path = input("Enter the path to the PNG image: ").strip()
    
    # Remove quotes if user dragged and dropped file
    if source_path.startswith('"') and source_path.endswith('"'):
        source_path = source_path[1:-1]
    
    if not os.path.exists(source_path):
        print(f"Error: File not found at {source_path}")
        return
    
    if not source_path.lower().endswith('.png'):
        print("Warning: The source file does not appear to be a PNG.")
        confirm = input("Continue anyway? (y/n): ").lower()
        if confirm != 'y':
            return

    # 4. Copy the image
    dest_filename = f"{game_id}.png"
    dest_path = os.path.join(THUMBNAILS_DIR, dest_filename)
    
    try:
        shutil.copy2(source_path, dest_path)
        print(f"Success: Image copied to {dest_path}")
    except Exception as e:
        print(f"Error copying file: {e}")
        return

    # 5. Update games.json if game exists
    if game_entry:
        # Relative path for web use (forward slashes)
        web_image_path = f"{THUMBNAILS_DIR}/{dest_filename}"
        
        if game_entry.get('image') == web_image_path:
            print("games.json already has the correct image path.")
        else:
            game_entry['image'] = web_image_path
            try:
                with open(GAMES_JSON_PATH, 'w', encoding='utf-8') as f:
                    json.dump(games_data, f, indent=4)
                print(f"Success: Updated {GAMES_JSON_PATH} with new image path.")
            except Exception as e:
                print(f"Error updating {GAMES_JSON_PATH}: {e}")

if __name__ == "__main__":
    add_game_logo()
