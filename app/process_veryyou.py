import os
import requests
import traceback
import numpy as np
import cv2
from app.split_utils import find_sub_images, save_sub_images
from app.scrape import scrape_veryyou_page_images, get_product_name
from app.config import config
from urllib.parse import urlparse, unquote

veryyou_temp = "https://www.veryyou.co.kr/product/%EB%AF%B8%EC%97%98-ops/23570/category/135/display/1/"

#%%

def is_veryyou(url):
    """
    判斷是否為 VeryYou 網頁
    """
    return "veryyou" in url or "www.veryyou.co.kr" in url
def get_filename_from_url(url):
    parsed = urlparse(url)
    basename = os.path.basename(parsed.path)
    basename = unquote(basename)
    if not os.path.splitext(basename)[1]:
        basename += ".jpg"
    return basename


def process_veryyou_url(image_url):
    """Download a single image from the given URL and return it as OpenCV image"""
    try:
        # 設置HTTP請求頭，模擬瀏覽器請求
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        
        # 發送GET請求下載圖片
        resp = requests.get(image_url, headers=headers)
        
        # 檢查響應狀態
        if resp.status_code != 200:
            print(f"Failed to download image: HTTP {resp.status_code}")
            return None
            
        # 將圖片二進制數據轉換為NumPy數組
        img_arr = np.frombuffer(resp.content, np.uint8)
        # 使用OpenCV解碼圖片數據
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        
        # 檢查圖片是否成功解碼
        if img is None:
            print("Failed to decode image")
            return None
            
        return img
    except Exception as e:
        traceback.print_exc()
        return None

def process_veryyou_page(url):
    try:
        product_name = get_product_name(url)
        image_urls = scrape_veryyou_page_images(url)
        # create folder for product
        folder_path = os.path.join(config.OUTPUT_DIR, product_name)
        os.makedirs(folder_path, exist_ok=True)

        # 1. 下載所有圖片
        print(f"Downloading {len(image_urls)} images...")
        images = []
        for url in image_urls:
            img = process_veryyou_url(url)
            if img is not None:
                images.append(img)
        
        if not images:
            return {"status": "error", "message": "No images were successfully downloaded"}
        
        # 2. 將所有圖片垂直拼接成一張長圖
        print("Concatenating images...")
        # 計算總高度和最大寬度
        total_height = sum(img.shape[0] for img in images)
        max_width = max(img.shape[1] for img in images)
        
        # 創建一個空白畫布
        long_image = np.zeros((total_height, max_width, 3), dtype=np.uint8)
        
        # 垂直拼接圖片
        y_offset = 0
        for img in images:
            h, w = img.shape[:2]
            # 居中放置圖片
            x_offset = (max_width - w) // 2
            long_image[y_offset:y_offset+h, x_offset:x_offset+w] = img
            y_offset += h
        
        # 3. 切割拼接後的長圖
        print("Splitting the concatenated image...")
        sub_imgs = find_sub_images(long_image)
        save_sub_images(sub_imgs, folder_path, prefix=product_name)
        
        return {"status": "ok", "num_sub_images": len(sub_imgs)}
    except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": str(e)}



