#!/usr/bin/env python
# -*- coding: utf-8 -*-
# app_starter.py - 用於啟動 FastAPI 應用程式的入口點

import os
import sys
import uvicorn
from app.config import config

def resource_path(relative_path):
    """取得資源的絕對路徑（用於 PyInstaller 打包後的路徑問題）"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 建立臨時資料夾
        base_path = sys._MEIPASS
    else:
        # 正常情況
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def ensure_directories():
    """確保輸入和輸出目錄存在"""
    # 獲取當前執行檔案的目錄
    base_dir = os.path.abspath(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__))
    
    # 處理相對路徑（如果 config 中使用相對路徑）
    input_dir = config.INPUT_DIR
    output_dir = config.OUTPUT_DIR
    
    # 如果路徑是相對的，轉換為絕對路徑
    if not os.path.isabs(input_dir):
        input_dir = os.path.join(base_dir, input_dir)
    if not os.path.isabs(output_dir):
        output_dir = os.path.join(base_dir, output_dir)
    
    # 創建目錄
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # 更新配置
    config.INPUT_DIR = input_dir
    config.OUTPUT_DIR = output_dir
    
    print(f"輸入目錄: {input_dir}")
    print(f"輸出目錄: {output_dir}")

def main():
    """啟動 FastAPI 應用程式"""
    try:
        print("正在啟動圖片分割 API 服務...")
        ensure_directories()
        
        # 顯示啟動訊息
        port = config.API_PORT
        print(f"API 服務將在 http://localhost:{port} 啟動")
        print("按下 Ctrl+C 可終止服務")
        
        # 導入 main 模組（避免循環導入）
        import main
        
        # 啟動服務
        uvicorn.run(main.app, host="127.0.0.1", port=port)
    except ImportError as e:
        print(f"錯誤：無法導入必要的模組: {e}")
        print("請確認所有需要的套件已經安裝: pip install -r requirements.txt")
    except Exception as e:
        print(f"啟動服務時發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        input("按任意鍵結束程式...")

if __name__ == "__main__":
    main()
