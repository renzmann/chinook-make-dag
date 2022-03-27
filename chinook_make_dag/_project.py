import sqlite3
from pathlib import Path

import yaml

THIS_FILE_DIR = Path(__file__).absolute().parent
PROJECT_DIR = THIS_FILE_DIR.parent
DEFAULT_DATABASE = THIS_FILE_DIR.name
TARGET_DIR = PROJECT_DIR / "target"
SQL_DIR = PROJECT_DIR / "sql"
DATA_DIR = PROJECT_DIR / "data"


def get_config():

    with open(PROJECT_DIR / "config.yml") as f:
        config = yaml.safe_load(f)

    return config


def get_connection():
    config = get_config()
    con = sqlite3.connect(DATA_DIR / "analysis.db")
    con.execute(f"ATTACH '{DATA_DIR / 'chinook.db'}' AS {config['chinook_db']}")
    return con
