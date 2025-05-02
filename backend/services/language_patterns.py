# Language-specific patterns for code element extraction
LANGUAGE_PATTERNS = {
    # Python patterns
    "python": {
        "extension": ".py",
        "function": r"def\s+(\w+)\s*\(([^)]*)\)",
        "class": r"class\s+(\w+)",
        "import": r"(?:from\s+(\w+)(?:\.\w+)*\s+)?import\s+(.+?)(?:$|\n)",
        "global": r"^([A-Z0-9_]+)\s*=",
        "comment": r"(?:#.+$|'''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\")"
    },
    # JavaScript patterns
    "javascript": {
        "extension": [".js", ".jsx", ".ts", ".tsx"],
        "function": r"(?:function\s+(\w+)\s*\(([^)]*)\)|const\s+(\w+)\s*=\s*(?:function|\([^)]*\)\s*=>)|(\w+)\s*:\s*function\s*\(([^)]*)\))",
        "class": r"class\s+(\w+)",
        "import": r"import\s+(?:(\w+)|{\s*([^}]+)\s*})\s+from",
        "global": r"(?:const|var|let)\s+([A-Z0-9_]+)\s*=",
        "comment": r"(?://.*$|/\*[\s\S]*?\*/)"
    },
    # Java patterns
    "java": {
        "extension": ".java",
        "function": r"(?:public|private|protected)?\s+(?:static\s+)?(?:[\w<>\[\]]+)\s+(\w+)\s*\(([^)]*)\)",
        "class": r"(?:public|private|protected)?\s+(?:static\s+)?class\s+(\w+)",
        "import": r"import\s+(.+?);",
        "global": r"(?:public|private|protected|static|final)\s+(?:\w+)\s+([A-Z0-9_]+)\s*=",
        "comment": r"(?://.*$|/\*[\s\S]*?\*/)"
    },
    # C# patterns
    "csharp": {
        "extension": [".cs"],
        "function": r"(?:public|private|protected|internal)?\s+(?:static\s+)?(?:[\w<>\[\]]+)\s+(\w+)\s*\(([^)]*)\)",
        "class": r"(?:public|private|protected|internal)?\s+(?:static\s+)?class\s+(\w+)",
        "import": r"using\s+(.+?);",
        "global": r"(?:public|private|protected|internal|static|const)\s+(?:\w+)\s+([A-Z0-9_]+)\s*=",
        "comment": r"(?://.*$|/\*[\s\S]*?\*/)"
    },
    # Go patterns
    "go": {
        "extension": ".go",
        "function": r"func\s+(\w+)\s*\(([^)]*)\)",
        "class": r"type\s+(\w+)\s+struct",
        "import": r"import\s+\(([^)]+)\)|import\s+(?:\"([^\"]+)\")",
        "global": r"var\s+([A-Z0-9_]+)",
        "comment": r"(?://.*$|/\*[\s\S]*?\*/)"
    },
    # Ruby patterns
    "ruby": {
        "extension": [".rb"],
        "function": r"def\s+(\w+)(?:\s*\(([^)]*)\))?",
        "class": r"class\s+(\w+)",
        "import": r"require\s+['\"](.+?)['\"]",
        "global": r"([A-Z0-9_]+)\s*=",
        "comment": r"(?:#.*$|=begin[\s\S]*?=end)"
    },
    # PHP patterns
    "php": {
        "extension": [".php"],
        "function": r"function\s+(\w+)\s*\(([^)]*)\)",
        "class": r"class\s+(\w+)",
        "import": r"(?:require|include|require_once|include_once)\s+['\"](.+?)['\"]|use\s+(.+?);",
        "global": r"\$([A-Z0-9_]+)\s*=",
        "comment": r"(?://.*$|/\*[\s\S]*?\*/|#.*$)"
    }
}