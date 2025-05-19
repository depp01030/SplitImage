import cv2
import numpy as np
import os
from PIL import Image

def is_mostly_white(image, white_thresh=245, ratio=0.97):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    white_pixels = np.sum(gray > white_thresh)
    total_pixels = gray.size
    return (white_pixels / total_pixels) > ratio

def find_sub_images(img, min_width=80, min_height=80, white_thresh=245):
    """自動偵測水平子圖位置，回傳每張子圖的ndarray"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 1. 找出非白色像素（預設白色在245以上）
    non_white_mask = (gray < white_thresh).astype(np.uint8) * 255
    # 2. 計算每一行（row）非白色像素比例
    row_non_white = np.sum(non_white_mask > 0, axis=1)
    # 3. 偵測出有內容的範圍
    is_content = row_non_white > (img.shape[1] * 0.01)
    # 4. 將連續的有內容的區段分割出來
    sub_imgs = []
    start, inside = None, False
    for i, v in enumerate(is_content):
        if v and not inside:
            start = i
            inside = True
        elif not v and inside:
            end = i
            if end - start > min_height:
                sub_img = img[start:end, :]
                # 再處理左右白邊
                col_non_white = np.sum((cv2.cvtColor(sub_img, cv2.COLOR_BGR2GRAY) < white_thresh), axis=0)
                left = np.argmax(col_non_white > 0)
                right = len(col_non_white) - np.argmax(col_non_white[::-1] > 0)
                cropped = sub_img[:, left:right]
                # 濾掉太窄/太白的子圖
                if cropped.shape[1] >= min_width and not is_mostly_white(cropped, white_thresh):
                    sub_imgs.append(cropped)
            inside = False
    return sub_imgs

def save_sub_images(sub_imgs, output_dir, prefix="subimg"):
    """
    sub_imgs: list of ndarray
    output_dir: 資料夾路徑
    prefix: 檔名前綴（通常用來源檔案名）
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for idx, img in enumerate(sub_imgs):
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        filename = f"{prefix}_{idx+1}.jpg"
        img_pil.save(os.path.join(output_dir, filename))
