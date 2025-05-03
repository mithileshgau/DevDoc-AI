import os

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