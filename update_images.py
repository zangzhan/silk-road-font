import json
import os
import difflib

DATA_FILE = 'silk-road-font/data.json'
IMAGE_DIR = 'silk-road-font/static/images'

def update_image_paths():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return
    
    if not os.path.exists(IMAGE_DIR):
        print(f"Error: {IMAGE_DIR} not found.")
        return

    # Get list of files in image directory
    image_files = os.listdir(IMAGE_DIR)
    print(f"Found {len(image_files)} images in {IMAGE_DIR}")

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    for item in data:
        name = item['name']
        # Normalized name for matching (remove special chars if needed, but simple matching first)
        
        # Try exact match first (ignoring extension)
        match = None
        for img_file in image_files:
            if img_file.startswith('.'): continue # Skip hidden files
            
            base_name = os.path.splitext(img_file)[0]
            # Check if image filename is contained in item name or vice versa
            # e.g. "敦煌汉简" matches "敦煌汉简.jpg"
            if base_name == name or base_name in name or name in base_name:
                 match = img_file
                 break
        
        # If not found, try fuzzy matching
        if not match:
             # simple fuzzy check
             pass 

        if match:
            new_path = f"/static/images/{match}"
            if item.get('image_url') != new_path:
                item['image_url'] = new_path
                updated_count += 1
                print(f"Updated {name} -> {new_path}")
        else:
            print(f"No image found for: {name}")

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated_count} items in data.json.")

if __name__ == "__main__":
    update_image_paths()