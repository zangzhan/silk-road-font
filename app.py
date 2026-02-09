from flask import Flask, jsonify, request, render_template
import json
import os
import re

app = Flask(__name__)

def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_text(text):
    if not text:
        return ""
    # Remove whitespace and punctuation/symbols including Chinese ones like 《》
    # keeping alphanumeric and Chinese characters
    return re.sub(r'[^\w\u4e00-\u9fa5]', '', text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fonts', methods=['GET'])
def get_fonts():
    data = load_data()
    query = request.args.get('q')
    
    if query:
        normalized_query = normalize_text(query)
        if normalized_query:
            filtered_data = []
            for item in data:
                # Search in name, site, description, and academic_value
                searchable_text = (
                    item.get('name', '') + 
                    item.get('site', '') + 
                    item.get('description', '') + 
                    item.get('research_hotspot', '') + 
                    item.get('category', '')
                )
                if normalized_query in normalize_text(searchable_text):
                    filtered_data.append(item)
            return jsonify(filtered_data)
            
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)