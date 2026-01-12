import json
import base64
import os

def encrypt_content():
    input_path = 'metadata.json'
    output_path = 'data.js'
    key = b'docuwatch'

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found")
        return

    # Read content
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix paths: games/ -> archives/
    # This avoids "games" keyword in URLs and matches the actual folder structure
    content = content.replace('"url": "games/', '"url": "archives/')
    # Also fix the game.html links if they exist in the content (though they shouldn't usually)
    content = content.replace('game.html', 'view.html')

    # Convert to bytes
    content_bytes = content.encode('utf-8')
    
    # XOR Encryption
    encrypted_bytes = bytearray()
    key_len = len(key)
    for i, b in enumerate(content_bytes):
        encrypted_bytes.append(b ^ key[i % key_len])

    # Base64 Encode
    encoded_data = base64.b64encode(encrypted_bytes).decode('utf-8')

    # Save as JS variable
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f'window.APP_DATA = "{encoded_data}";')

    print(f"Success: Encrypted content saved to {output_path}")

if __name__ == "__main__":
    encrypt_content()