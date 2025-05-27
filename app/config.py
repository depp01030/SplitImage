import os

# 嘗試導入 dotenv，如果無法導入則忽略
try:
    from dotenv import load_dotenv
    load_dotenv()  # 會自動找專案根目錄的 .env
    print("已載入 .env 檔案設定")
except ImportError:
    print("警告：未找到 dotenv 模組，將使用預設設定")
    pass  # 忽略錯誤，後續會使用默認值

class Config:
    INPUT_DIR = os.getenv("INPUT_DIR", "./input")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output")
    API_PORT = int(os.getenv("API_PORT", "8888"))

config = Config()
