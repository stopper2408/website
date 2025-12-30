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

def get_game_metadata(game_dir):
    index_path = os.path.join(game_dir, "index.html")
    title = None
    description = None
    image = None
    
    # Look for images
    possible_images = [
        "icon.png",
        "logo.png",
        "favicon.ico",
        "meta/apple-touch-icon.png",
        "img/logo.png",
        "images/logo.png"
    ]
    
    for img_path in possible_images:
        full_path = os.path.join(game_dir, img_path)
        if os.path.exists(full_path):
            # Use relative path for the image
            image = f"games/{os.path.basename(game_dir)}/{img_path}"
            break
    
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
                        # This might be an absolute URL, which is fine
                        image = img_match.group(1).strip()
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
                
                # Add to games list
                games_list.append({
                    "id": game_name,
                    "title": title,
                    "image": image,
                    "url": f"games/{game_name}/index.html",
                    "description": description,
                    "category": "Arcade"
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
