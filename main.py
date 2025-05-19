# -*- coding: utf-8 -*-
#main.py

from app.config import config
from app.process import process_folder, process_file, process_url
from app.scrape import scrape_page_images, get_product_name
from fastapi import FastAPI, UploadFile, File, Form
import os

app = FastAPI(title="圖片分割 API")

@app.get("/")
async def root():
    return {"message": "Welcome to the Image Split API!"}
@app.post("/split/url")
async def split_url(url: str = Form(...)):
    cnt = process_url(url, config.OUTPUT_DIR)
    return {"status": "ok", "num_sub_images": cnt}

@app.post("/split/page_url")
async def split_page_url(url: str = Form(...)):
    product_name = get_product_name(url)
    image_urls = scrape_page_images(url)
    # create folder for product
    folder_path = os.path.join(config.OUTPUT_DIR, product_name)
    os.makedirs(folder_path, exist_ok=True)

    cnt = 0
    for url in image_urls:
        cnt += process_url(url, folder_path)
    return {"status": "ok", "num_sub_images": cnt}



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
