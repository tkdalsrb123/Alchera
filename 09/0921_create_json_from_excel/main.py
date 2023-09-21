import os, sys, json
import pandas as pd
import logging
from tqdm import tqdm
import numpy as np
import math

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

def makeJson(path, id, gender, age, result, qa):
    json_tree = {}
    json_tree['object'] = [{"id":id, "gender":gender, "age":age}]
    json_tree['annotation'] = {"text":{"result":result, "q_a":qa,}}
    logger.info(f"{path}/{id}.json")
    with open(f"{path}/{id}.json", 'w', encoding='utf-8') as o:
        json.dump(json_tree, o, indent=2, ensure_ascii=False)

def replaceText(t):
    text = ""
    if type(t) == str:
        t = t.replace(' ', '')
        if t == '남':
            text = 'male'
        elif t == '여':
            text = 'female'
        elif '세' in t:
            text = t.replace('세', '')
    return text


def makeInfo(x, path):
    id = x.iloc[0]
    id = str(id).rjust(4, '0')
    gender = replaceText(x.iloc[12])
    age = replaceText(x.iloc[11])
    result = ""
    qa = ""
    if type(x['result']) != float: 
        result = x['result']
    if type(x['q_a']) != float: 
        qa = x['q_a']

    makeJson(path, id, gender, age, result, qa)
    
_, excel_dir, output_dir = sys.argv

logger = make_logger('log.log')
tqdm.pandas()

excel = pd.read_excel(excel_dir)
excel.progress_apply(makeInfo, axis=1, args=(output_dir,))