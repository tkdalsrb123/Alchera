import json, cv2, os, sys
import logging
import numpy as np
from collections import defaultdict
from tqdm import tqdm
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
                filename = '_'.join(filename.split('_')[2:])
                file_path = os.path.join(root, file)

                file_dict[filename] = file_path
    return file_dict

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_img(img_path, img):
    result, encoded_img = cv2.imencode('.png', img)
    logger.info(f"{img_path} 저장!!")
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (0, 0))  
    return result

def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)
    
def create_text(text, font, img_w, img_h):
    w, h = get_text_dimensions(text, font)
    if w > img_w:
        split = len(text)//2
        text = text[:split] + '\n' + text[split:]
    return text

if __name__ == "__main__":

    _, input_dir, output_dir = sys.argv

    logger = make_logger('log.log')

    img_dict = readfiles(input_dir, '.jpg')
    json_dict = readfiles(input_dir, '.json')

    for filename, img_path in tqdm(img_dict.items()):
        json_path = json_dict.get(filename)
        if json_path:
            output_img_path = makeOutputPath(img_path, input_dir, output_dir)
            with open(json_path, encoding='utf-8') as f:
                json_file = json.load(f)
            
            
            size = 13
            font = ImageFont.truetype('malgunbd.ttf', size)
            
            img = Image.open(img_path)
            width, height = img.size
            
            add_img = add_margin(img, 0, width, 0, 0, (255, 255,255))
            add_w, add_h = add_img.size
            draw = ImageDraw.Draw(add_img)
            for idx, ann in enumerate(json_file['annotations']):
                title = ann['title']
                title_text = f"title: {title}"
                legend = ','.join(ann["legend"])
                legend_text = f"legend: {legend}"
                unit = ann['unit']
                unit_text = f"unit: {unit}"
                x_axis = ','.join(ann['axis_label']['x_axis'])
                x_axis_text = f"axis_label - x_axis: {x_axis}"
                y_axis = ','.join(ann['axis_label']['y_axis'])
                y_axis_text = f"axis_label - y_axis: {y_axis}"
                data_label = ','.join([str(d)for d in ann['data_label'][0]])
                data_label_text = f"data_lable: {data_label}"
                
                title_text = create_text(title_text, font, width, add_h)
                legend_text = create_text(legend_text, font, width, add_h)
                unit_text = create_text(unit_text, font, width, add_h)
                x_axis_text = create_text(x_axis_text, font, width, add_h)
                y_axis_text= create_text(y_axis_text, font, width, add_h)
                data_label_text= create_text(data_label_text, font, width, add_h)

                text = '\n'.join([title_text, legend_text, unit_text, x_axis_text, y_axis_text, data_label_text])
        
                if idx > 0:
                    text = copy_text + '\n ---- \n' + text

                copy_text = text


                draw.text((width+5, 0), text, (0,0,0), font=font )
            add_img.save(output_img_path, 'PNG')
        else:
            print(img_path)
