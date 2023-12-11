import os, sys, cv2, json, logging
from collections import defaultdict
import numpy as np
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

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_img(img_path, img):
    ext = os.path.splitext(img_path)[-1]
    result, encoded_img = cv2.imencode(f'{ext}', img)
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)
            
R_category_colors = {
    1: (212, 166, 255),
    2: (3, 195, 253),
    3: (246, 155, 68),
    4: (144, 255, 255),
    5: (240, 120, 140),
}

E_category_colors = {
    1: (212, 166, 255),
    2: (246, 155, 85),    
    3: (240, 120, 140),
    4: (83, 179, 36),
    5: (144, 255, 255),
    6: (3, 195, 253)
}
            
if __name__ == '__main__':
    _, img_dir, json_dir, output_dir, thickness, alpha = sys.argv
    
    logger = make_logger('log.log')
    img_dict = readfiles(img_dir, ['.jpg', '.jpeg'])
    json_dict = readfiles(json_dir, ['.json'])
    
    alpha = float(alpha)
    for filename, json_path in tqdm(json_dict.items()):
        logger.info(json_path)
        img_path = img_dict[filename]
        output_img_path = makeOutputPath(img_path, img_dir, output_dir)
        data = readJson(json_path)
        
        cat_dict = {}
        for cat in data['Categories']:
            cat_dict[cat['id']] = cat['name']
            
        ann_dict = {}
        for ann in data['Annotations']:
            _id = ann['segments_info'][0]['category_id']
            seg = ann['segments_info'][0]['segmentation'][0]
            coordinates = [(seg[idx], seg[idx+1])for idx in range(0, len(seg), 2)]
            ann_dict[_id] = coordinates
        
        img = read_img(img_path)
        overlay = img.copy()
        for _id, coor in ann_dict.items():
            if filename.split('_')[0] == 'R':
                color = R_category_colors[_id]
            elif filename.split('_')[0] == 'E':
                color = E_category_colors[_id]
            text = cat_dict[_id]
            xymean = np.mean(coor, axis=0)
            
            pts = np.array(coor, dtype=np.int32)
            cv2.polylines(img, [pts], True, color, int(thickness))
            cv2.fillPoly(overlay, [pts], color)
            cv2.putText(img, text, (round(xymean[0]), round(xymean[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        img = cv2.addWeighted(overlay, alpha, img, 1-alpha, 0.0)
        save_img(output_img_path, img)