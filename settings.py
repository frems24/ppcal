"""
Application settings.
"""
from pathlib import Path

# Application base dir
BASE_DIR = Path(__file__).resolve().parent

# Directory with systems descriptions
SYSTEMS_DIR = BASE_DIR / "sys"

# Directory with devices descriptions
DEVICES_DIR = BASE_DIR / "devices"

# Directory for results csv files
RESULTS = BASE_DIR / "results"

# Devices assumptions
ROUGHNESS = 4.5e-5
N6 = 31.6  # Constant for valves calculation
X_T = 0.72  # Valve type-dependent constant
VALVE_OPENING = 0.7
