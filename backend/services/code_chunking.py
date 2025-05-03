import os
from google import genai
from google.genai import types
from .get_language_prompt import get_language_prompt
from .load_prompt import load_prompt_template
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from typing import List, Optional

# Initialize Gemini client
api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)

def chunk_code(code: str, language: str, max_chunk_size: int = 8000, chunk_overlap: int = 200) -> List[str]:
    """
    Chunks source code based on language-specific syntax.
    
    Args:
        code: The source code to chunk
        language: Programming language of the code
        max_chunk_size: Maximum size of each chunk in characters
        chunk_overlap: Number of characters to overlap between chunks
        
    Returns:
        List of code chunks
    """
    # Check if code needs chunking
    if len(code) <= max_chunk_size:
        return [code]
    
    # Map common language names to LangChain Language enum
    language_map = {
        "python": Language.PYTHON,
        "py": Language.PYTHON,
        "javascript": Language.JS,
        "js": Language.JS,
        "typescript": Language.TS,
        "ts": Language.TS,
        "java": Language.JAVA,
        "go": Language.GO,
        "ruby": Language.RUBY,
        "rust": Language.RUST,
        "cpp": Language.CPP,
        "c++": Language.CPP,
        "c": Language.C,
        "csharp": Language.CSHARP,
        "c#": Language.CSHARP,
        "php": Language.PHP,
    }
    
    # Get the language enum or use generic text splitting if language not supported
    lang = language_map.get(language.lower())
    
    # Create the appropriate text splitter
    if lang:
        text_splitter = RecursiveCharacterTextSplitter.from_language(
            language=lang,
            chunk_size=max_chunk_size,
            chunk_overlap=chunk_overlap
        )
    else:
        # Fallback to generic recursive splitting with code-friendly separators
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=max_chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", ";", ",", " ", ""]
        )
    
    # Split the code into chunks
    chunks = text_splitter.create_documents([code])
    
    # Extract the text content from the documents
    return [chunk.page_content for chunk in chunks]


def generate_chunk_documentation(code_chunk: str, language_prompt: str, file_name: str) -> str:
    """
    Generates documentation for a single code chunk using Gemini API.
    
    Args:
        code_chunk (str): Source code chunk to document.
        language_prompt (str): Prompt indicating the programming language of the code.
        file_name (str): Name of the source file.
        
    Returns:
        str: Generated documentation in markdown format for the code chunk.
    """
    
    # Load the structured documentation prompt
    prompt_template = load_prompt_template("documentation_prompt.txt")
    
    # Create the prompt for this specific chunk
    prompt = prompt_template.format(
        code=code_chunk,
        language_prompt=language_prompt,
        file_name=file_name
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                top_p=0.9,
                top_k=40
            )
        )
        documentation = response.text
    except Exception as e:
        return f"Error generating documentation for chunk: {str(e)}"
    
    return documentation

def combine_documentation_chunks(chunk_docs: List[str], language: str, file_name: str) -> str:
    """
    Combines documentation from multiple code chunks into a single markdown document.
    
    Args:
        chunk_docs (List[str]): List of documentation strings for each code chunk.
        
    Returns:
        str: Combined documentation in markdown format.
    """
    # Aggregate the documentation from all chunks
    aggregation_prompt = f"""
    I have documentation for different parts of a {language} file named {file_name}.
    Please combine these documentation chunks into a single coherent documentation:
    
    {' '.join([f'Chunk {i+1}: {doc}' for i, doc in enumerate(chunk_docs)])}
    
    Create a unified, non-repetitive documentation that covers all the functionality described in these chunks.
    """
        
    try:
        aggregation_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=aggregation_prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                top_p=0.9,
                top_k=40,
                max_output_tokens=4000
            )
        )
        documentation = aggregation_response.text
    except Exception as e:
        return f"Error aggregating documentation chunks: {str(e)}"
    
    return documentation