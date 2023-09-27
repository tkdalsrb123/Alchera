import json, os, sys
import pandas as pd
import logging
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

def readfiles(dir):
    file_dict = defaultdict(str)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.json':
                filename = filename.split('.')[0]
                file_path = os.path.join(root, file)

                file_dict[filename] = file_path
    return file_dict

def matching_dict(x):
    split_x = x.split('\t')
    info_dict[split_x[0]] = split_x[1:]

def openJson(path):
    logger.info(path)
    with open(path, encoding='utf-8') as f:
        file = json.load(f)

    return file

def saveJson(output_path, file):
    logger.info(f"{output_path} 저장!!")
    with open(output_path, 'w', encoding='utf-8') as o:
        json.dump(file, o, indent=2, ensure_ascii=False)

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def jsonTree(filename, points, score, output_path):
    tree = {
                "filename": {
                    "img_filename": f"{filename}.png",
                    "json_filename": f"{filename}.alchera.json",
                    "전문가평가데이터_filename": os.path.split(csv_dir)[-1],
                },
                "Bounding_Box": {
                    "x": 2.701710671647504,
                    "y": 112.86405618591141,
                    "w": 762.6147523424958,
                    "h": 800.3342869979143,
                },
                "Point": points,
                "expert_evaluation_data":{
                    "항목1": int(score[0]),
                    "항목2": int(score[1]),
                    "항목3": int(score[2]),
                    "항목4": int(score[3]),
                    "항목5": int(score[4]),
                    "항목6": int(score[5]),
                }
    }
    saveJson(output_path, tree)
if __name__ == '__main__':
    
    _, json_dir, csv_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    
    df = pd.read_csv(csv_dir, encoding='utf-8', header=None)
    info_dict = {}
    df.iloc[:, 0].apply(matching_dict)

    json_dict = readfiles(json_dir)

    for filename, json_path in tqdm(json_dict.items()):
        
        output_json_path = makeOutputPath(json_path, json_dir, output_dir)
        score = info_dict[filename]

        json_file = openJson(json_path)
        
        points = json_file[0]['points']
        points = [{"x":p[0], "y":p[1]}for p in points]
        
        jsonTree(filename, points, score, output_json_path)
        