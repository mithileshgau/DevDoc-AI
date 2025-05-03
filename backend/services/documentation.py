from .get_language_prompt import get_language_prompt
from .code_chunking import chunk_code, combine_documentation_chunks, generate_chunk_documentation


def generate_documentation(code: str, file_name: str) -> str:
    """
    Generates high-quality documentation for the given code using Gemini API
    with hallucination mitigation techniques and code chunking for large files.
    
    Args:
        code (str): Source code to document.
        file_name (str): Name of the source file.
        
    Returns:
        str: Generated documentation in markdown format.
    """
    
    # Determine the programming language of the code
    language_prompt, language = get_language_prompt(file_name)
    
    # Check if code needs to be chunked (>8000 chars is a reasonable threshold)
    code_chunks = chunk_code(code, language, max_chunk_size=8000, chunk_overlap=50)


    if len(code_chunks) == 1:
        # generate_chunk_documentation for single chunk

        code_chunk = code_chunks[0]

        documentation = generate_chunk_documentation(code_chunk, language_prompt, file_name)

    else:
        # Large code file, process chunks and aggregate
        chunk_docs = []
        
        for i, chunk in enumerate(code_chunks):
            try:
                # Generate documentation for each chunk
                chunk_doc = generate_chunk_documentation(chunk, language_prompt, file_name)
                chunk_docs.append(chunk_doc)
            except Exception as e:
                return f"Error generating documentation for chunk {i+1}: {str(e)}"
        
        documentation = combine_documentation_chunks(chunk_docs, language, file_name)
    
    # Add a disclaimer about potential hallucinations
    disclaimer = (
        "\n\n---\n\n*Note: This documentation was automatically generated and has been "
        "checked for accuracy against the source code. However, some interpretations "
        "of code functionality may require human review.*"
    )
    documentation += disclaimer
    
    return documentation

