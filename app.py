import json
import os
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__name__))
JSON_PATH = os.path.join(BASE_DIR, 'area_codes.json')

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    AREA_CODES_DB = json.load(f)
    
with open(os.path.join(BASE_DIR, 'kabupaten.json'), 'r', encoding='utf-8') as f:
    KABUPATEN_DB = json.load(f)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/lookup', methods=['GET'])
def lookup():
    code = request.args.get('code', '')
    
    clean_code = ''.join(filter(str.isdigit, code))
    
    if not clean_code:
        return jsonify({"success": False, "error": "Будь ласка, введіть коректний код."}), 400
        
    data = AREA_CODES_DB.get(clean_code)
    
    if data:
        return jsonify({"success": True, "data": data})
    else:
        return jsonify({"success": False, "error": f"Код {clean_code} не знайдено в базі."}), 404



@app.route('/api/indo', methods=['GET'])
def indo_lookup():
    query = request.args.get('q', '').lower().strip()
    
    if len(query) < 3:
        return jsonify({"success": False, "error": "Введіть хоча б 3 літери."}), 400

    results = []
    for name, data in KABUPATEN_DB.items():
        if query in name.lower():
            results.append({
                "name": name,
                "island": data["island"],
                "lat": data["lat"],
                "lon": data["lon"]
            })
            
    if results:
        return jsonify({"success": True, "data": results[0]})
    else:
        return jsonify({"success": False, "error": "Кабупатен не знайдено."}), 404


@app.route('/api/indo/random', methods=['GET'])
def indo_random():
    random_name = random.choice(list(KABUPATEN_DB.keys()))
    data = KABUPATEN_DB[random_name]
    
    return jsonify({
        "success": True, 
        "name": random_name, 
        "data": data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)