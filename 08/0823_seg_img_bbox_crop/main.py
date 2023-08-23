import cv2, os, sys
import xmltodict
import pandas as pd
import numpy as np
from collections import defaultdict
from tqdm import tqdm
import logging

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

def read_files(path, Ext):
    if Ext == 'img':
        file_dict = defaultdict(str)
        for root, dirs, files in os.walk(path):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.png' or ext == '.jpg':
                    file_path = os.path.join(root, file)
                    file_dict[file] = file_path
        
        return file_dict
    
    elif Ext == 'xml':
        file_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.xml':
                    file_path = os.path.join(root, file)
                    file_list.append(file_path)

        return file_list


def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

_, img_dir, xml_dir, excel_dir, output_dir = sys.argv

logger = make_logger('log.log')

excel = pd.read_excel(excel_dir)
Class = list(map(eval, excel['class'].values))

img_dict = read_files(img_dir, 'img')
xml_list = read_files(xml_dir, 'xml')

for xml_path in tqdm(xml_list, desc='xml', position=0):
    xml_file = readxml(xml_path)

    for image in tqdm(xml_file['annotations']['image'], desc='image', position=1, leave=False):
        have = image.get('polygon') 
        if have != None:        # polygon이 있을 경우
            img_name = image["@name"]
            
            img_path = img_dict[img_name]

            if img_path != '':      # 이미지가 존재할 경우
                logger.info(img_path)
                img = read_img(img_path)
                height, width, _ = img.shape
                
                mask = np.zeros((height, width), dtype=np.uint8)
                
                if type(image['polygon']) == list:
                    i=0
                    for poly in image['polygon']:
                        label = poly['@label']

                        if label in Class:
                            filename, ext = os.path.splitext(img_name)
                            file_num = str(i).zfill(3)
                            folder = os.path.join(output_dir, label)
                            os.makedirs(folder, exist_ok=True)
                            output_file_path = os.path.join(folder, f'{filename}_{file_num}{ext}')
                            
                            coor = poly['@points']
                            split_list = coor.split(';')
                            coor_list = list(map(lambda x: x.split(','), split_list))
                            pts = np.array([[[round(float(i[0])), round(float(i[1]))] for i in coor_list]])
                            cv2.fillPoly(mask, pts, (255))
                            
                            res = cv2.bitwise_and(img, img, mask = mask)
                            rect = cv2.boundingRect(pts)
                            cropped = res[rect[1]: rect[1] + rect[3],  rect[0]: rect[0] + rect[2]]
                            
                            result, n = cv2.imencode(ext, cropped)
                            
                            if result:
                                with open(output_file_path, mode='w+b') as f:
                                    n.tofile(f)
                            
                            i += 1
                            
                elif type(image['polygon']) == dict:
                    label = image['polygon']
                    
                    if label in Class:
                        filename, ext = os.path.splitext(img_name)
                        file_num = str(i).zfill(3)
                        folder = os.path.join(output_dir, label)
                        os.makedirs(folder, exist_ok=True)
                        output_file_path = os.path.join(folder, f'{filename}_{file_num}{ext}')
                        
                        coor = image['polygon']['@points']
                        split_list = coor.split(';')
                        coor_list = list(map(lambda x: x.split(','), split_list))
                        pts = np.array([[[round(float(i[0])), round(float(i[1]))] for i in coor_list]])
                        cv2.fillPoly(mask, pts, (255))
                        
                        res = cv2.bitwise_and(img, img, mask = mask)
                        rect = cv2.boundingRect(pts)
                        cropped = res[rect[1]: rect[1] + rect[3],  rect[0]: rect[0] + rect[2]]
                        
                        result, n = cv2.imencode(ext, cropped)
                        
                        if result:
                            with open(output_file_path, mode='w+b') as f:
                                n.tofile(f)

                    
        