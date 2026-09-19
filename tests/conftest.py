import sys
from pathlib import Path

# Adds the main project folder (6FFECT) to the Python paths
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))
