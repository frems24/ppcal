"""
Application settings.
"""
from pathlib import Path

# Application base dir
BASE_DIR = Path(__file__).resolve().parent

# Directory with system description in toml files:
TOML_DIR = BASE_DIR / "toml"
