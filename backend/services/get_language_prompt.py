import os

def get_language_prompt(file_name: str) -> str:
    """
    Determines the programming language of the given file based on its extension
    and returns a prompt string to be used in documentation generation.

    Args:
        file_name (str): Name of the source file.

    Returns:
        str: A prompt string indicating the programming language of the code.
        str: The programming language identified from the file extension.

    """

    # create a dict for language and extensions
    language_extensions = {
        "python": [".py"],
        "javascript": [".js", ".jsx"],
        "typescript": [".ts", ".tsx"],
        "java": [".java"],
        "go": [".go"],
        "ruby": [".rb"],
        "rust": [".rs"],
        "cpp": [".cpp", ".h"],
        "csharp": [".cs"],
        # Add more languages and extensions as needed
    }

    # Determine the programming language based on file extension
    file_extension = os.path.splitext(file_name)[1].lower()
    language = "unknown"
    for lang, extensions in language_extensions.items():
        if file_extension in extensions:
            language = lang
            break
    
    if language == "unknown":
        # if language is unknown, add a message to the prompt
       language_prompt = (
            f"Note: The programming language of the provided code is unknown. "
            "Please generate documentation based on the code structure without specific language context.\n\n"
        )
    else:
        language_prompt = (
            f"The programming language of the provided code is {language}. "
            "Please generate documentation based on the code structure.\n\n"
        )
    
    return language_prompt, language