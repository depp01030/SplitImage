import os
import requests
import numpy as np
import cv2
from app.utils import find_sub_images, save_sub_images
from app.config import config
from urllib.parse import urlparse, unquote
 
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




def get_filename_from_url(url):
    parsed = urlparse(url)
    basename = os.path.basename(parsed.path)
    basename = unquote(basename)
    if not os.path.splitext(basename)[1]:
        basename += ".jpg"
    return basename

def process_url(url, output_dir):

    prefix = os.path.splitext(get_filename_from_url(url))[0]
    resp = requests.get(url)
    img_arr = np.frombuffer(resp.content, np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    sub_imgs = find_sub_images(img)
    save_sub_images(sub_imgs, output_dir, prefix=prefix)
    return len(sub_imgs)
