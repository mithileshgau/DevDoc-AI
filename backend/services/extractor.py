import zipfile

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
                        continue
    return extracted_files
