import os
import threading
import requests  # добавить импорт
from flask import Flask, jsonify, request, send_file, after_this_request
from flask_cors import CORS
import parser
import tempfile

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

products = []
products_lock = threading.Lock()

def set_products(new_products):
    global products
    with products_lock:
        products = new_products

def get_products():
    with products_lock:
        return products.copy()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/products', methods=['GET'])
def get_products_route():
    return jsonify(get_products())

@app.route('/api/load/url', methods=['POST'])
def load_from_url():
    try:
        html_bytes = parser.fetch_html_from_url(parser.DEFAULT_URL)
        new_products = parser.parse_html(html_bytes)
        set_products(new_products)
        return jsonify({'status': 'ok', 'count': len(new_products)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/load/html', methods=['POST'])
def load_from_html():
    if 'html_file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400
    file = request.files['html_file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400
    html_bytes = file.read()
    try:
        new_products = parser.parse_html(html_bytes)
        set_products(new_products)
        return jsonify({'status': 'ok', 'count': len(new_products)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/load/csv', methods=['POST'])
def load_from_csv():
    if 'csv_file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400
    file = request.files['csv_file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400
    encoding = request.form.get('encoding', 'utf-8-sig')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name
    try:
        new_products = parser.read_csv(tmp_path, encoding)
        set_products(new_products)
        return jsonify({'status': 'ok', 'count': len(new_products)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        os.unlink(tmp_path)

@app.route('/api/save/csv', methods=['POST'])
def save_csv():
    current_products = get_products()
    if not current_products:
        return jsonify({'status': 'error', 'message': 'No data to save'}), 400
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w', newline='', encoding='utf-8-sig') as tmp:
        parser.save_to_csv(current_products, tmp.name)
        tmp_path = tmp.name
    @after_this_request
    def cleanup(response):
        os.unlink(tmp_path)
        return response
    return send_file(tmp_path, as_attachment=True, download_name='products.csv', mimetype='text/csv')

@app.route('/api/products', methods=['DELETE'])
def clear_products():
    set_products([])
    return jsonify({'status': 'ok', 'count': 0})

@app.route('/api/create_bitrix_deal', methods=['POST'])
def create_bitrix_deal():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'status': 'error', 'message': 'No title provided'}), 400

    bitrix_url = "https://b24-uyue2c.bitrix24.ru/rest/1/di5nj5c3d2fovw60/crm.deal.add.json"
    payload = {
        "fields": {
            "TITLE": data['title'],
            "COMMENTS": data.get('link', ''),
            "OPPORTUNITY": data.get('price', 0),
            "CURRENCY_ID": "RUB"
        }
    }
    try:
        response = requests.post(bitrix_url, json=payload, timeout=10)
        response.raise_for_status()
        return jsonify({'status': 'ok', 'result': response.json()})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)