import cv2, os, sys, json
import logging
import numpy as np
from label import label
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

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def readfiles(dir, Ext):
    file_dict = defaultdict(str)
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

def save_img(img_path, img):
    result, encoded_img = cv2.imencode('.jpg', img)
    logger.info(f"{img_path} 저장!!")
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)
            
def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def select_color(key):
    color_mappings = {
    "metal_knife": (192, 192, 192),
    "metal_tongs": (128, 128, 128),
    "metal_forks": (169, 169, 169),
    "metal_spoon": (211, 211, 211),
    "metal_chopsticks": (169, 169, 169),
    "metal_ladle": (169, 169, 169),
    "metal_grater": (169, 169, 169),
    "eggs": (255, 255, 0),
    "chestnut": (139, 69, 19),
    "drumstick": (139, 69, 19),
    "chicken_wing": (244, 164, 96),
    "wedge_potato": (210, 105, 30),
    "shrimp": (255, 165, 0),
    "mackerel": (0, 0, 139),
    "chocolate_chip_cookie": (210, 105, 30),
    "madeleine": (244, 164, 96),
    "squid": (0, 0, 0),
    "abalone": (128, 128, 128),
    "vienna_sausage": (244, 164, 96),
    "triangle_rice_ball": (255, 255, 255),
    "chicken_tender": (244, 164, 96),
    "onion_ring": (139, 69, 19),
    "potato_hotdog": (210, 105, 30),
    "shrimp_toast": (255, 165, 0),
    "chili_shrimp": (255, 69, 0),
    "rolled_seaweed": (0, 128, 0),
    "chicken_skewers": (255, 69, 0),
    "buckweat_crepe": (139, 69, 19),
    "something1": (255, 0, 0),
    "something2": (0, 255, 0),
    "something3": (0, 0, 255),
    "something4": (255, 255, 0),
    "something5": (0, 255, 255),
    "something6": (255, 0, 255),
    "something7": (128, 0, 0),
    "something8": (0, 128, 0),
    "something9": (0, 0, 128),
    "something10": (128, 128, 0)
    }
    return color_mappings[key]

_, img_dir, json_dir, output_dir = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, '.jpg')
json_dict = readfiles(json_dir, '.json')

for filename, img_path in tqdm(img_dict.items()):
    json_path = json_dict.get(filename)
    if json_path:
        output_img_path = makeOutputPath(img_path, img_dir, output_dir, 'jpg')
        
        json_file = readJson(json_path)
        
        
        img = read_img(img_path)
        for obj in json_file['objects']:
            points = obj['points']
            name = obj['name']
            color = select_color(name)
            x1y1 = tuple([round(p) for p in points[0]])
            x2y2 = tuple([round(p) for p in points[1]])

            cv2.rectangle(img, x1y1, x2y2, color =color, thickness=3)
            img = label(img, name, 10, color, x1y1, 0.5)        
        save_img(output_img_path, img)
