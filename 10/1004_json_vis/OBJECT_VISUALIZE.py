import json, cv2, os, sys
import logging
import numpy as np
from collections import defaultdict
from tqdm import tqdm

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

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.jpg")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def select_color(name):
    if name == 'contact_line' or name == 'contact_line_2':
        color = (0, 0, 255)
    elif name == 'Object_segmentation':
        color = (255, 0, 0)
    elif name == 'Shadow_segmentation':
        color = (193, 182, 255)
    elif name == "Void":
        color = (0, 0, 0)
    
    return color

def contact_line(box_point,obj_seg_points):
    box_points = np.array(box_point)
    x_points = []
    y_points = []
    contact_points = []
    #print(box_points)
    for point in box_points:
        x,y = point
        x_points.append(x)
        y_points.append(y)
    for one_point in obj_seg_points:
        x,y = one_point
        if min(x_points)<=x and max(x_points)>=x and min(y_points)<=y and max(y_points)>=y:
            contact_points.append(one_point)
    contact_points = np.array(contact_points, np.int32)
    return contact_points

if __name__ == "__main__":

    _, img_dir, json_dir, output_dir = sys.argv

    logger = make_logger('log.log')

    seq = ["Shadow_segmentation", "Object_segmentation", "Void", "contact_line", "contact_line_2"]
    img_dict = readfiles(img_dir, '.jpg')
    json_dict = readfiles(json_dir, '.json')
    
    for filename, img_path in tqdm(img_dict.items()):
        json_path = json_dict.get(filename)
        if json_path:
            output_img_path = makeOutputPath(img_path, img_dir, output_dir)
            with open(json_path, encoding='utf-8') as f:
                json_file = json.load(f)
            
            img = read_img(img_path)
            w, h, _ = img.shape
            canvas = np.zeros((h, w, 3), np.uint8)
            vis_dict = defaultdict(list)
            for obj in json_file['objects']:
                name = obj['name']
                points = obj['points']
                
                vis_dict[name].append(points)

            for obj_name in seq:
                obj_points_list = vis_dict.get(obj_name)
                color = select_color(obj_name)
                if obj_points_list:
                    for obj_points in obj_points_list:
                        obj_points = [[round(p[0]), round(p[1])] for p in obj_points]
                        if len(obj_points) > 2:
                            obj_points = np.array(obj_points, np.int32)
                            cv2.fillPoly(canvas, [obj_points], color)
                        elif len(obj_points) <= 2:
                            for obj_seg_points in vis_dict['Object_segmentation']:
                                contact_points = contact_line(obj_points, obj_seg_points)
                                cv2.polylines(canvas, [contact_points], False, color, 10)
            
            save_img(output_img_path, canvas)
                
                