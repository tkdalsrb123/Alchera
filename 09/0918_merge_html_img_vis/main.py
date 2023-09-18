import cv2, os, sys, json
import logging
import numpy as np
from tqdm import tqdm
from collections import defaultdict
from html2image import Html2Image
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def make_logger(log):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # formatter
    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s:%(lineno)d] -- %(message)s")
    # file_handler
    file_handler = logging.FileHandler(log, mode='w')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    # logger.add
    logger.addHandler(file_handler)
    
    return logger

def readfiles(dir, Ext):
    file_dict = defaultdict(str)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == Ext:
                file_path = os.path.join(root, file)

                file_dict[filename] = file_path
    return file_dict

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

_, img_dir, html_dir, html2img_dir, output_dir = sys.argv

logger = make_logger('log.log')

html_dict = readfiles(html_dir, '.html')

driver = webdriver.Chrome()
options = webdriver.ChromeOptions()
options.add_argument('headless')

for filename, html_path in tqdm(html_dict.items()):
    try:
        driver.get(html_path)
        tbody_el = driver.find_element(By.XPATH, "/html/body/table/tbody")
        width = tbody_el.size['width']
        height = tbody_el.size['height']
        driver.set_window_size(width, height+220)
        save_img = f'{html2img_dir}/{filename}.png'
        driver.save_screenshot(save_img)
        # time.sleep(1)
    except:
        print(html_path, '오류 파일')
        pass
    
driver.quit()

img_dict = readfiles(img_dir, '.jpg')
html_img_dict = readfiles(html2img_dir, '.png')

for filename, img_path in tqdm(img_dict.items()):
    output_img_path = makeOutputPath(img_path, img_dir, output_dir)
    html_path = html_img_dict.get(filename)
    if html_path:
        logger.info(html_path)
        img1 = Image.open(img_path)
        img2 = Image.open(html_path)
        img2 = img2.resize(img1.size)
        img1_size = img1.size
        img2_size = img2.size
        new_image = Image.new('RGB', (2*img1_size[0], img1_size[1]), (250,250,250))
        new_image.paste(img1, (0,0))
        new_image.paste(img2,(img1_size[0], 0))
        new_image.save(output_img_path, "PNG")
        