from .documentation import generate_documentation

def main():
    # Example usage
    file_name = "example.py"
    with open(file_name, "r", encoding="utf-8") as file:
        code = file.read()
    
    documentation = generate_documentation(code, file_name)
    print(documentation)