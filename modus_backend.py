from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

# Path to Firebase Hosting project folder inside Render container
FIREBASE_PROJECT_PATH = '/opt/render/project/src'  # default for Render
UPLOAD_FOLDER = os.path.join(FIREBASE_PROJECT_PATH, 'public')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload_config', methods=['POST'])
def upload_config():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename != 'cloud_config.json':
        return jsonify({'error': 'Only cloud_config.json is allowed'}), 400

    save_path = os.path.join(UPLOAD_FOLDER, 'cloud_config.json')
    try:
        file.save(save_path)
        print(f"[INFO] File saved to {save_path}")
    except Exception as e:
        return jsonify({'error': f'Failed to save file: {e}'}), 500

    try:
        firebase_token = os.getenv("FIREBASE_TOKEN")
        if not firebase_token:
            return jsonify({'error': 'FIREBASE_TOKEN is not set in environment'}), 500

        result = subprocess.run(
            ["firebase", "deploy", "--only", "hosting", "--token", firebase_token],
            cwd=FIREBASE_PROJECT_PATH,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("[INFO] Firebase deploy successful.")
            return jsonify({'message': 'Deployed to Firebase successfully'}), 200
        else:
            print("[ERROR] Firebase deploy failed:", result.stderr)
            return jsonify({'error': 'Deploy failed', 'details': result.stderr}), 500

    except Exception as e:
        return jsonify({'error': f'Failed to deploy: {e}'}), 500
