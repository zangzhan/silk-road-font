import json
import os
import requests

DATA_FILE = 'data.json'
IMAGE_DIR = 'static/images'

def download_images():
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_data = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for item in data:
        image_url = item.get('image_url')
        if image_url and image_url.startswith('http'):
            try:
                print(f"Downloading image for ID {item['id']}: {image_url}")
                response = requests.get(image_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # Determine extension or default to .jpg
                ext = '.jpg'
                if 'png' in image_url.lower():
                    ext = '.png'
                elif 'jpeg' in image_url.lower():
                    ext = '.jpg'
                
                filename = f"{item['id']}{ext}"
                filepath = os.path.join(IMAGE_DIR, filename)
                
                with open(filepath, 'wb') as img_file:
                    img_file.write(response.content)
                
                # Update URL to local path
                item['image_url'] = f"/static/images/{filename}"
                print(f"Saved to {filepath}")
                
            except requests.RequestException as e:
                print(f"Failed to download image for ID {item['id']}: {e}")
                # Fallback to placeholder
                fallback_url = f"https://placehold.co/600x400?text={item['name']}"
                print(f"Downloading fallback: {fallback_url}")
                try:
                    response = requests.get(fallback_url, timeout=10)
                    response.raise_for_status()
                    filename = f"{item['id']}.jpg"
                    filepath = os.path.join(IMAGE_DIR, filename)
                    with open(filepath, 'wb') as img_file:
                        img_file.write(response.content)
                    item['image_url'] = f"/static/images/{filename}"
                    print(f"Saved fallback to {filepath}")
                except Exception as fallback_error:
                    print(f"Fallback failed too: {fallback_error}")
        
        updated_data.append(item)

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)
    
    print("Data.json updated with local image paths.")

if __name__ == "__main__":
    download_images()