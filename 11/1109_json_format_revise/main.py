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
            new_filename = '_'.join(filename_split)
            ext = ext.lower()   
            if ext == '.json':
                file_path = os.path.join(root, file)
                if type == 'bbox':
                    file_dict[new_filename].append(file_path)
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

def jsonTree(imageName):
    info = {
        "imageName": imageName,
        "width": "",
        "height": "",
        "labeler": "",
        "examinator": "",
        "timestamp": "",
        "format": "JPG",
        "fileSize": "",
        "dirPath": "",
        "projectName": "사물 세그멘테이션 검수",
        "taskName": "test3"}
    
    return info

def get_classId(key):
    id = {
    "Object_segmentation":"a279da37-a4d2-4105-81f3-ab92e2917cc3",
    "Shadow_segmentation":"3eea1feb-282d-476a-bdb9-30bbdfffb747",
    "contact_line":"3cddd9fd-9085-4093-81ac-fc2dfc2031c6",
    "Void":"e97c8829-2902-4461-a8a2-a84cce895765",
    "contact_line_polygon":"8f710a88-7cbb-4ed1-9cd4-1368374d20b0"
    }
    
    val = id[key]

    return val

if __name__ == '__main__':
    _, bbox_dir, polygon_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    
    bbox_dict = readfiles(bbox_dir, 'bbox')
    polygon_dict = readfiles(polygon_dir, 'polygon')
    
    for filename, polygon_path in tqdm(polygon_dict.items()):
        filename_split = filename.split('_')
        filename_split.pop(3)
        new_filename = '_'.join(filename_split)
        bbox_path_list = bbox_dict.get(new_filename)

        tree = {"objects": [],
                "info": None}
        output_json_path = makeOutputPath(polygon_path, polygon_dir, output_dir, 'json')
        logger.info(output_json_path)
        polygon_data = readJson(polygon_path)
        
        for data in polygon_data:
            obj = data['objects']
            if type(obj) == dict:
                obj = [obj]
            for o in obj:
                o['classId'] = get_classId(o['name'])
                tree['objects'].append(o)
                
        if bbox_path_list:
            for bbox_path in bbox_path_list:
                logger.info(bbox_path)
                bbox_data = readJson(bbox_path)
                for bbox_obj in bbox_data['objects']:
                    bbox_obj['classId'] = get_classId(bbox_obj['name'])
                    tree['objects'].append(bbox_obj)
                    
        info = jsonTree(f"{filename}.JPG")
        tree['info'] = info
            
        saveJson(tree, output_json_path)
        logger.info(output_json_path)