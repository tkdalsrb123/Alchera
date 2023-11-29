import os, sys, cv2, json, logging
import numpy as np
from tqdm import tqdm
from label import label
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


def vis(img, vis_list, _type):
    for vis in vis_list:
        text = vis['class']['level1'] + '_' + vis['class']['level2'] +'_' + vis['class']['level3']
        if _type == 'bbox':
            x1 = vis['left']['top']['x']
            y1 = vis['left']['top']['y']
            x2 = vis['right']['bottom']['x']
            y2 = vis['right']['bottom']['y']
            
            cv2.rectangle(img, (x1, y1), (x2, y2), color=colors_bgr[vis['class']['level1']], thickness=3)
            img = label(img, text, font_size, font_color, (x1,y1), 0.0)
            
        elif _type == 'polygon':
            pts = [ [p['x'],p['y']] for p in vis['point_list']]
            pts = np.array(pts, dtype=np.int32)
            
            cv2.polylines(img, [pts], True, colors_bgr[vis['class']['level1']], thickness=3)
            img = label(img, text, font_size, font_color, pts[0], 0.0)
            
        elif _type == 'polyline':
            pts = [ [p['x'],p['y']] for p in vis['point_list'][0]]
            pts = np.array(pts, dtype=np.int32)

            cv2.polylines(img, [pts], False, colors_bgr[vis['class']['level1']], thickness=3)
            img = label(img, text, font_size, font_color, pts[0], 0.0)
    
    return img
            
font_size = 5
font_color = (0, 0, 0)
            
colors_bgr = {
    'Vehicle': (0, 0, 255),       # 빨간색
    'Pedestrian': (0, 255, 255),  # 노란색
    'TrafficLight': (255, 0, 0),  # 파란색
    'RoadSign': (0, 255, 0),      # 연두색
    'Line': (255, 0, 255),        # 보라색
    'Structure': (0, 165, 255)    # 주황색
}

if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    json_dict = readfiles(input_dir, '.json')
    img_dict = readfiles(input_dir, '.png')

    for filename, json_path in tqdm(json_dict.items()):
        img_path = img_dict[filename]
        output_img_path = makeOutputPath(img_path, input_dir, output_dir, 'png')

        data = readJson(json_path)
        bbox_list = data['label_data'].get('2d_bounding_box')
        polygon_list = data['label_data'].get('polygon')
        polyline_list = data['label_data'].get('polyline')
        
        img = read_img(img_path)

        if bbox_list:
            img = vis(img, bbox_list, 'bbox')
        if polygon_list:
            img = vis(img, polygon_list, 'polygon')
        if polyline_list:
            img = vis(img, polyline_list, 'polyline')

        save_img(output_img_path, img, 'png')