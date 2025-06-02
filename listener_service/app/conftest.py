import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
root_dir = Path(__file__).parent
sys.path.append(str(root_dir))