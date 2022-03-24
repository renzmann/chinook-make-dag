from pathlib import Path

THIS_FILE_DIR = Path(__file__).absolute().parent
PROJECT_DIR = THIS_FILE_DIR.parent
DEFAULT_DATABASE = THIS_FILE_DIR.name
TARGET_DIR = PROJECT_DIR / "target"
SQL_DIR = PROJECT_DIR / "sql"
DATA_DIR = PROJECT_DIR / "data"
