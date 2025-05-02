import re
from typing import Dict, List, Tuple


def verify_documentation(code_elements: Dict, documentation: str, language: str) -> Tuple[bool, List[str]]:
    """
    Verifies the generated documentation against the extracted code elements
    to detect potential hallucinations.
    
    Args:
        code_elements (Dict): Dictionary of extracted code elements
        documentation (str): Generated documentation to verify
        language (str): Programming language of the code
        
    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_issues)
    """
    issues = []
    
    # Check for function names that don't exist in the code
    function_names = []
    for func in code_elements["functions"]:
        if isinstance(func, tuple) and len(func) > 0:
            function_names.append(func[0])
        elif isinstance(func, str):
            function_names.append(func)
    
    for function_name in function_names:
        if function_name and function_name not in documentation:
            issues.append(f"Function '{function_name}' is in the code but missing from documentation")
    
    # Check for class names that don't exist in the code
    for class_name in code_elements["classes"]:
        if class_name and class_name not in documentation:
            issues.append(f"Class '{class_name}' is in the code but missing from documentation")
    
    # Look for potential hallucinated functions/classes (language-specific)
    if language == "python":
        doc_function_matches = re.findall(r"`def\s+(\w+)\s*\(", documentation)
        for func in doc_function_matches:
            if not any(func == code_func[0] if isinstance(code_func, tuple) else func == code_func 
                       for code_func in code_elements["functions"]):
                issues.append(f"Documentation mentions function '{func}' which doesn't exist in the code")
        
        doc_class_matches = re.findall(r"`class\s+(\w+)", documentation)
        for cls in doc_class_matches:
            if cls not in code_elements["classes"]:
                issues.append(f"Documentation mentions class '{cls}' which doesn't exist in the code")
    
    elif language == "javascript":
        # Check for documented functions that don't exist
        doc_function_matches = re.findall(r"`(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:function|\([^)]*\)\s*=>)|(\w+)\s*:\s*function)", documentation)
        for func_match in doc_function_matches:
            if isinstance(func_match, tuple):
                for func in func_match:
                    if func and not any(func == code_func[0] if isinstance(code_func, tuple) else func == code_func 
                                       for code_func in code_elements["functions"]):
                        issues.append(f"Documentation mentions function '{func}' which doesn't exist in the code")
            else:
                if func_match and not any(func_match == code_func[0] if isinstance(code_func, tuple) else func_match == code_func 
                                         for code_func in code_elements["functions"]):
                    issues.append(f"Documentation mentions function '{func_match}' which doesn't exist in the code")
    
    # Generic function and class checks for other languages
    else:
        # Simple heuristic to look for code blocks that might contain non-existent functions
        # This is a basic approach and might need refinement for specific languages
        code_blocks = re.findall(r"```[a-z]*\n([\s\S]*?)```", documentation)
        for block in code_blocks:
            for line in block.split('\n'):
                # Look for function-like patterns in code blocks
                if re.search(r"\b\w+\s*\(", line):
                    func_name = re.search(r"\b(\w+)\s*\(", line)
                    if func_name and func_name.group(1) not in function_names and func_name.group(1) not in ["if", "for", "while", "switch"]:
                        issues.append(f"Documentation contains code example with potential function '{func_name.group(1)}' which doesn't exist in the code")
    
    return len(issues) == 0, issues