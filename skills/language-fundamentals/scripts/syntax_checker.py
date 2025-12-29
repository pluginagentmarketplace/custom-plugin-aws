#!/usr/bin/env python3
"""Multi-language syntax checker."""
import subprocess
import sys

CHECKERS = {
    ".py": ["python", "-m", "py_compile"],
    ".js": ["node", "--check"],
    ".ts": ["npx", "tsc", "--noEmit"],
}

def check_syntax(filepath: str) -> dict:
    """Check file syntax."""
    ext = "." + filepath.split(".")[-1]
    if ext not in CHECKERS:
        return {"error": f"Unsupported extension: {ext}"}

    cmd = CHECKERS[ext] + [filepath]
    result = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "file": filepath,
        "valid": result.returncode == 0,
        "errors": result.stderr if result.returncode != 0 else None
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(check_syntax(sys.argv[1]))
