from flask import Blueprint, request, jsonify
from services.documentation import generate_documentation
import os

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({"error": "No files part"}), 400

    files = request.files.getlist('files')  # Get the list of uploaded files
    if not files:
        return jsonify({"error": "No files selected"}), 400

    docs = {}
    for file in files:
        if file.filename == '':
            continue
        try:
            content = file.read().decode('utf-8')  # Read and decode the file content
            docs[file.filename] = generate_documentation(content, file.filename)
        except Exception as e:
            docs[file.filename] = f"Error processing file: {str(e)}"

    return jsonify(docs)