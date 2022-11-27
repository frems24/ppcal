"""
Application settings.
"""
from pathlib import Path

# Application base dir
BASE_DIR = Path(__file__).resolve().parent

# Directory with system descriptions in toml files:
TOML_DIR = BASE_DIR / "toml"

# Directory with schemes
SCHEMES_DIR = TOML_DIR / "schemes"

# Directory with devices descriptions
DEVICES_DIR = TOML_DIR / "devices"

# Directory for results csv files
RESULTS = BASE_DIR / "results"

# Devices assumptions
ROUGHNESS = 4.5e-5
N6 = 31.6  # Constant for valves calculation
X_T = 0.72  # Valve type-dependent constant
VALVE_OPENING = 0.7
