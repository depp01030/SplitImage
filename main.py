# -*- coding: utf-8 -*-
#main.py

from app.config import config
from app.process_naver import is_naver, process_naver_page
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
import os
from app.process_minuet import is_minuet, process_minuet_page
from app.process_veryyou import is_veryyou, process_veryyou_page
from functools import partial
import asyncio
from concurrent.futures import ProcessPoolExecutor

app = FastAPI(title="圖片分割 API")
# 創建進程池執行器用於CPU密集型任務
process_pool = ProcessPoolExecutor()

@app.get("/")
async def root():
    return {"message": "Welcome to the Image Split API!"}

# 在異步函數中運行CPU密集型任務的輔助函數
async def run_in_process_pool(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(process_pool, partial(func, *args, **kwargs))

@app.post("/download_naver/image_list")
async def receive_naver_image_list(data: dict):
    return_pack = {
        "status": "ok",
        "num_images": 0,
        "downloaded": 0,
        "message": "Processing completed successfully."
    }
    
    # 在進程池中運行CPU密集型操作
    process_result = await run_in_process_pool(process_naver_page, data)
    return_pack.update(process_result)

    return return_pack



@app.post("/split/page_url")
async def download_images(url: str= Form(...),
                           background_tasks: BackgroundTasks = None):
    """
    接收圖片網址，下載並處理圖片
    """
    return_pack = {
        "status": "ok",
        "num_images": 0,
        "downloaded": 0,
        "message": "Processing completed successfully."
    }
    
    if is_minuet(url):
        print(f"此為 Minuet 網址 {url}")
        processor = process_minuet_page
    elif is_naver(url):
        print(f"此為 Naver 網址，請使用naver專用下載功能")
        return_pack["status"] = "error"
        return_pack["message"] = "Please use the Naver-specific download function."
        return return_pack
    elif is_veryyou(url):
        processor = process_veryyou_page
    else:
        print(f"Unsupported URL: {url}")
        print(f"Use minuet trying...")
        processor = process_minuet_page
    
    # 在進程池中運行CPU密集型操作
    result = await run_in_process_pool(processor, url)
    print(f"處理結果：{result}")   
    return result

# @app.post("/split/url")
# async def split_url(url: str = Form(...)): 
#     return  process_url(url, config.OUTPUT_DIR)

# @app.post("/split/page_url")
# async def split_page_url(url: str = Form(...)):
#     status = process_page_url(url)

#     return status