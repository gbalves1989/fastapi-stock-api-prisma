import os

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(".env")

API_HOST: str = os.getenv("API_HOST")
API_PORT: int = int(os.getenv("API_PORT"))
API_VERSION: str = os.getenv("API_VERSION")

SIZE_PER_PAGE: int = os.getenv("SIZE_PER_PAGE")

REQUEST_PER_MINUTES: int = os.getenv("REQUEST_PER_MINUTES")
REQUEST_PER_MINUTES_AUTH: int = os.getenv("REQUEST_PER_MINUTES_AUTH")

JWT_SECRET: str = os.getenv("JWT_SECRET")
ALGORITHM: str = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

UPLOAD_DIR: Path = Path(os.getenv("UPLOAD_DIR"))
