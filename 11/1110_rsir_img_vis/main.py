import os, sys, json, cv2, logging
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
            if Ext == '.json':
                if ext == Ext and 'Property' in filename:
                    file_path = os.path.join(root, file)
                
                    file_dict[filename] = file_path
            elif Ext == '.png':
                if ext == Ext:
                    file_path = os.path.join(root, file)
                
                    file_dict[filename] = file_path
    return file_dict

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_img(img_path, img, ext):
    result, encoded_img = cv2.imencode(f'.{ext}', img)
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)
            
if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    
    json_dict = readfiles(input_dir, '.json')
    img_dict = readfiles(input_dir, '.png')

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = int(1)
    
    data_dict = {}
    for filename, json_path in tqdm(json_dict.items(), desc='extract json info'):
        logger.info(json_path)
        data = readJson(json_path)

        for d in data:
            data_dict[d['Source']] = [d['Location'], d['RoadType'], d['IlluminationCondition']]
            
    
    for filename, data in tqdm(data_dict.items(), desc='image visualization'):
        new_filename = os.path.splitext(filename)[0]
        img_path = img_dict[new_filename]
        logger.info(img_path)

        output_img_path = makeOutputPath(img_path, input_dir, output_dir, "jpg")

        img = read_img(img_path)
        text_list = [f"Source:{filename}", f"Location: {data[0]}", f"RoadType: {data[1]}", f"IlluminationCondition: {data[2]}"]
        
        h = 50
        for text in text_list:
            cv2.putText(img, text, (50,h), fontFace=font, fontScale=fontScale, color=(255,255,255), thickness=2, lineType=cv2.LINE_AA)
            h += 30
        
        save_img(output_img_path, img, "jpg") 
        logger.info(output_img_path)