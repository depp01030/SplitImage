
import os
import requests
import numpy as np
import cv2
from app.utils import find_sub_images, save_sub_images
from app.scrape import scrape_page_images, get_product_name
from app.config import config
from urllib.parse import urlparse, unquote


def get_filename_from_url(url):
    parsed = urlparse(url)
    basename = os.path.basename(parsed.path)
    basename = unquote(basename)
    if not os.path.splitext(basename)[1]:
        basename += ".jpg"
    return basename


def process_minute_url(url, output_dir): 
    try:
        prefix = os.path.splitext(get_filename_from_url(url))[0]
        resp = requests.get(url)
        img_arr = np.frombuffer(resp.content, np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        sub_imgs = find_sub_images(img)
        save_sub_images(sub_imgs, output_dir, prefix=prefix)
        
        return {"status": "ok", "num_sub_images": len(sub_imgs)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def process_minute_page(url):
    try:
        product_name = get_product_name(url)
        image_urls = scrape_page_images(url)
        # create folder for product
        folder_path = os.path.join(config.OUTPUT_DIR, product_name)
        os.makedirs(folder_path, exist_ok=True)

        cnt = 0
        for url in image_urls:
            cnt += process_minute_url(url, folder_path)

        return {"status": "ok", "num_sub_images": cnt}
    except Exception as e:
        return {"status": "error", "message": str(e)}