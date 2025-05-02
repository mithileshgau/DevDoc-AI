from flask import Blueprint, request, jsonify, current_app
import os
from services.extractor import extract_zip
from services.documentation import generate_documentation
import concurrent.futures

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.zip'):
        zip_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(zip_path)

        extracted_files = extract_zip(zip_path)

        docs = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_file = {
                executor.submit(generate_documentation, content, fname): fname
                for fname, content in extracted_files.items()
            }
            for future in concurrent.futures.as_completed(future_to_file):
                docs[future_to_file[future]] = future.result()

        os.remove(zip_path)
        return jsonify(docs)
