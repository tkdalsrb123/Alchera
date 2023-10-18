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
            if ext == Ext:
                file_path = os.path.join(root, file)
            
                file_dict[filename] = file_path
    return file_dict

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def readImg(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def saveImg(img_path, img, ext):
    result, encoded_img = cv2.imencode(f'.{ext}', img)
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)


def draw_text(img, text,
          font=cv2.FONT_HERSHEY_PLAIN,
          pos=(0, 0),
          font_scale=1,
          font_thickness=1,
          text_color=(0, 0, 0),
          text_color_bg=(255, 255, 255)
          ):

    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, pos, (x + text_w, y - text_h), text_color_bg, -1)
    cv2.putText(img, text, (x, y + font_scale - 1), font, font_scale, text_color, font_thickness)

    return text_size

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

if __name__ == '__main__':    
    _, img_dir, json_dir, output_dir = sys.argv

    logger = make_logger('log.log')

    img_dict = readfiles(img_dir, '.jpg')
    json_dict = readfiles(json_dir, '.json')
    font_path = './NotoSansCJKkr-Light.otf'
    font = ImageFont.truetype(font_path, 15)
    for filename, json_path in tqdm(json_dict.items()):
        img_path = img_dict.get(filename)
        if img_path:
            output_img_path = makeOutputPath(img_path, img_dir, output_dir, '.jpg')
            json_file = readJson(json_path)
            logger.info(json_path)
            img = readImg(img_path)
            h, w, _ = img.shape
            i = 1
            text_list = []

            for box in json_file['boxes']:
                x1 = box['coords'][0][0]['x']
                y1 = box['coords'][0][0]['y']
                x2 = box['coords'][0][2]['x']
                y2 = box['coords'][0][2]['y']
                text = box['texts'][0]

                cv2.rectangle(img, (x1,y1), (x2,y2), (0, 0, 255))
                
                draw_text(img, str(i), pos=(x1,y1))

                text_list.append(' '.join([str(i), text]))
                i += 1
            
            img = Image.fromarray(img)
            
            width, height = img.size
            
            img = add_margin(img, 0, w, 0, 0, (255, 255, 255))
            draw = ImageDraw.Draw(img)
            
            text = '\n'.join(text_list)
            text_h, text_w = get_text_size(draw, text)
            if text_h <= height:
                draw.text((width+5, 0), text, (0, 0 ,0), font=font)
            else:
                s = 0
                p = 5
                for i in range(150, len(text_list), 10):
                    th, tw = get_text_size(draw, '\n'.join(text_list[s:i]))
                    if th > height:
                        draw.text((width+p, 0), '\n'.join(text_list[s:i-10]), (0,0,0), font=font)
                        s = i-10
                        p += tw
                if s  < len(text_list):
                    draw.text((width+p, 0), '\n'.join(text_list[s:len(text_list)]), (0,0,0), font=font)

            img.save(output_img_path, 'JPEG')
            
        else:
            print(json_path)