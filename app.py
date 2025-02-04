import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
from google.cloud import storage
import requests
from flask import Flask, request, jsonify




app = Flask(__name__)
CORS(app)
#/etc/secrets/graceful-byway-449804-e2-02e24efd1eae.json
storage_client = storage.Client.from_service_account_json('graceful-byway-449804-e2-02e24efd1eae.json')
bucket_name = 'peermentorreview'


@app.route('/')
def index():
   # return send_from_directory(app.static_folder, 'index.html')
   return send_from_directory('.', 'index.html')


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        
        print("hi")
        data = request.form
        file = request.files['certificate']
        file = request.files.get('certificate')
        if file and file.filename:
         file_path = os.path.join('uploads', file.filename)
         file.save(file_path)
         bucket = storage_client.get_bucket(bucket_name)
         blob = bucket.blob(file.filename)
         blob.upload_from_filename(file_path)
         print("File uploaded successfully.")
         certificate_uploaded = 'Yes'
        else:
            print("No file uploaded.")
            certificate_uploaded = 'No'
        apps_script_url = 'https://script.google.com/macros/s/AKfycbyqvb3rYWm-crYZaOyk6B6Z2e62kN25XXC9ZlDzzHtAJNtNbJiRIGdxLPNwNJAgQ5majA/exec'
        response = requests.post(apps_script_url, json={
            'full_name': data['full_name'],
            'email': data['email'],
            'journal': data['journal'],
            'article': data['article'],
            'mentor': data['mentor'],
            'mentor_email': data['mentor_email'],
            'certificate_uploaded':certificate_uploaded ,
            
        },headers={'Content-Type': 'application/json'})
        print("Apps Script Response:", response.text)


        return jsonify({"message": "Submission successful", "apps_script_response": response.json()}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Submission failed"}), 500
    



if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)