import os
from pathlib import Path
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///charity_donations.db')
APP_NAME = "Charity connect"
APP_VERSION = "1.0.0"
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
BCRYPT_ROUNDS = 12
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
SESSION_FILE = DATA_DIR / '.session'
if DATABASE_URL.startswith('sqlite'):
    db_path = Path(DATABASE_URL.replace('sqlite:///', ''))
    db_path.parent.mkdir(parents=True, exist_ok=True)