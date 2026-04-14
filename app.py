import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__name__))
JSON_PATH = os.path.join(BASE_DIR, 'area_codes.json')

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    AREA_CODES_DB = json.load(f)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)