# -*- coding: utf-8 -*-
#main.py

from app.config import config
from app.process import process_folder, process_file, process_url, process_page_url
from app.process_naver import process_naver_page
from fastapi import FastAPI, UploadFile, File, Form
import os

app = FastAPI(title="圖片分割 API")

@app.get("/")
async def root():
    return {"message": "Welcome to the Image Split API!"}

@app.post("/download_naver/image_list")
async def receive_naver_image_list(data: dict):
    # 正確處理 JSON 格式的資料
    image_urls = data.get('image_urls', [])
    page_url = data.get('page_url', '')  # 獲取頁面 URL
    print(f"收到 NAVER 圖片 URL 數量：{len(image_urls)}")
    
    # # 輸出前 5 個圖片網址
    # for i, url in enumerate(image_urls[:5]):
    #     print(f"{i+1}. {url}")
    
    # if len(image_urls) > 5:
    #     print(f"... 還有 {len(image_urls) - 5} 張圖片網址")
    
    # 使用 process_naver_page 函數處理圖片
    result = process_naver_page(page_url, image_urls)
    
    # 回傳結果給 extension
    return {"status": "ok", "num_images": len(image_urls), "downloaded": result.get("num_sub_images", 0)}
@app.post("/split/url")
async def split_url(url: str = Form(...)): 
    return  process_url(url, config.OUTPUT_DIR)

@app.post("/split/page_url")
async def split_page_url(url: str = Form(...)):
    status = process_page_url(url)

    return status 



@app.post("/split/file")
async def split_file(file: UploadFile = File(...)):
    tmp_path = os.path.join(config.INPUT_DIR, file.filename)
    with open(tmp_path, "wb") as f:
        f.write(await file.read())
    cnt = process_file(tmp_path, config.OUTPUT_DIR)
    return {"status": "ok", "num_sub_images": cnt}

@app.get("/split/folder")
async def split_folder():
    print('hi')
    results = process_folder(config.INPUT_DIR, config.OUTPUT_DIR)
    return {"status": "ok", "results": results}

# 啟動時 uvicorn main:app --port 8888  （或 API_PORT）
