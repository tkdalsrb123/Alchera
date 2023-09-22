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

def makeJson(path, id, gender, age, language, logic, view, nature, music, individual, physical, review, q_a):
    json_tree = {}
    json_tree['object'] = [{"id":id, "gender":gender, "age":age}]
    json_tree['annotation'] = {"text":{"result":{
                                                "language":language, "logic":logic, "view":view, 
                                                 "nature":nature, "music":music, "individual":individual, 
                                                 "physical":physical, "review":review
                                                 }, 
                                       "q_a":q_a,
                                       }
                               }
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

def findNaN(n):
    if pd.isnull(n) == True:
        t = ""
    elif type(n) == float:
        t = str(int(n))
    else:
        t = n
    return t

def makeInfo(x, path):
    id = x.iloc[0]
    id = str(id).rjust(4, '0')
    gender = replaceText(x.iloc[1])
    age = replaceText(x.iloc[2])
    
    language = findNaN(x.iloc[3])
    logic = findNaN(x.iloc[4])
    view = findNaN(x.iloc[5])
    nature = findNaN(x.iloc[6])
    music = findNaN(x.iloc[7])
    individual = findNaN(x.iloc[8])
    physical = findNaN(x.iloc[9])
    review = findNaN(x.iloc[10])
    q_a = findNaN(x.iloc[11])
    

    makeJson(path, id, gender, age, language, logic, view, nature, music, individual, physical, review, q_a)
    
_, excel_dir, output_dir = sys.argv

logger = make_logger('log.log')
tqdm.pandas()

excel = pd.read_excel(excel_dir)
excel.progress_apply(makeInfo, axis=1, args=(output_dir,))