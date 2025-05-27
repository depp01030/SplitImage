import os
import requests
import numpy as np
import cv2
from app.utils import find_sub_images, save_sub_images
from app.config import config
from urllib.parse import urlparse, unquote
from app.utils import is_naver
from app.process_naver import process_naver_page
from app.process_minute import process_minute_page, process_minute_url

def process_folder(input_dir, output_dir):
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    results = []
    for fname in files:
        in_path = os.path.join(input_dir, fname)
        img = cv2.imread(in_path)
        sub_imgs = find_sub_images(img)
        save_sub_images(sub_imgs, output_dir, prefix=os.path.splitext(fname)[0])
        results.append({'file': fname, 'sub_count': len(sub_imgs)})
    return results

def process_file(file_path, output_dir):
    img = cv2.imread(file_path)
    sub_imgs = find_sub_images(img)
    save_sub_images(sub_imgs, output_dir, prefix=os.path.splitext(os.path.basename(file_path))[0])
    return len(sub_imgs)

def process_url(url, output_dir):
    if is_naver(url):
        return {"status": "ok", "message": "not supported for Naver URLs"}
    else: #minute
        return process_minute_url(url, output_dir)

 
def process_page_url(url):
    if is_naver(url):
        return process_naver_page(url)
    else:
        return process_minute_page(url)

