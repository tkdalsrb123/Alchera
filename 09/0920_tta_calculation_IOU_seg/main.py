import os, sys, json
import xmltodict
import logging 
from collections import defaultdict
import pandas as pd

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
            df_list.append([filename, poly['@label'], len(points), points])
    df = pd.DataFrame(df_list, columns=['filename', 'label', 'len', 'points'])
    return df 

_, standard_xml_dir, iou_xml_dir, save_dir = sys.argv

logger = make_logger('log.log')

standard_xml = readxml(standard_xml_dir)
iou_xml = readxml(iou_xml_dir)

st_df = make_df(standard_xml)
iou_df = make_df(iou_xml)

df = pd.merge(st_df, iou_df, 'outer', ['filename', 'label', 'len'])
a = df[df['filename'] == 'S_DCH_230725_0099_LF_034']
print(a['len'])