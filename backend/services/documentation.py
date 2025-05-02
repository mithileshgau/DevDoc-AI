import os
from google import genai

# Initialize Gemini client
# get the API key .env file
api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)

def load_prompt_template() -> str:
    """
    Loads the structured documentation prompt from a file.
    """
    prompt_path = os.path.join("prompts", "documentation_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()

def generate_documentation(code: str, file_name: str) -> str:
    """
    Generates high-quality documentation for the given code using Gemini API.

    Args:
        code (str): Source code to document.
        file_name (str): Name of the source file.

    Returns:
        str: Generated documentation in markdown format.
    """
    prompt_template = load_prompt_template()

    # Format the prompt with actual code and filename
    prompt = prompt_template.format(code=code, file_name=file_name)

    # Call Gemini API flash-2.0
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # Use the appropriate model name
        contents=prompt
    )

    return response.text
