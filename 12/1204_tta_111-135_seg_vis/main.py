import os, sys, logging, cv2, json
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
    with open(path, 'r', encoding='utf-8') as f:
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

def center_point(polygon_coordinates):
    sum_x = 0
    sum_y = 0
    for point in polygon_coordinates:
        sum_x += point[0]
        sum_y += point[1]
    avg_x = sum_x / len(polygon_coordinates)
    avg_y = sum_y / len(polygon_coordinates)
    return (round(avg_x), round(avg_y))

category = {
"1":(151,219,242),
"2":(197,0,255),
"3":(0,0,0),
"4":(236,236,236),
"5":(255,192,0),
"6":(1,31,255),
"7":(1,141,255),
"8":(1,234,255),
"9":(1,255,31),
"10": (255,251,1),
"11": (255,1,9)}

if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')

    json_dict = readfiles(input_dir, '.json')
    img_dict = readfiles(input_dir, '.jpg')

    for filename, json_path in tqdm(json_dict.items()):
        logger.info(json_path)
        img_path = img_dict[filename]
        output_img_path = makeOutputPath(img_path, input_dir, output_dir, 'jpg')
        img = read_img(img_path)
        overlay = img.copy()
        data = readJson(json_path)

        for annotations in data['ANNOTATIONS']:
            _id = annotations['ID']
            coordinate = annotations['COORDINATE']
            
            color = category.get(_id)
            if color is None:
                color = (55,125,247)
            color = (color[2], color[1], color[0])
            pts = [[round(coor[0]), round(coor[1])] for coor in coordinate]
            center = center_point(pts)
            pts = np.array(pts, dtype=np.int32)

            cv2.fillPoly(overlay, [pts], color)
            cv2.putText(img, _id, center, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0 ,0), 3)
        result = cv2.addWeighted(img, 0.5, overlay, 0.5, 0.0)
            
        save_img(output_img_path, result, 'jpg')
