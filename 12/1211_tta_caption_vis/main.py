import os, sys, json , cv2, logging
import numpy as np
from PIL import Image, ImageDraw, ImageFont
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
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext in Ext:
                
                file_path = os.path.join(root, file)

                file_dict[filename] = file_path
    return file_dict

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}{ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def save_img(img_path, img, ext):
    result, encoded_img = cv2.imencode(f'.{ext}', img)
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)
            
def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def vis(img, margin, text, output_path):
    
    h, w, _ = img.shape
    new_h = h + margin
    new_img = np.zeros((new_h, w, 3), np.uint8)
    new_img.fill(255)
    
    pillow_img = Image.fromarray(new_img)
    font = ImageFont.truetype('malgunbd.ttf', int(text_size))
    draw = ImageDraw.Draw(pillow_img)

    draw.text((10, h), text, font=font, fill='black')
    
    cv2_image = cv2.cvtColor(np.array(pillow_img), cv2.COLOR_RGB2BGR)
    
    cv2_image[:h, :] = img
    save_img(output_path, cv2_image, 'jpg')
    
if __name__ == "__main__":
    _, img_dir, json_dir, output_dir, text_size = sys.argv
    
    img_dict = readfiles(img_dir, ['.jpg', '.jpeg'])
    json_dict = readfiles(json_dir, ['.json'])
    
    
    for filename, json_path in json_dict.items():
        filename = '_'.join(filename.split('_')[2:])
        img_path = img_dict[filename]
        output_img_path = makeOutputPath(img_path, img_dir, output_dir)
        data = readJson(json_path)

        img = read_img(img_path)       

        text = data['Caption'][0]['description']
        vis(img, 50, text, output_img_path)