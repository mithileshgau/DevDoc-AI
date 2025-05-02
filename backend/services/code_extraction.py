import os
import re
from .language_patterns import LANGUAGE_PATTERNS
from typing import Dict

def detect_language(file_name: str) -> str:
    """
    Detects the programming language based on file extension.
    """
    extension = os.path.splitext(file_name)[1].lower()
    for language, patterns in LANGUAGE_PATTERNS.items():
        lang_extensions = patterns["extension"]
        if isinstance(lang_extensions, list):
            if extension in lang_extensions:
                return language
        elif extension == lang_extensions:
            return language
    return "unknown"

def remove_comments(code: str, language: str) -> str:
    """
    Removes comments from the code based on language-specific patterns.
    """
    if language not in LANGUAGE_PATTERNS:
        return code
    comment_pattern = LANGUAGE_PATTERNS[language]["comment"]
    return re.sub(comment_pattern, "", code)

def extract_code_elements(code: str, language: str) -> Dict:
    """
    Extracts key elements from the code to use for verification.
    
    Args:
        code (str): Source code to analyze
        language (str): Programming language of the code
        
    Returns:
        Dict: Dictionary containing extracted code elements
    """
    if language not in LANGUAGE_PATTERNS:
        return {
            "functions": [],
            "classes": [],
            "imports": [],
            "globals": []
        }
    
    # Get language-specific patterns
    patterns = LANGUAGE_PATTERNS[language]
    
    # Remove comments before parsing
    clean_code = remove_comments(code, language)
    
    # Extract function definitions
    functions = []
    if language == "javascript":
        # Handle JavaScript's multiple function definition styles
        named_funcs = re.findall(r"function\s+(\w+)\s*\(([^)]*)\)", clean_code)
        arrow_funcs = re.findall(r"const\s+(\w+)\s*=\s*(?:\([^)]*\))?\s*=>", clean_code)
        object_funcs = re.findall(r"(\w+)\s*:\s*function\s*\(([^)]*)\)", clean_code)
        
        functions.extend(named_funcs)
        functions.extend([(name, "") for name in arrow_funcs])
        functions.extend(object_funcs)
    else:
        functions = re.findall(patterns["function"], clean_code)
        
        # Handle special cases for certain languages
        if isinstance(functions, list) and functions and isinstance(functions[0], tuple) and len(functions[0]) > 2:
            # Some regex patterns might produce more capture groups than needed
            functions = [(group[0], group[1]) if isinstance(group, tuple) and len(group) > 1 else (group, "") 
                          for group in functions]
    
    # Extract class definitions
    classes = re.findall(patterns["class"], clean_code)
    
    # Extract imports (language-specific)
    imports = []
    import_matches = re.findall(patterns["import"], clean_code)
    
    if language == "python":
        for imp in import_matches:
            if imp[0]:  # from X import Y
                modules = [x.strip() for x in imp[1].split(',')]
                for module in modules:
                    imports.append(f"{imp[0]}.{module}")
            else:  # import X
                modules = [x.strip() for x in imp[1].split(',')]
                imports.extend(modules)
    elif language == "go":
        for imp in import_matches:
            if imp[0]:  # multi-line import
                for line in imp[0].split('\n'):
                    line = line.strip().strip('"')
                    if line:
                        imports.append(line)
            elif imp[1]:  # single import
                imports.append(imp[1])
    else:
        # Generic import handling for other languages
        imports = [imp[0] if isinstance(imp, tuple) else imp for imp in import_matches]
    
    # Extract global variables and constants
    globals_list = []
    global_pattern = patterns["global"]
    
    for line in clean_code.split('\n'):
        match = re.match(global_pattern, line.strip())
        if match:
            globals_list.append(match.group(1))
    
    return {
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "globals": globals_list
    }