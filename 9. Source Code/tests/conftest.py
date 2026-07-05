import os
import sys
from pathlib import Path

# Add project root to python path so tests can import app modules
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
