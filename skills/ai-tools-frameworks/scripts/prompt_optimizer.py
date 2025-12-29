#!/usr/bin/env python3
"""Prompt optimization utilities."""

def optimize_prompt(prompt: str) -> str:
    """Apply prompt engineering best practices."""
    optimizations = []

    if not prompt.endswith(("?", ".", ":")):
        optimizations.append("Add clear ending punctuation")

    if len(prompt.split()) < 10:
        optimizations.append("Consider adding more context")

    if "step by step" not in prompt.lower():
        optimizations.append("Consider adding 'step by step' for reasoning")

    return {
        "original": prompt,
        "suggestions": optimizations,
        "optimized": f"Please think step by step. {prompt}"
    }

if __name__ == "__main__":
    result = optimize_prompt("Explain machine learning")
    print(result)
