import os, sys, json, logging
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

def readfiles(dir, type):
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            filename_split = filename.split('_')
            filename_split.pop(3)
            filename = '_'.join(filename_split)
            ext = ext.lower()   
            if ext == '.json':
                file_path = os.path.join(root, file)
                if type == 'bbox':
                    file_dict[filename].append(file_path)
                elif type == 'polygon':
                    file_dict[filename] = file_path
                    
    return file_dict

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def saveJson(file, path):
    with open(path, 'w') as f:
        json.dump(file, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    _, bbox_dir, polygon_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    
    bbox_dict = readfiles(bbox_dir, 'bbox')
    polygon_dict = readfiles(polygon_dir, 'polygon')
    
    for filename, polygon_path in tqdm(polygon_dict.items()):
        bbox_path_list = bbox_dict.get(filename)
        if bbox_path_list:
            tree = {"objects": []}
            output_json_path = makeOutputPath(polygon_path, polygon_dir, output_dir, 'json')
            logger.info(output_json_path)
            polygon_data = readJson(polygon_path)
            
            for data in polygon_data:
                obj = data['objects']
                if type(obj) == dict:
                    obj = [obj]
                for o in obj:
                    tree['objects'].append(o)

            for bbox_path in bbox_path_list:
                logger.info(bbox_path)
                bbox_data = readJson(bbox_path)
                for bbox_obj in bbox_data['objects']:
                    tree['objects'].append(bbox_obj)
                    
                
            saveJson(tree, output_json_path)
            logger.info(output_json_path)