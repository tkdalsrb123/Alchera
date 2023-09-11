import cv2, json, os, sys
import logging
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont
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
    
    new_width = 0
    new_height = height + top
    
    result = Image.new(img.mode, (new_width, new_height), (255, 255, 255))
    
    result.paste(img, (0, top))

    return result

_, img_dir, json_dir, output_dir = sys.argv

img_dict = readfiles(img_dir, '.jpg')
json_dict = readfiles(json_dir, '.json')

for filename, img_path in tqdm(img_dict.items()):
    json_path = json_dict[filename]

    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)
    
    
    
    for image in json_file['annotations']['image']:
        text1 = image['classification']['class']
        have_case = image['classification'].get('case')
        if have_case != None:
            text2 = image['classification']['case']
            text = f'{text1}:{text2}'
        elif have_case == None:
            text = text1
    
    for image in json_file['annotationsData']['image']:
        coor =  [ (v['x'], v['y']) for v in image['coordinate']]
        
        