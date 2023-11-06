import cv2, os, sys
import logging
import numpy as np
from tqdm import tqdm
from collections import defaultdict

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

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_img(img_path, img):
    result, encoded_img = cv2.imencode('.jpg', img)
    logger.info(f"{img_path} 저장!!")
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)

def makeOutputPath(file_path, file_dir, output_dir, file):
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

_, img_dir, png_dir, output_dir = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, '.jpg')
png_dict = readfiles(png_dir, '.png')
for filename, img_path in img_dict.items():
    png_path = png_dict[filename]
    if png_path:
        root, file = os.path.split(img_path)
        output_img_path = makeOutputPath(img_path, img_dir, output_dir, file)
        img = read_img(img_path)
        png = read_img(png_path)

        img_bitwise = cv2.bitwise_not(png)
        img_gray = cv2.cvtColor(img_bitwise, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(img_gray, 127, 255,cv2.THRESH_BINARY)
        adaptive_threshold= cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        contours, _ = cv2.findContours(adaptive_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for i in range(len(sorted_contours)):
            if i>0:
                contour = sorted_contours[i]
                print([contour])
                cv2.drawContours(img, [contour], -1, (0,0,255), 3)

        # save_img(output_img_path, img)
        
        