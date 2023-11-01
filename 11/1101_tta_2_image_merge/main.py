import cv2, os, sys
import logging
import numpy as np
from collections import defaultdict
from tqdm import tqdm

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
    file_dict = defaultdict(lambda: defaultdict(str))
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            lr = filename.split('_')[-1][0]
            filename = '_'.join(filename.split('_')[:2])
            ext = ext.lower()
            if ext == Ext:
                file_path = os.path.join(root, file)
                
                file_dict[filename][lr] = file_path
    return file_dict


def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_img(img_path, img):
    result, encoded_img = cv2.imencode('.jpg', img)
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)

def makeOutputPath(file_path, file_dir, output_dir, filename):
    root, file = os.path.split(file_path)
    f, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}{ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    img_dict = readfiles(input_dir, '.jpg')

    for filename, img_path_lr in tqdm(img_dict.items()):
        r_img_path = img_path_lr['R']
        l_img_path = img_path_lr['L']
        
        output_img_path = makeOutputPath(r_img_path, input_dir, output_dir, filename)
        r_img = read_img(r_img_path)
        l_img = read_img(l_img_path)
        
        merge_img = cv2.hconcat([r_img, l_img])
        save_img(output_img_path, merge_img)
        