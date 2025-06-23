import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
from app.config import config


def is_naver(url: str) -> bool:
    """
    檢查網址是否為 Naver 網站
    """
    keywords = ["naver.com", "blog.naver.com", "post.naver.com", "smartstore.naver"]
    for keyword in keywords:
        if keyword in url:
            return True
    return False
def get_naver_product_name(url: str) -> str:
    '''
    url = "https://smartstore.naver.com/foldedlinen/products/11452355200"
    '''
    # 取得商店名稱與商品ID
    parts = url.strip("/").split("/")
    store = parts[3]         # foldedlinen
    product_id = parts[5]    # 11452355200
    product_id = product_id.split('?')[0]
    product_name = f"{store}-{product_id}"
    print("商品名稱：", product_name)
    return product_name


def unpack_naver_data(data):

    # 正確處理 JSON 格式的資料
    image_urls = data.get('image_urls', [])
    page_url = data.get('page_url', '')  # 獲取頁面 URL
    if not is_naver(page_url):
        print("Invalid Naver page URL")
        return {
            'status': 'error',
            'message': 'Invalid Naver page URL'
        }
    
    
    print(f"收到 NAVER 圖片 URL 數量：{len(image_urls)}")
    return {
        'status': 'ok',
        'image_urls': image_urls,
        'page_url': page_url
    }
def process_naver_page(data):

    unpacked_data = unpack_naver_data(data)
    
    if unpacked_data['status'] != 'ok':
        return {
            'status': 'error',
            'message': unpacked_data['message']
        }
    page_url = unpacked_data['page_url']
    image_urls = unpacked_data['image_urls']
    # 使用 process_naver_page 函數處理圖片
    
    try:
        product_name = get_naver_product_name(page_url) 
        
        # 建立商品資料夾
        folder_path = os.path.join(config.OUTPUT_DIR, product_name)
        os.makedirs(folder_path, exist_ok=True)
 
        cnt = 0
        for i, img_url in enumerate(image_urls):
            try:
                # 下載並處理圖片
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Referer": page_url
                }
                img_resp = requests.get(img_url, headers=headers, timeout=10)
                
                if img_resp.status_code == 200:
                    # 取得檔案名稱
                    filename = os.path.basename(img_url.split('?')[0])
                    if not filename or '.' not in filename:
                        # 如果沒有有效檔名，生成一個
                        filename = f"image_{i+1}.jpg"
                    
                    # 儲存檔案路徑
                    file_path = os.path.join(folder_path, filename)
                    
                    # 儲存檔案
                    with open(file_path, 'wb') as f:
                        f.write(img_resp.content)
                    
                    print(f"已下載圖片 {i+1}/{len(image_urls)}: {filename}")
                    cnt += 1
 
                else:
                    print(f"無法下載圖片 {i+1}/{len(image_urls)}: HTTP 狀態碼 {img_resp.status_code}")
            except Exception as e:
                print(f"處理圖片時發生錯誤 {img_url}: {str(e)}")
                continue

        return {"status": "ok", "num_sub_images": cnt}
    except Exception as e:
        import traceback
        print(f"處理頁面時發生錯誤: {url}, 錯誤: {str(e)}")
        traceback.print_exc()
        return {"status": "error", "message": str(e)}