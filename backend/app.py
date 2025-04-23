API_KEY = 'AIzaSyDnCQo6Hj9XchH5StMuPvop388EGgNosds'

from flask import Flask, request, jsonify
from flask_cors import CORS
import zipfile
import os
from google import genai

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")  # Allow requests from your React frontend

# Initialize the Gemini API client
client = genai.Client(api_key=API_KEY)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.zip'):
        # Save the uploaded ZIP file
        zip_path = os.path.join('uploads', file.filename)
        file.save(zip_path)

        # Extract the ZIP file
        extracted_files = extract_zip(zip_path)

        print(f"Extracted files: {extracted_files.keys()}")  # Debugging line
        # Generate documentation for each file
        docs = {}
        for file_name, file_content in extracted_files.items():
            # # print the file name and content for debugging
            # print(f"File: {file_name}")
            # print(f"Content: {file_content[:100]}...")
            docs[file_name] = generate_documentation(file_content)

        return jsonify(docs)

def extract_zip(zip_path):
    extracted_files = {}
    allowed_extensions = ('.py', '.js', '.ts', '.java', '.sql', '.json', '.yaml', '.yml', '.html', '.xml')

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith(allowed_extensions):
                with zip_ref.open(file_name) as file:
                    try:
                        content = file.read().decode('utf-8')
                        extracted_files[file_name] = content
                    except UnicodeDecodeError:
                        print(f"Skipping file (cannot decode): {file_name}")
            else:
                print(f"Skipping file (unsupported extension): {file_name}")
    
    return extracted_files

def generate_documentation(code):
    # Use Gemini API to generate documentation
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=f"""Generate comprehensive documentation for the following code. The documentation should follow a clean, technical format similar to official language or framework documentation. Organize the output into the following sections:

1. Title and Purpose – What the script/program/module does.
2. Global Variables / Constants / Configurations – List and explain each, including purpose and data type.
3. Event Handlers / Triggers (if applicable) – Describe any event-driven logic or listeners.
4. Function/Class Documentation – For each function or class, include:
   - Signature or definition
   - Description of its purpose
   - Input parameters and expected types
   - Return values (and types)
   - Key internal logic or algorithms (briefly)
5. Input/Output Data Format – Describe the format of files or data being read or produced.
6. Dependencies or Libraries Used – Mention any third-party tools or APIs required.
7. Features / Functional Highlights – Summarize the key capabilities the code enables.
8. Possible Improvements / Limitations – List any known issues, limitations, or areas for enhancement.

Format everything using clear section headers, bullet points, and code blocks where relevant. Keep the tone professional and concise. Avoid referencing the source file or language unless essential.

Code:
{code}
"""
)

    return response.text

if __name__ == '__main__':
    app.run(debug=True)
