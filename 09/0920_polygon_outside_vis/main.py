import cv2, os, sys, json
import logging
import numpy as np
from tqdm import tqdm
from collections import defaultdict
from PIL import Image, ImageFont, ImageDraw, ImageOps


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

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def tag_name(type, code):
    if type == 'growth':
        if code == 0:
            text = '종자생산'
        elif code == 1:
            text = '중간양성'
        elif code == 2:
            text = '어미성숙'
            
    elif type == 'farm':
        if code == 0:
            text = '일반양식장'
        elif code == 1:
            text = '생태양식장'
            
    elif type == 'mig':
        if code == 0:
            text = '성숙단계'
        elif code == 1:
            text = '성숙완료'
        elif code == 2:
            text = '자어'
        elif code == 3:
            text = '치어'
        elif code == 4:
            text = '중간양성'
        elif code == 5:
            text = '추가양성'
    
    return text

def make_text(code, gtext, mtext, ftext):
    if code == 0 or code == 2:
        text = f"{gtext}-{mtext}"
    elif code == 1:
        text = f"{gtext}-{ftext}-{mtext}"
    
    return text

def minmaxCoor(coor, xy, type):
    x = [c[0] for c in coor]
    y = [c[1] for c in coor]
    if xy == 'x' and type == 'min':
        co = min(x)
    elif xy == 'y' and type == 'min':
        co = min(y)
    elif xy == 'x' and type == 'max':
        co = max(x)
    elif xy == 'y' and type == 'max':
        co = max(y)

    return co

_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

json_dict = readfiles(input_dir, '.json')
img_dict = readfiles(input_dir, '.jpg')

for filename, img_path in tqdm(img_dict.items()):
    json_path = json_dict[filename]

    output_img_path = makeOutputPath(img_path, input_dir, output_dir)
    with open(json_path, encoding='utf-8-sig') as f:
        json_file = json.load(f)
    
    img = read_img(img_path)
    h, w, _ = img.shape
    
    growth_code = json_file['info']['growth_stage']
    g_text = tag_name('growth', json_file['info']['growth_stage'])
    m_text = tag_name('mig', json_file['info']['migguri_type'])
    f_text = tag_name('farm', json_file['info']['farm_environment'])

    text = make_text(growth_code, g_text, m_text, f_text)
    
    for seg in json_file['segmentation']:
        polygon = seg['polygon']
        min_x = round(minmaxCoor(polygon, 'x', 'min'))-5
        min_y = round(minmaxCoor(polygon, 'y', 'min'))-5
        max_x = round(minmaxCoor(polygon, 'x', 'max'))+5
        max_y = round(minmaxCoor(polygon, 'y', 'max'))+5

        cv2.polylines(img, np.int32([[polygon]]), False, (255,255,0), 5, cv2.LINE_AA)

        cv2.line(img, (min_x, 0), (min_x, h), (0, 0, 255))
        cv2.line(img, (max_x, 0), (max_x, h), (0, 0, 255))
        cv2.line(img, (0, min_y), (w, min_y), (0, 0, 255))
        cv2.line(img, (0, max_y), (w, max_y), (0, 0, 255))

    font = ImageFont.truetype('malgunbd.ttf', 30)

    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    
    draw.text((5,5), text , (0,0,255), font)
    
    img = np.array(img)
    
    save_img(output_img_path, img)