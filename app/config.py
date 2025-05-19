import os
from dotenv import load_dotenv

load_dotenv()  # 會自動找專案根目錄的 .env

class Config:
    INPUT_DIR = os.getenv("INPUT_DIR", "./input")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output")
    API_PORT = int(os.getenv("API_PORT", "8888"))

config = Config()
