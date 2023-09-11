import cv2, json, os, sys
from collections import defaultdict
from PIL import Image, ImageFont, ImageDraw
import logging
from tqdm import tqdm

def make_logger(log):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # formatter
    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s:%(lineno)d] -- %(message)s")
    # file_handler
    file_handler = logging.FileHandler(log, mode='w')
    file_handler.setFormatter(file_formatter)
    file_handler.setLjhevel(logging.INFO)
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
    bottom = 50
    
    width, height = img.size
    
    new_width = width + right + left
    new_height = height + top + bottom
    
    result = Image.new(img.mode, (new_width, new_height), (255, 255, 255))
    
    result.paste(img, (left, top))

    return result

def get_text_dimensions(text_string, font):
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

_, img_dir, json_dir, output_dir, text_size = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, '.png')
json_dict = readfiles(json_dir, '.json')

for filename, img_path in img_dict.items():
    have_json = json_dict.get(filename)
    if have_json != None:
        json_path = json_dict[filename]

        root, file = os.path.split(img_path)
        mid = '\\'.join(root.split('\\')[len(img_dir.split('\\')):])
        folder = os.path.join(output_dir, mid)
        os.makedirs(folder, exist_ok=True)
        output_img_dir = os.path.join(folder, file)
        
        with open(json_path, encoding='utf-8') as f:
            json_file = json.load(f)
        x_list = []
        y_list = []
        
        img = AddPadding(img_path)

        fontpath = "malgunbd.ttf"
        fontSize = int(text_size)
        font = ImageFont.truetype(fontpath, fontSize)
        draw = ImageDraw.Draw(img)
        
        for ocr in json_file['source_image']['ocr']:
            coor = eval(ocr[0])
            text = ocr[1]
            x = [ co['x']  for co in coor]
            y = [ co['y']  for co in coor]
            x1 = min(x) + 50
            y1 = min(y) + 50 
            x2 = max(x) + 50
            y2 = max(y) + 50
            
            width, height = get_text_dimensions(text, font)
            text_background = draw.textbbox((x1 + ((round((x2-x1) - width)//2)), y1-height), text, font=font)
            draw.rectangle((x1,y1,x2,y2), outline=(255,0,0), width=1)
            draw.rectangle((text_background), fill=(0, 0, 0))
            draw.text((x1 + ((round((x2-x1) - width)//2)), y1-height), text, font=font, fill=(255, 255, 255))

        logger.info(f"{output_img_dir} 저장 !!")
        img.save(output_img_dir, 'PNG')
            
            