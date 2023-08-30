import os, sys, json
import pandas as pd
from PIL import Image, ImageFont, ImageDraw, ImageOps
from collections import defaultdict
from tqdm import tqdm
import logging


def readfiles(dir, Ext):
    file_dict = defaultdict(str)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == Ext:
                file_path = os.path.join(root, file)
                file_dict[filename] = file_path

    return file_dict

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

_, excel_dir, img_dir, json_dir, output_dir = sys.argv

logger = make_logger('log.log')

df = pd.read_excel(excel_dir)
cat_dict = dict(zip(df['category'], df['class value']))

img_dict = readfiles(img_dir, '.jpg')
json_dict = readfiles(json_dir, '.json')

for filename, img_path in tqdm(img_dict.items()):
    json_filename = f'{filename}_dataset'
    have_json = json_dict.get(json_filename)
    if have_json != None:
        logger.info(img_path)
        json_path = json_dict[json_filename]
        logger.info(json_path)
        root, file = os.path.split(img_path)
        mid = '\\'.join(root.split('\\')[len(img_dir.split('\\')):])
        folder = os.path.join(output_dir, mid)
        os.makedirs(folder, exist_ok=True)
        output_img_path = os.path.join(folder, file)
        with open(json_path, encoding='utf-8') as f:
            json_file = json.load(f)
        text_list = []
        for cat in json_file['images']["category"]:
            text_list.append(cat_dict[cat])
            
        text = '\n'.join(text_list) 

        img = Image.open(img_path)
        img = ImageOps.exif_transpose(img)
        fontpath = 'malgunbd.ttf'
        font = ImageFont.truetype(fontpath, 30)
        draw = ImageDraw.Draw(img)
        
        draw.text((0, 0), text, font=font, fill=(255, 0, 0))
        
        img.save(output_img_path, 'JPEG')

        