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
        "Puzzle": ["2048", "hextris", "tetris", "puzzle", "logic", "sudoku", "connect", "brain", "maze", "factory"],
        "Action": ["shooter", "fps", "gun", "fight", "battle", "asteroids", "run", "jump", "platformer", "survival", "tank", "war", "glitch", "underrun", "geometry", "slope", "tunnel"],
        "Strategy": ["tower", "defense", "strategy", "civilization", "empire", "kingdom", "idle", "clicker", "manage", "trimps", "sim"],
        "Sports": ["soccer", "football", "basketball", "tennis", "golf", "sport", "race", "racing", "drift", "surf"],
        "Arcade": ["arcade", "retro", "classic", "pacman", "snake", "breakout", "space", "invaders", "dino"]
    }
    
    for cat, keywords in categories.items():
        for keyword in keywords:
            if keyword in combined:
                return cat
                
    return "Arcade" # Default

def clean_title(title):
    # Remove version numbers
    title = re.sub(r'\sv?\d+(\.\d+)*', '', title)
    # Remove "Javascript" or "JS" prefixes/suffixes
    title = re.sub(r'javascript', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\bjs\b', '', title, flags=re.IGNORECASE)
    # Fix HTML entities
    title = title.replace("&ndash;", "-").replace("&amp;", "&")
    # Remove file extensions
    title = title.replace(".exe", "").replace(".html", "")
    # Clean whitespace
    return title.strip()

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
        image = f"archives/{os.path.basename(game_dir)}/{found_image_path}".replace("\\", "/")

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
                             image = f"archives/{os.path.basename(game_dir)}/{img_url}".replace("\\", "/")
                        else:
                             image = img_url
        except Exception:
            pass
            
    return title, description, image

def download_repo_as_game(repo_url, game_id, target_dir, branch="main"):
    print(f"Downloading {game_id} from {repo_url}...")
    zip_url = f"{repo_url}/archive/refs/heads/{branch}.zip"
    
    try:
        r = requests.get(zip_url)
        if r.status_code != 200:
            # Try master if main fails
            zip_url = f"{repo_url}/archive/refs/heads/master.zip"
            r = requests.get(zip_url)
            
        if r.status_code == 200:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            extract_path = f"temp_{game_id}"
            z.extractall(extract_path)
            
            # Find the root folder (usually repo-branch)
            root_folder = os.listdir(extract_path)[0]
            source_path = os.path.join(extract_path, root_folder)
            
            target_game_path = os.path.join(target_dir, game_id)
            if os.path.exists(target_game_path):
                shutil.rmtree(target_game_path)
            
            shutil.copytree(source_path, target_game_path)
            shutil.rmtree(extract_path)
            
            # Get metadata
            extracted_title, extracted_desc, extracted_image = get_game_metadata(target_game_path)
            
            title = extracted_title if extracted_title else game_id.replace("-", " ").title()
            description = extracted_desc if extracted_desc else f"Play {title} now!"
            image = extracted_image if extracted_image else "https://placehold.co/300x200/1e293b/3b82f6?text=" + game_id
            category = get_game_category(title, description)
            
            return {
                "id": game_id,
                "title": title,
                "image": image,
                "url": f"archives/{game_id}/index.html",
                "description": description,
                "category": category
            }
        else:
            print(f"Failed to download {game_id}: Status {r.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading {game_id}: {e}")
        return None

def setup_games(source_dir, target_dir):
    html5_source = os.path.join(source_dir, "gfiles", "html5")
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    games_list = []
    
    # Games to exclude (broken, obscure, or bad quality)
    BLOCKLIST = [
        "themazeofspacegoblins", "xx142-b2exe", "konnekt", "q1k3", 
        "shuttledeck", "ninjavsevilcorp", "edgenotfound", "sleepingbeauty",
        "backcountry", "astray", "asciispace", "retrohaunt", "pushback",
        "roadblocks", "spacegarden", "spacehuggers", "towermaster"
    ]
    
    # Manual title overrides
    TITLE_OVERRIDES = {
        "chromedino": "Dino Run",
        "pacman": "Pac-Man",
        "tetris": "Tetris",
        "breakout": "Breakout",
        "racer": "Racer",
        "minecraft": "Minecraft (Clone)",
        "trimps": "Trimps",
        "cookieclicker": "Cookie Clicker",
        "2048": "2048",
        "hextris": "Hextris"
    }

    print("Processing HTML5 games...")
    if os.path.exists(html5_source):
        for game_name in os.listdir(html5_source):
            if game_name in BLOCKLIST:
                print(f"Skipping blocked game: {game_name}")
                continue
                
            game_source_path = os.path.join(html5_source, game_name)
            if os.path.isdir(game_source_path):
                target_game_path = os.path.join(target_dir, game_name)
                
                # Check for index.html
                index_file = os.path.join(game_source_path, "index.html")
                if not os.path.exists(index_file):
                    print(f"Skipping {game_name}: No index.html")
                    continue
                    
                # Check file size (skip empty/tiny files)
                if os.path.getsize(index_file) < 100:
                    print(f"Skipping {game_name}: index.html too small")
                    continue

                # Copy game files
                if os.path.exists(target_game_path):
                    shutil.rmtree(target_game_path)
                shutil.copytree(game_source_path, target_game_path)
                print(f"Copied {game_name}")
                
                # Get metadata
                extracted_title, extracted_desc, extracted_image = get_game_metadata(target_game_path)
                
                # Determine title
                if game_name in TITLE_OVERRIDES:
                    title = TITLE_OVERRIDES[game_name]
                elif extracted_title:
                    title = clean_title(extracted_title)
                else:
                    title = game_name.replace("-", " ").title()
                
                description = extracted_desc if extracted_desc else f"Play {title} now!"
                image = extracted_image if extracted_image else "https://placehold.co/300x200/1e293b/3b82f6?text=" + game_name
                
                category = get_game_category(title, description)
                
                # Add to games list
                games_list.append({
                    "id": game_name,
                    "title": title,
                    "image": image,
                    "url": f"archives/{game_name}/index.html",
                    "description": description,
                    "category": category
                })
    
    # Download extra games
    extra_games = [
        ("https://github.com/mcalec-dev/slope-game", "slope"),
        ("https://github.com/gameshaxor/SubwaySurfers", "subway-surfers")
    ]
    
    for repo, gid in extra_games:
        game_data = download_repo_as_game(repo, gid, target_dir)
        if game_data:
            games_list.append(game_data)
            print(f"Added extra game: {gid}")
    
    return games_list

def main():
    base_dir = os.getcwd()
    games_dir = os.path.join(base_dir, "archives")
    
    try:
        repo_path = download_and_extract_repo()
        
        games_data = setup_games(repo_path, games_dir)
        
        # Save content.json
        with open("content.json", "w") as f:
            json.dump(games_data, f, indent=2)

        # Save content_data.js
        with open("content_data.js", "w", encoding="utf-8") as f:
            f.write("window.GAMES_DATA = " + json.dumps(games_data, indent=4) + ";\n")
            
        print(f"Successfully processed {len(games_data)} games.")
        print("Updated content.json and content_data.js")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        if os.path.exists("temp_repo"):
            shutil.rmtree("temp_repo")

if __name__ == "__main__":
    main()
