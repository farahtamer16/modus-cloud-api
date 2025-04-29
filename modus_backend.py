from flask import Flask, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded_configs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload_config', methods=['POST'])
def upload_config():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename != 'cloud_config.json':
        return jsonify({'error': 'Only cloud_config.json is allowed'}), 400

    save_path = os.path.join(UPLOAD_FOLDER, 'cloud_config.json')
    file.save(save_path)
    return jsonify({'message': 'Config uploaded successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
