import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
from google.cloud import storage
import requests


# Initialize Flask
app = Flask(__name__)
CORS(app)
storage_client = storage.Client.from_service_account_json('/etc/secrets/graceful-byway-449804-e2-02e24efd1eae.json')
bucket_name = 'peermentorreview'

# Flask route to serve static index page
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')
from flask import Flask, request, jsonify
import os
from datetime import datetime
import sqlite3

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        
       
        data = request.form
        file = request.files['certificate']
        file = request.files.get('certificate')
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file.filename)
        blob.upload_from_filename(file_path)
        print("File uploaded successfully.")
        apps_script_url = 'https://script.google.com/macros/s/AKfycbz2G7xLJtcG647oYUyPtIEOwA6U4bv5CwFKU7Tm2E2exsvDD0Yd_eBWvPDRS3YWELJ0Ug/exec'
        response = requests.post(apps_script_url, json={
            'full_name': data['full_name'],
            'email': data['email'],
            'journal': data['journal'],
            'article': data['article'],
            'mentor': data['mentor'],
            'mentor_email': data['mentor_email'],
            'certificate_uploaded': 'Yes' if file else 'No',
            
        },headers={'Content-Type': 'application/json'})
        print("Apps Script Response:", response.text)


        return jsonify({"message": "Submission successful", "apps_script_response": response.json()}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Submission failed"}), 500
    

# Run Flask server

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)