import json, os, sys
import logging
from tqdm import tqdm
from collections import defaultdict
import pandas as pd
from shapely.geometry import Polygon
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

def openJson(path):
    with open(path, encoding='utf-8-sig') as f:
        json_file = json.load(f)
    
    return json_file

if __name__ == "__main__":
    _, source_dir, treed_dir, output_dir = sys.argv

    logger = make_logger('log.log')
    source_dict = readfiles(source_dir, '.json')
    treed_dict = readfiles(treed_dir, '.json')

    iou_list = []
    for filename, source_path in tqdm(source_dict.items()):
        logger.info(filename)
        treed_path = treed_dict[filename]
        
        source_data = openJson(source_path)
        treed_data = openJson(treed_path)

        for obj in treed_data['objects']:
            name = obj['name']
            if name == '영역오류':
                ann_list = source_data['image_inside_info']['annotations']
                if ann_list:
                    for ann in ann_list:
                        source_points = [[round(poly['x']), round(poly['y'])] for poly in ann['polygon_info']]
                        treed_points = [[round(p[0]), round(p[1])] for p in obj['points']]
                        try:
                            polygon1 = Polygon(treed_points)
                            polygon2 = Polygon(source_points)
                            intersect = polygon1.intersection(polygon2).area
                            union = polygon1.union(polygon2).area
                            iou_val = intersect/union
                            if iou_val > 0:
                                iou_list.append([filename, iou_val])
                        except:
                            print(filename)
                    
    df = pd.DataFrame(iou_list, columns=['filename', 'IoU'])
    df.to_csv(f"{output_dir}/IoU_list.csv", index=False)