import json, os, sys
import logging
from collections import defaultdict
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

def select_color(Class):
    if Class == '표':
        color = (255, 192, 203)
    elif Class =='텍스트':
        color = (255, 0, 0)
    elif Class == '초록색':
        color = (0, 255, 137)
        
    return color

_, img_dir, json_dir, output_dir = sys.argv

logger = make_logger('log.log')

json_dict = readfiles(json_dir, '.json')
img_dict = readfiles(img_dir, '.png')

for filename, img_path in img_dict.items():

    json_path = json_dict[filename]

    root, file = os.path.split(img_path)
    mid = '\\'.join(root.split('\\')[len(img_dir.split('\\')):])
    folder = os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)
    output_img_dir = os.path.join(folder, file)
    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)

    img = AddPadding(img_path)

    fontpath = "malgunbd.ttf"
    fontSize = 5
    font = ImageFont.truetype(fontpath, fontSize)
    draw = ImageDraw.Draw(img)
    
    description = json_file['descriptions']['description']
    text_list = description.split(' ')
    print(len(text_list), 'text_list')
    print(len(json_file['annotations']['ocr_labels']), 'json_file_list')
    for idx, ocr in enumerate(json_file['annotations']['ocr_labels']):
        x1 = ocr['bbox']['x'] + 50
        y1 = ocr['bbox']['y'] + 50
        x2 = x1 + ocr['bbox']['width']
        y2 = y1 + ocr['bbox']['height']
        _class = ocr['_class']
        text = text_list[idx]
        
        c_width, c_height = get_text_dimensions(_class, font)
        color = select_color(_class)
        text_background = draw.textbbox((x1,y1-c_height), text, font=font)
        draw.rectangle((x1,y1,x2,y2), outline=color, width=1)
        draw.rectangle((text_background), fill=color)
        draw.text((x1,y1-c_height), _class, font=font, fill=(0, 0, 0))
        draw.text((x1,y2), text, font=font, fill=(0,0,0))
        
    logger.info(f"{output_img_dir} 저장 !!")
    img.save(output_img_dir, 'PNG')