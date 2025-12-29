#!/usr/bin/env python3
"""FastAPI application scaffold generator."""

from pathlib import Path

def generate_project(name: str, base_path: str = "."):
    """Generate FastAPI project structure."""
    root = Path(base_path) / name
    dirs = [
        "app/api/v1/endpoints",
        "app/core",
        "app/db",
        "app/models",
        "app/schemas",
        "app/services",
        "tests",
    ]

    for d in dirs:
        (root / d).mkdir(parents=True, exist_ok=True)
        (root / d / "__init__.py").touch()

    # Main application
    (root / "app/main.py").write_text('''
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "healthy"}
''')

    # Config
    (root / "app/core/config.py").write_text('''
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "API"
    DATABASE_URL: str = ""
    SECRET_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
''')

    print(f"Created project: {root}")

if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "myapi"
    generate_project(name)
