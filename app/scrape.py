import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
'''
url = "https://en.love-minuet.com/product/nattie-short-pants-%EC%95%84%EC%9D%B4%EB%B3%B4%EB%A6%AC/17329/category/42/display/1/"
url = "https://en.love-minuet.com/product/koon-stripe-pants-3color/17339/category/1/display/3/"
url = "https://www.veryyou.co.kr/product/%EB%AF%B8%EC%97%98-ops/23570/category/135/display/1/"
'''
def get_product_name(url: str) -> str:

   # ✅ 拆出 slug 部分（URL path 中的第二段）
    slug = url.strip("/").split("/")[4]  # index=4 是商品名稱

    # ✅ URL decode（將 %EC… 解成韓文）
    product_name = unquote(slug)
    print("商品名稱：", product_name)
    return product_name
   

def scrape_minuet_page_images(url):
    base_url = "https://en.love-minuet.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 抓取所有商品說明中的圖片
    prd_detail = soup.select_one("#prdDetail")
    img_tags = prd_detail.select("p img")

    image_urls = [urljoin(base_url, img["ec-data-src"]) for img in img_tags if img.get("ec-data-src")]

    # 輸出圖片連結
    for img_url in image_urls:
        print(img_url)
    return image_urls


def scrape_veryyou_page_images(url):
    # url = 'https://www.veryyou.co.kr/product/%EB%B9%84%EC%98%AC%EB%9D%BC-%EC%A0%88%EA%B0%9C-sleeveless/23504/category/25/display/1/'
    base_url = "https://www.veryyou.co.kr"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 依照指定 selector 抓取所有 img
    section = soup.select_one("#prdDetailContent")
    if section:
        img_tags = section.select("img")
        image_urls = [urljoin(base_url, img.get("ec-data-src") or img.get("src")) for img in img_tags if img.get("ec-data-src") or img.get("src")]
    else:
        image_urls = []

    # 輸出圖片連結
    for img_url in image_urls:
        print(img_url)
    return image_urls



