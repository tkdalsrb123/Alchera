import cv2, os, sys, json
import logging
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
            if Ext == 'json':
                if ext == '.json':
                    filename = '_'.join(filename.split('_')[:-1])
                    file_path = os.path.join(root, file)

                    file_dict[filename].append(file_path)
            elif Ext == 'img':
                if ext == '.jpg' or ext == '.jpeg':
                    file_path = os.path.join(root, file)

                    file_dict[filename] = file_path
                    
    return file_dict


def make_output_path(input_path, file_path, output_path):
    root, file = os.path.split(file_path)
    mid = '\\'.join(root.split('\\')[len(input_path.split('\\')):])
    folder= os.path.join(output_path, mid)
    os.makedirs(folder, exist_ok=True)
    output_file_path = os.path.join(folder, file)
    return output_file_path


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

def select_color(facePart):
    if facePart == 'forehead':
        color = (0,0,255)
    elif facePart == "glabellus":
        color = (255,255,0)
    elif facePart == 'l_perocular':
        color = (255,0,0)
    elif facePart == 'r_perocular':
        color = (0,255,255)
    elif facePart == 'l_cheek':
        color = (47,255,173)
    elif facePart == 'r_cheek':
        color = (255,0,255)
    elif facePart == 'lip':
        color = (0,128,0)
    elif facePart == 'chin':
        color = (0,165,255)

    return color

def select_thickness(facePart):
    if facePart == 'glabellus':
        thickness = 30
    elif facePart == 'l_perocular':
        thickness = 15
    elif facePart == 'r_perocular':
        thickness = 5
    else:
        thickness = 5
    
    return thickness
    
_, img_dir, json_dir, output_dir = sys.argv

logger = make_logger('log.log')

json_dict = readfiles(json_dir, 'json')
img_dict = readfiles(img_dir, 'img')

for filename, img_path in tqdm(img_dict.items()):
    json_path_list = json_dict[filename]

    img = read_img(img_path)
    
    output_img_path = make_output_path(img_dir, img_path, output_dir)
    for json_path in json_path_list:
        logger.info(json_path)
        with open(json_path, encoding='utf-8') as f:
            json_file = json.load(f)
        
        facepart = json_file['images']['facepart']
        x1y1 = tuple(json_file['images']['bbox'][:2])
        x2y2 = tuple(json_file['images']['bbox'][2:])

        color = select_color(facepart)
        thickness = select_thickness(facepart)
        cv2.rectangle(img, x1y1, x2y2, color=color, thickness=thickness)

    save_img(output_img_path, img)