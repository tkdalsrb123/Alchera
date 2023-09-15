import os, sys, json
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

def readfiles(dir, type=None):
    if type == None:
        file_dict = defaultdict(str)
        for root, dirs, files in os.walk(dir):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.json':
                    file_path = os.path.join(root, file)

                    file_dict[filename] = file_path
    elif type == 'crop':
        file_dict = defaultdict(list)
        for root, dirs, files in os.walk(dir):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.json':
                    new_filename = '_'.join(filename.split('_')[:-1])
                    file_path = os.path.join(root, file)

                    file_dict[new_filename].append(file_path)
                    
    return file_dict

def openJson(path):
    logger.info(f"{path} 읽기")
    with open(path, encoding='utf-8') as f:
        json_file = json.load(f)
    
    return json_file

def saveJson(path, file):
    logger.info(f"{path} 저장")
    with open(path, 'w', encoding='utf-8') as o:
        json.dump(file, o, indent=2, ensure_ascii=False)
        
def makeOutputPath(file_path, file_dir, output_dir, file):
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

_, json_dir, crop_json_dir, output_dir = sys.argv

logger = make_logger('log.log')

json_dict = readfiles(json_dir)
crop_json_dict = readfiles(crop_json_dir, 'crop')

for filename, json_path in tqdm(json_dict.items()):
    crop_json_list = crop_json_dict.get(filename)
    if crop_json_list:
        output_json_path = makeOutputPath(json_path, json_dir, output_dir, f"{filename}.json")
        
        output_json = defaultdict(list)
        
        json_file = openJson(json_path)
        
        info = json_file['info']
        
        for obj in json_file['objects']:
            id = obj['id']
            classId = obj['classId']
            name = obj['name']
            bbox = obj['points']
            for crop_json_path in crop_json_list:
                crop_json_file = openJson(crop_json_path)

                points = crop_json_file['objects'][0]['points']
            
                output_json['objects'].append({"id":id, "classId":classId, "name":name, "bbox":bbox, "points":points})


        output_json['info'] = info

        saveJson(output_json_path, output_json)