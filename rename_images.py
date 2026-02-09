import json
import os

DATA_FILE = 'silk-road-font/data.json'
IMAGE_DIR = 'silk-road-font/static/images'

# Mapping: Chinese Name (from data.json 'name' field) -> New English Filename
NAME_MAP = {
    "武威仪礼简": "wuwei_ritual_slips.jpg",
    "武威汉代医简": "wuwei_medical_slips.jpeg",
    "王杖诏书令简": "wangzhang_edict_slips.jpeg",
    "居延汉简": "juyan_han_slips.jpg",
    "敦煌汉简": "dunhuang_han_slips.jpg",
    "楼兰残简": "loulan_fragments.jpg",
    "尼雅佉卢文木牍": "niya_kharosthi_wood.jpg",
    "长沙走马楼吴简": "changsha_zoumalou_wu_slips.jpg",
    "吐鲁番出土文书": "turpan_documents.jpg",
    "甘谷汉简": "gangu_han_slips.jpg",
    "敦煌遗书（写经体）": "dunhuang_manuscripts.jpg",
    "悬泉置汉简": "xuanquanzhi_han_slips.jpg"
}

def rename_and_update():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Rename files in static/images
    if os.path.exists(IMAGE_DIR):
        files = os.listdir(IMAGE_DIR)
        for filename in files:
            # Check if file contains any of the Chinese names
            for cn_name, en_name in NAME_MAP.items():
                if cn_name in filename:
                    old_path = os.path.join(IMAGE_DIR, filename)
                    new_path = os.path.join(IMAGE_DIR, en_name)
                    
                    try:
                        os.rename(old_path, new_path)
                        print(f"Renamed: {filename} -> {en_name}")
                    except OSError as e:
                        print(f"Error renaming {filename}: {e}")
                    break

    # 2. Update data.json
    updated_count = 0
    for item in data:
        name = item['name']
        if name in NAME_MAP:
            new_filename = NAME_MAP[name]
            new_url = f"/static/images/{new_filename}"
            if item.get('image_url') != new_url:
                item['image_url'] = new_url
                updated_count += 1
                print(f"Updated JSON for {name}: {new_url}")

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated_count} items in data.json.")

if __name__ == "__main__":
    rename_and_update()