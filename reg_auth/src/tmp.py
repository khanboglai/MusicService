from pathlib import Path

BASE_DIR = Path(__file__).parent

Path = BASE_DIR / "certs"

print(Path)