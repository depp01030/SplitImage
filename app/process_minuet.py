
import os
import requests
import traceback
import numpy as np
import cv2
from app.split_utils import find_sub_images, save_sub_images
from app.scrape import scrape_minuet_page_images, get_product_name
from app.config import config
from urllib.parse import urlparse, unquote
minuet_temp = "https://en.love-minuet.com/product/koon-stripe-pants-3color/17339/category/1/display/3/"
def is_minuet(url: str) -> bool:
    """
    檢查網址是否為 Naver 網站
    """
    keywords = ["minuet", "minuet.com.tw", "minuet.tw"]
    for keyword in keywords:
        if keyword in url:
            return True 
    return False

def get_filename_from_url(url):
    parsed = urlparse(url)
    basename = os.path.basename(parsed.path)
    basename = unquote(basename)
    if not os.path.splitext(basename)[1]:
        basename += ".jpg"
    return basename


def process_minuet_url(image_url, output_dir): 
    try:
        prefix = os.path.splitext(get_filename_from_url(image_url))[0]
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        
        resp = requests.get(image_url, headers=headers)
        
        # 檢查響應狀態
        if resp.status_code != 200:
            return {"status": "error", "message": f"Failed to download image: HTTP {resp.status_code}"}
            
        img_arr = np.frombuffer(resp.content, np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        
        if img is None:
            return {"status": "error", "message": "Failed to decode image"}
            
        sub_imgs = find_sub_images(img)
        save_sub_images(sub_imgs, output_dir, prefix=prefix)
        
        return {"status": "ok", "num_sub_images": len(sub_imgs)}
    except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

def process_minuet_page(url):
    try:
        product_name = get_product_name(url)
        image_urls = scrape_minuet_page_images(url)
        # create folder for product
        folder_path = os.path.join(config.OUTPUT_DIR, product_name)
        os.makedirs(folder_path, exist_ok=True)

        cnt = 0
        for image_url in image_urls:
            split_result = process_minuet_url(image_url, folder_path)
            if split_result["status"] == "ok":
                cnt += split_result["num_sub_images"]
            else:
                print(split_result["message"])
        return {"status": "ok", "num_sub_images": cnt}
    except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": str(e)}
    
