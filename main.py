# -*- coding: utf-8 -*-
#main.py

from app.config import config
from app.process_naver import is_naver, process_naver_page
from fastapi import FastAPI, UploadFile, File, Form
import os
from app.process_minuet import is_minuet, process_minuet_page
from app.process_veryyou import is_veryyou, process_veryyou_page
app = FastAPI(title="圖片分割 API")

@app.get("/")
async def root():
    return {"message": "Welcome to the Image Split API!"}

return_pack = {
    "status": "ok",
    "num_images": 0,
    "downloaded": 0,
    "message": "Processing completed successfully."
}
@app.post("/download_naver/image_list")
async def receive_naver_image_list(data: dict):
    process_result = process_naver_page(data)
    return_pack.update(process_result)

    return return_pack



@app.post("/split/page_url")
async def download_images(url: str= Form(...)):
    """
    接收圖片網址，下載並處理圖片
    """
    if is_minuet(url):
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
    return_pack = processor(url)
    print(f"處理結果：{return_pack}")   
    return return_pack

# @app.post("/split/url")
# async def split_url(url: str = Form(...)): 
#     return  process_url(url, config.OUTPUT_DIR)

# @app.post("/split/page_url")
# async def split_page_url(url: str = Form(...)):
#     status = process_page_url(url)

#     return status 