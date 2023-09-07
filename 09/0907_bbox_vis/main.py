import json, os, sys, cv2
from collections import defaultdict
import numpy as np
import logging
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont

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
    Ext = Ext.lower()
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext == Ext:
                file_path = os.path.join(root, file)

                file_dict[filename] = file_path
    return file_dict

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

_, img_dir, json_dir, output_dir = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, '.JPG')
json_dict = readfiles(json_dir, '.json')

for filename, img_path in tqdm(img_dict.items()):
    have_json = json_dict.get(filename)
    logger.info(filename)
    if have_json != None:
        json_path = json_dict[filename]
        root, file = os.path.split(img_path)
        mid = '\\'.join(root.split('\\')[len(img_dir.split('\\')):])
        folder= os.path.join(output_dir, mid)
        os.makedirs(folder, exist_ok=True)
        output_img_path = os.path.join(folder, file)

        with open(json_path, encoding='utf-8') as f:
            json_file = json.load(f)
        
        text = json_file['scene_info']['fall_direction']
        coor_split = json_file['bboxdata']['bbox_location'].split(',')
        if len(coor_split) > 1:
            x1 = round(float(coor_split[0]))
            y1 = round(float(coor_split[1]))
            x2 = round(float(coor_split[2]))
            y2 = round(float(coor_split[3]))

            img = read_img(img_path)
            
            font = cv2.FONT_HERSHEY_PLAIN
            
            overlay = img.copy()
            
            fontScale = 3   # background 크기 조절(글씨 크기를 조절하면서 같이 조절해야함)
            text_w, text_h = cv2.getTextSize(text, font, fontScale=fontScale, thickness=1)[0]
            cv2.rectangle(overlay, (x1, y1-text_h), (x1+(text_w//5)*2, y1), (255,255,255), -1)
            alpha = 0.5  # 배경 투명도 조절
            bbox_thickness = 2  # bbox 선두께 조절
            fontSize = 30   # 글씨 크기 조절
            img = cv2.addWeighted(img, alpha, overlay, 1-alpha, 0)
            cv2.rectangle(img, (x1,y1),(x2,y2), (0, 0, 255), thickness=bbox_thickness)  
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)        
            img = Image.fromarray(img)
            fontpath = "malgunbd.ttf"
            pil_font = ImageFont.truetype(fontpath, fontSize)
            draw = ImageDraw.Draw(img)

            draw.text((x1, y1-text_h-5), text, font=pil_font, fill=(255, 0, 0) )

            logger.info(f"{output_img_path} 저장!!")
            img.save(output_img_path, 'JPEG')
        else:
            img.save(output_img_path, 'JPEG')