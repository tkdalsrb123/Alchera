import os, sys, logging, json, cv2
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
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext in Ext:
                file_path = os.path.join(root, file)
            
                file_dict[filename] = file_path
    return file_dict

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def saveImg(img_path, img, ext):
    if ext == '.jpg':
        img.save(img_path, 'JPEG')
    elif ext == '.png':
        img.save(img_path, 'PNG')
                
def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (0, 0))  
    return result

def get_text_size(draw, text):
    text_bbox = draw.textbbox((0,0), text, font=font)
    h = text_bbox[3] - text_bbox[1]
    w = text_bbox[2] - text_bbox[0]
    
    return h, w

def text_vis(draw, name, value, x, y, img_w):
    draw.text((x, y), name, (0, 0, 255), font=font)
    name_h, name_w = get_text_size(draw, name)
    y = y+name_h+10
    for val in value:
        text_h, text_w = get_text_size(draw, val)
        if text_w > img_w:
            val_list = val.split(' ')
            s = 0

            for i in range(5, len(val_list)):
                t = ' '.join(val_list[s:i])
                th, tw = get_text_size(draw, t)

                if tw > img_w:
                    text = ' '.join(val_list[s:i-3])
                    draw.text((x, y), text, (0, 0, 0), font=font)
                    y += th
                    s = i-3
                    
            if s < len(val_list):
                draw.text((x, y), ' '.join(val_list[s:]), (0, 0, 0), font=font)

        else:
            draw.text((x, y), val, (0, 0, 0), font=font)
        y += text_h+5
   

    return draw, y
    
if __name__ == '__main__':    
    _, img_dir, json_dir, output_dir = sys.argv

    logger = make_logger('log.log')

    img_dict = readfiles(img_dir, ['.jpg', '.png'])
    json_dict = readfiles(json_dir, ['.json'])
    font_path = 'malgunbd.ttf'
    font = ImageFont.truetype(font_path, 10)
    for filename, json_path in tqdm(json_dict.items()):
        img_path = img_dict.get(filename)
        if img_path:

            ext = os.path.splitext(img_path)[-1]
            output_img_path = makeOutputPath(img_path, img_dir, output_dir, ext)
            json_file = readJson(json_path)
            logger.info(json_path)
            img = Image.open(img_path)

            img_width, img_higth = img.size
            img = add_margin(img, 0, round(img_width*0.7), 0, 0, (255,255,255))
            img_add_w, img_add_h = img.size
            draw = ImageDraw.Draw(img)
            h = 5
            for i, att in enumerate(json_file['objects'][0]['attributes']):
                name = att['name']
                name = f'{i+1}. {name}'
                value = att['values'][0]['value']
                
                value_list = value.replace('다.', '다.;').split(';')
 
                draw, height = text_vis(draw, name, value_list, img_width+5, h, round(img_width*0.7))
                
                h = height+20
   
            saveImg(output_img_path, img, ext)

                
                
                
            