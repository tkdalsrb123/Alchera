import os, sys, json
import logging
import numpy as np
from tqdm import tqdm
from collections import defaultdict
from PIL import Image, ImageFont, ImageDraw

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

def AddPadding(img_path):
    img = Image.open(img_path)
    right = 50
    left = 50
    top = 50
    bottom = 200
    
    width, height = img.size
    
    new_width = width + right + left
    new_height = height + bottom
    
    result = Image.new(img.mode, (new_width, new_height), (255, 255, 255))
    
    result.paste(img, (left, top))

    return result

def get_text_dimensions(text_string, font):
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

_, img_dir, json_dir, output_dir = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, '.png')
json_dict = readfiles(json_dir, '.json')

for filename, img_path in tqdm(img_dict.items()):
    json_path = json_dict[filename]
    logger.info(json_path)
    output_img_path = makeOutputPath(img_path, img_dir, output_dir)
    with open(json_path, encoding='utf-8-sig') as f:
        json_file = json.load(f)

    pd_type = json_file['label']['PD_type']
    insulator_tyep = json_file['metadata']['equipment_information']['insulator_type']
    equipment_name = json_file['metadata']['equipment_information']['equipment_name']
    
    text = f"equipment_name(수집 장비):{equipment_name} \n insulator_tyep(절연체 종류):{insulator_tyep} \n PD_type(부분방전 유형):{pd_type}"
    img = AddPadding(img_path)

    width, height = img.size

    fontpath = "malgunbd.ttf"
    fontSize = 15
    font = ImageFont.truetype(fontpath, fontSize)
    draw = ImageDraw.Draw(img)
    
    draw.text((0, height-100), text, (0, 0, 0), font)

    img.save(output_img_path, 'PNG')
    logger.info(f"{output_img_path} 저장!!")
    