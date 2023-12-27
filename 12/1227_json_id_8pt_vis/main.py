import os, sys, json, logging, cv2, random
import numpy as np
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
    with open(path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    return data 

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_img(img_path, img, ext):
    result, encoded_img = cv2.imencode(f'.{ext}', img)
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)
            
def random_rgb():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    
    return (blue, green, red)

if __name__ == "__main__":
    _, img_dir, json_dir, output_dir = sys.argv

    img_dict = readfiles(img_dir, '.png')
    json_dict = readfiles(json_dir, '.json')

    for filename, img_path in tqdm(img_dict.items()):
        output_img_path = makeOutputPath(img_path, img_dir, output_dir, 'png')
        json_path = json_dict[filename]

        data = readJson(json_path)
        img = read_img(img_path)
        for obj in data['object']:
            points = [(round(float(point.split(',')[0])), round(float(point.split(',')[1]))) for point in obj['cuboid']['points'].values()]
            color = random_rgb()
            for point in points:
                cv2.circle(img, point, 5, color, -1)
                
        save_img(output_img_path, img, 'png')