import json
import os

DATA_FILE = 'silk-road-font/data.json'

# The 10 specified cases (including the existing one for reference/update)
new_cases = [
    {
        "id": 4, # Continuing from existing 3
        "name": "居延汉简",
        "dynasty": "西汉-东汉",
        "origin": "内蒙古额济纳旗居延遗址",
        "category": "行政/军事",
        "description": "汉代隶书的“标准库”，包含大量公文书、簿籍，展现了隶书由秦隶向汉隶的演变。数量巨大，内容涉及屯戍边防、烽火制度及日常生活。",
        "research_hotspot": "汉代边塞防御体系、简牍隶书的书法演变规律、汉代社会经济史料挖掘。",
        "image_url": "/static/images/placeholder.jpg"
    },
    {
        "id": 5,
        "name": "敦煌汉简",
        "dynasty": "西汉-东汉",
        "origin": "甘肃敦煌阳关、玉门关及沿线烽燧",
        "category": "军事/行政",
        "description": "记录了丝路边防屯戍生活，其中的“屯戍丛帖”是研究草隶（章草雏形）的关键。内容极其丰富，被誉为“汉代边塞百科全书”。",
        "research_hotspot": "汉代邮驿制度、章草书法的形成与发展、丝绸之路早期交通与贸易。",
        "image_url": "/static/images/placeholder.jpg"
    },
    {
        "id": 6,
        "name": "楼兰残简",
        "dynasty": "魏晋",
        "origin": "新疆罗布泊楼兰古城遗址",
        "category": "文书/信札",
        "description": "展现了从隶书向楷书、行书过渡的形态，是书法史上“魏晋风度”的先声。其中《李柏文书》是行书早期的杰出代表。",
        "research_hotspot": "魏晋书法流变、楼兰古国的兴衰历史、魏晋时期西域的屯田与治理。",
        "image_url": "/static/images/placeholder.jpg"
    },
    {
        "id": 7,
        "name": "尼雅佉卢文木牍",
        "dynasty": "汉晋",
        "origin": "新疆民丰县尼雅遗址（精绝国）",
        "category": "法律/经济",
        "description": "记录了丝路南道的古老语言，是研究西域三十六国法律、经济的唯一文字证据。字体为佉卢文，内容涉及买卖、契约、诉讼等。",
        "research_hotspot": "丝绸之路语言交流、精绝国社会结构、中亚文化与汉文化的融合。",
        "image_url": "/static/images/placeholder.jpg"
    },
    {
        "id": 8,
        "name": "长沙走马楼吴简",
        "dynasty": "三国（孙吴）",
        "origin": "湖南长沙走马楼",
        "category": "行政/赋税",
        "description": "虽非核心丝路出土，但其行草书体对研究丝路文书的标准化具有极高对比价值。数量庞大，主要为孙吴时期的司法文书和赋税名籍。",
        "research_hotspot": "孙吴时期的户籍赋税制度、楷书与行草的并行发展、简牍形制与文书行政。",
        "image_url": "/static/images/placeholder.jpg"
    },
    {
        "id": 9,
        "name": "吐鲁番出土文书",
        "dynasty": "晋-唐",
        "origin": "新疆吐鲁番阿斯塔那古墓群等",
        "category": "经籍/文书",
        "description": "包含大量《论语》、《诗经》残卷，展现了唐代楷书在西域的极高普及度。记录了唐代西域的政治、经济、军事及宗教活动。",
        "research_hotspot": "唐代西域治理模式、儒家经典在西域的传播、唐代楷书的标准化与艺术特色。",
        "image_url": "/static/images/placeholder.jpg"
    },
    {
        "id": 10,
        "name": "甘谷汉简",
        "dynasty": "东汉",
        "origin": "甘肃甘谷县",
        "category": "诏书",
        "description": "内容为汉代中央下发给基层的“诏书”，字体法度严谨，是典型的官式隶书。字形扁平，波磔分明，具有极高的庙堂气象。",
        "research_hotspot": "汉代诏书发布流程、标准隶书（八分书）的艺术特征、汉代中央与地方的行政关系。",
        "image_url": "/static/images/placeholder.jpg"
    },
    {
        "id": 11,
        "name": "敦煌遗书（写经体）",
        "dynasty": "唐-宋",
        "origin": "甘肃敦煌莫高窟藏经洞",
        "category": "宗教/经籍",
        "description": "世界公认的中国书法艺术宝库，包含大量成熟的经生体楷书。这些写经书法结构严谨、笔法纯熟，对后世书法影响深远。",
        "research_hotspot": "敦煌写经的书法艺术风格、佛教经典的版本学研究、古代造纸与装帧技术。",
        "image_url": "/static/images/placeholder.jpg"
    },
    {
        "id": 12,
        "name": "悬泉置汉简",
        "dynasty": "西汉-东汉",
        "origin": "甘肃敦煌悬泉置遗址",
        "category": "外交/驿站",
        "description": "专门记录外交接待的档案，包含康居、大月氏等国来使记录，是“活的丝路史”。详细记载了驿站的接待规格、消耗物资及往来人员。",
        "research_hotspot": "汉代丝绸之路外交制度、悬泉置驿站的运作机制、中西文化交流实证。",
        "image_url": "/static/images/placeholder.jpg"
    },
    # ID 10 in user list is Wuwei Medical Slips, which already exists as ID 2. 
    # We will verify existing data and not duplicate if name matches.
]

def expand_data():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)

    # Create a map of existing names to avoid duplicates
    existing_names = {item['name']: item for item in existing_data}
    
    # Find the max ID to continue numbering correctly
    max_id = 0
    if existing_data:
        max_id = max(item['id'] for item in existing_data)

    added_count = 0
    for case in new_cases:
        if case['name'] in existing_names:
            print(f"Skipping existing case: {case['name']}")
            continue
        
        # Assign new ID
        max_id += 1
        case['id'] = max_id
        existing_data.append(case)
        added_count += 1
        print(f"Added new case: {case['name']} (ID: {max_id})")

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully added {added_count} new cases to data.json.")

if __name__ == "__main__":
    expand_data()