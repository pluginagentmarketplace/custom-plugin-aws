#!/usr/bin/env python3
"""Time complexity analyzer."""

COMPLEXITY_MAP = {
    "for i in range": "O(n)",
    "for i in range.*for j in range": "O(n²)",
    "while.*//": "O(log n)",
    "sorted(": "O(n log n)",
    "dict[": "O(1)",
}

def analyze_complexity(code: str) -> dict:
    """Analyze code complexity (simplified)."""
    import re
    findings = []

    for pattern, complexity in COMPLEXITY_MAP.items():
        if re.search(pattern, code):
            findings.append({"pattern": pattern, "complexity": complexity})

    return {
        "findings": findings,
        "estimated": findings[0]["complexity"] if findings else "Unknown"
    }

if __name__ == "__main__":
    code = "for i in range(n): print(i)"
    print(analyze_complexity(code))
