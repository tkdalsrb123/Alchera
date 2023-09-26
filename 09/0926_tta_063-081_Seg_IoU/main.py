import json, os, sys
import logging
from tqdm import tqdm
from collections import defaultdict
import pandas as pd
from shapely.geometry import Polygon
import time
import numpy as np


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
    
def readfiles(dir):
    file_dict = defaultdict(str)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.json':
                file_path = os.path.join(root, file)
                
                file_dict[filename] = file_path
                
    return file_dict

def openJson(path):
    with open(path, encoding='utf-8-sig') as f:
        json_file = json.load(f)
    
    return json_file

_, label_json_dir, treeD_json_dir, output_dir = sys.argv

label_json_dict = readfiles(label_json_dir)
treeD_json_dict = readfiles(treeD_json_dir)

df_list = []
for filename, label_json_path in tqdm(label_json_dict.items()):
    treeD_json_path = treeD_json_dict.get(filename)
    if treeD_json_path:
        label_json_file = openJson(label_json_path)
        treeD_json_file = openJson(treeD_json_path)

        for ann in label_json_file['annotations']:
            try:
                ann1 = [[round(ann['polygon'][i]), round(ann['polygon'][i+1])] for i in range(0, len(ann['polygon']), 2)]
                polygon1 = Polygon(ann1)
                iou_list = []
                for obj in treeD_json_file['objects']:
                    name = obj['name']
                    if name == '영역오류':
                        ann2 = [ [round(p[0]), round(p[1])] for p in obj['points']]
                        polygon2 = Polygon(ann2)
                        intersect = polygon1.intersection(polygon2).area
                        union = polygon1.union(polygon2).area
                        iou_val = intersect/union
                        iou_list.append(iou_val)
                
                        df_list.append([filename, name, max(iou_list)])
            except:
                pass
            
df = pd.DataFrame(df_list, columns=['파일명', '영역오류', 'IoU 값'])
df.to_excel(f'{output_dir}/IoU.xlsx', index=False)
