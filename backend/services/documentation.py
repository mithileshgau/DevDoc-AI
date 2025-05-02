import os
from google import genai
from google.genai import types
from .language_patterns import LANGUAGE_PATTERNS
from .code_extraction import detect_language, extract_code_elements, remove_comments
from .document_verification import verify_documentation

# Initialize Gemini client
api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)

def generate_documentation(code: str, file_name: str) -> str:
    """
    Generates high-quality documentation for the given code using Gemini API
    with hallucination mitigation techniques.
    
    Args:
        code (str): Source code to document.
        file_name (str): Name of the source file.
        
    Returns:
        str: Generated documentation in markdown format.
    """
    # Detect language based on file extension
    language = detect_language(file_name)
    
    if language == "unknown":
        language_prompt = "I couldn't determine the programming language from the file extension. Please analyze the code and identify the language before documenting it."
    else:
        language_prompt = f"The code is written in {language}."
    
    # Extract code elements for verification
    code_elements = extract_code_elements(code, language)
    
    # Load the structured documentation prompt
    prompt_template = load_prompt_template("documentation_prompt.txt")
    
    # Format function names for the prompt
    function_names = []
    for func in code_elements["functions"]:
        if isinstance(func, tuple) and len(func) > 0:
            function_names.append(func[0])
        elif isinstance(func, str):
            function_names.append(func)
    
    # Format the prompt with actual code, filename and extracted elements
    prompt = prompt_template.format(
        code=code, 
        file_name=file_name,
        language=language,
        language_prompt=language_prompt,
        functions=", ".join(function_names),
        classes=", ".join(code_elements["classes"]),
        imports=", ".join(code_elements["imports"]),
        globals=", ".join(code_elements["globals"])
    )
    
    # Call Gemini API
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # Use the appropriate model name
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,  # Lower temperature for more factual responses
            top_p=0.9,
            top_k=40
        )  
    )
    
    documentation = response.text
    
    # Verify the generated documentation
    is_valid, issues = verify_documentation(code_elements, documentation, language)
    
    # If issues found, try to fix them with a refinement prompt
    if not is_valid:
        refinement_template = load_prompt_template("refinement_prompt.txt")
        refinement_prompt = refinement_template.format(
            original_documentation=documentation,
            issues="\n".join([f"- {issue}" for issue in issues]),
            code=code,
            language=language
        )
        
        # Call Gemini API again for refinement
        refinement_response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=refinement_prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,  # Lower temperature for more factual responses
                top_p=0.9,
                top_k=40
            ) 
        )
        
        documentation = refinement_response.text
    
    # Add a disclaimer about potential hallucinations
    disclaimer = (
        "\n\n---\n\n*Note: This documentation was automatically generated and has been "
        "checked for accuracy against the source code. However, some interpretations "
        "of code functionality may require human review.*"
    )
    documentation += disclaimer
    
    return documentation

def load_prompt_template(template_name: str) -> str:
    """
    Loads a prompt template from the prompts directory.
    
    Args:
        template_name (str): Name of the template file without directory path
        
    Returns:
        str: The content of the prompt template
    """
    prompt_path = os.path.join("prompts", template_name)
    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()