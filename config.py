from dotenv import load_dotenv
import os

load_dotenv()

def validate_config():
    required_vars = ["TOKEN", "SHEET_ID", "CREDENTIALS_PATH"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise ValueError(f"Отсутствуют переменные окружения: {missing}")
