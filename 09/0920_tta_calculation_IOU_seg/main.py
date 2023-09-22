import os, sys, json
import xmltodict
import logging 
from collections import defaultdict
import pandas as pd
from shapely.geometry import Polygon
import time
from tqdm import tqdm
import numpy as np

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data

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

def make_df(xml):
    df_list = []
    for image in xml['annotations']['image']:
        filename = image['@name'].split('.')[0]
        for poly in image['polygon']:
            points = [po.split(',') for po in poly['@points'].split(';')]
            points = [[round(float(p[0])), round(float(p[1]))] for p in points]
            df_list.append([filename, poly['@label'], points])
    df = pd.DataFrame(df_list, columns=['filename', 'label', 'points'])
    return df 

def makeSeg(seg1, seg2):
    seg1 = [ [int(p[0]), int(p[1])] for p in seg1 ]
    seg2 = [ [int(p[0]), int(p[1])] for p in seg2 ]
    seg1_max_x = max(seg1, key=lambda p: p[0])[0]
    seg1_max_y = max(seg1, key=lambda p: p[1])[1]
    seg2_max_x = max(seg2, key=lambda p: p[0])[0]
    seg2_max_y = max(seg2, key=lambda p: p[1])[1]
    max_x = max(seg1_max_x, seg2_max_x)
    max_y = max(seg1_max_y, seg2_max_y)
    
    return max_x, max_y

def findIOU(x):
    label = x['label']
    st_points = x['points']
    iou_points = iou.loc[iou['label'] == label, 'points'].values
    iou_list = []
    for iou_point in iou_points:
        try:
            polygon1 = Polygon(st_points)
            polygon2 = Polygon(iou_point)
            intersect = polygon1.intersection(polygon2).area
            union = polygon1.union(polygon2).area
            iou_val = intersect/union
            iou_list.append(iou_val)
        except:
            print(filename, label)
        # max_x, max_y = makeSeg(st_points, iou_point)
        # bg_cv2 = np.zeros([max_x+1,max_y+1],dtype=np.uint8)
        # seg1_cv2 = visual.seg(bg_cv2, st_points, -1, (255, 255, 255), alpha=0.0)
        # seg2_cv2 = visual.seg(bg_cv2, iou_point, -1, (255, 255, 255), alpha=0.0)
        # intersection = np.logical_and(seg1_cv2, seg2_cv2)
        # union = np.logical_or(seg1_cv2, seg2_cv2)
        # a = np.sum(intersection)/np.sum(union)
        # print(a)
        # iou_list.append(np.sum(intersection)/np.sum(union))
    # print('----------------')
        
    df_list.append([filename, label, max(iou_list)])
    
    


_, standard_xml_dir, iou_xml_dir, save_dir = sys.argv

logger = make_logger('log.log')

standard_xml = readxml(standard_xml_dir)
iou_xml = readxml(iou_xml_dir)

st_df = make_df(standard_xml)
iou_df = make_df(iou_xml)

filename_list = st_df['filename'].unique()

df_list = []
for filename in tqdm(filename_list):
    st = st_df[st_df['filename'] == filename]
    iou = iou_df[iou_df['filename'] == filename]

    st.apply(findIOU, axis=1)

# df = pd.DataFrame(df_list, columns=['filename', 'label', 'IOU'])
# df.to_excel(f'{save_dir}/iou.xlsx', index=False)