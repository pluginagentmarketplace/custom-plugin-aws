#!/usr/bin/env python3
"""Simple code quality analyzer."""
import ast
from pathlib import Path

def analyze_file(filepath: str) -> dict:
    """Analyze Python file for basic metrics."""
    content = Path(filepath).read_text()
    tree = ast.parse(content)

    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

    return {
        "classes": len(classes),
        "functions": len(functions),
        "lines": len(content.splitlines()),
        "complexity_warning": len(functions) > 20
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(analyze_file(sys.argv[1]))
