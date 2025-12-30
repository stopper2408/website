import os
import json
import requests
import zipfile
import shutil
import io
import re

def download_and_extract_repo():
    url = "https://github.com/BinBashBanana/gfiles/archive/refs/heads/master.zip"
    print(f"Downloading repo from {url}...")
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    
    print("Extracting zip...")
    z.extractall("temp_repo")
    
    return "temp_repo/gfiles-master"

def get_game_category(title, description):
    title_lower = title.lower()
    desc_lower = description.lower() if description else ""
    combined = title_lower + " " + desc_lower
    
    categories = {
        "Puzzle": ["2048", "hextris", "tetris", "puzzle", "logic", "sudoku", "connect", "brain"],
        "Action": ["shooter", "fps", "gun", "fight", "battle", "asteroids", "run", "jump", "platformer", "survival", "tank", "war"],
        "Strategy": ["tower", "defense", "strategy", "civilization", "empire", "kingdom", "idle", "clicker", "manage"],
        "Sports": ["soccer", "football", "basketball", "tennis", "golf", "sport", "race", "racing", "drift"],
        "Arcade": ["arcade", "retro", "classic", "pacman", "snake", "breakout", "space", "invaders"]
    }
    
    for cat, keywords in categories.items():
        for keyword in keywords:
            if keyword in combined:
                return cat
                
    return "Arcade" # Default

def get_game_metadata(game_dir):
    index_path = os.path.join(game_dir, "index.html")
    title = None
    description = None
    image = None
    
    # Look for images (prioritize screenshots/thumbnails)
    possible_images = [
        "thumbnail.png", "thumbnail.jpg",
        "cover.png", "cover.jpg",
        "screenshot.png", "screenshot.jpg",
        "preview.png", "preview.jpg",
        "logo.png", "logo.jpg",
        "icon.png", "icon.jpg",
        "favicon.ico",
        "meta/apple-touch-icon.png",
        "img/logo.png",
        "images/logo.png",
        "media/logo.png"
    ]
    
    # Search recursively for images if not found in root
    found_image_path = None
    
    # First check root and specific subdirs
    for img_path in possible_images:
        full_path = os.path.join(game_dir, img_path)
        if os.path.exists(full_path):
            found_image_path = img_path
            break
            
    # If still not found, try to find ANY png/jpg in the folder (risky but better than nothing)
    if not found_image_path:
        for root, dirs, files in os.walk(game_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')) and 'icon' in file.lower():
                    rel_path = os.path.relpath(os.path.join(root, file), game_dir)
                    found_image_path = rel_path
                    break
            if found_image_path: break

    if found_image_path:
        # Normalize path separators to forward slashes for URL
        image = f"games/{os.path.basename(game_dir)}/{found_image_path}".replace("\\", "/")

    if os.path.exists(index_path):
        try:
            with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
                # Extract title
                title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip()
                    
                # Extract description
                desc_match = re.search(r'<meta\s+(?:name|property)=["\'](?:og:)?description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
                if desc_match:
                    description = desc_match.group(1).strip()
                    
                # Extract image from meta if not found locally
                if not image:
                    img_match = re.search(r'<meta\s+(?:name|property)=["\'](?:og:)?image["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
                    if img_match:
                        img_url = img_match.group(1).strip()
                        if not img_url.startswith("http"):
                             # It's a relative path, construct it
                             image = f"games/{os.path.basename(game_dir)}/{img_url}".replace("\\", "/")
                        else:
                             image = img_url
        except Exception:
            pass
            
    return title, description, image

def setup_games(source_dir, target_dir):
    html5_source = os.path.join(source_dir, "gfiles", "html5")
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    games_list = []
    
    print("Processing HTML5 games...")
    if os.path.exists(html5_source):
        for game_name in os.listdir(html5_source):
            game_source_path = os.path.join(html5_source, game_name)
            if os.path.isdir(game_source_path):
                target_game_path = os.path.join(target_dir, game_name)
                
                # Copy game files
                if os.path.exists(target_game_path):
                    shutil.rmtree(target_game_path)
                shutil.copytree(game_source_path, target_game_path)
                print(f"Copied {game_name}")
                
                # Get metadata
                extracted_title, extracted_desc, extracted_image = get_game_metadata(target_game_path)
                
                title = extracted_title if extracted_title else game_name.replace("-", " ").title()
                description = extracted_desc if extracted_desc else f"Play {title} now!"
                image = extracted_image if extracted_image else "https://placehold.co/300x200/1e293b/3b82f6?text=" + game_name
                
                category = get_game_category(title, description)
                
                # Add to games list
                games_list.append({
                    "id": game_name,
                    "title": title,
                    "image": image,
                    "url": f"games/{game_name}/index.html",
                    "description": description,
                    "category": category
                })
    
    return games_list

def main():
    base_dir = os.getcwd()
    games_dir = os.path.join(base_dir, "games")
    
    try:
        repo_path = download_and_extract_repo()
        
        games_data = setup_games(repo_path, games_dir)
        
        # Save games.json
        with open("games.json", "w") as f:
            json.dump(games_data, f, indent=2)
            
        print(f"Successfully processed {len(games_data)} games.")
        print("Updated games.json")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        if os.path.exists("temp_repo"):
            shutil.rmtree("temp_repo")

if __name__ == "__main__":
    main()
