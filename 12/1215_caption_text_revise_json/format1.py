import os, sys, logging, json
from tqdm import tqdm
from collections import defaultdict

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
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(file, f, indent=2, ensure_ascii=False)

def get_true_value(values):
    for value in values:
        if value['selected'] == True:
            val = value['value']
    return val
def bbox_format(_id, _type, points, tabulization_count):
    bbox = {
        "id": _id,
        "type": _type,
        "points": points,
        "tabulization_count": tabulization_count
        }
        
    return bbox

def json_format(outline, total_count, bbox, output_path):
    tree  ={
    "objects": {
        "detail": [
            {
            "outline": outline,
            "total_count": total_count
            }
        ],
        "bbox": bbox
        }
    }
    
    saveJson(tree, output_path)
    
if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')

    json_dict = readfiles(input_dir, '.json')

    for filename, json_path in json_dict.items():
        logger.info(json_path)
        output_json_path = makeOutputPath(json_path, input_dir, output_dir, 'json')
        data = readJson(json_path)
        bbox_list = []
        for objects in data['objects']:
            if objects['name'] == '이미지 설명':
                for attributes in objects['attributes']:
                    if attributes['name'] == '개요(outline)':
                        outline = get_true_value(attributes['values'])
                    elif attributes['name'] == '캡션 가능한 그래프 개수(전체 이미지 내)':
                        total_count = get_true_value(attributes['values'])
            else:
                _id = objects['id']
                _type = objects['name']
                points = objects['points']
                tabulization_count = 0
                if objects['attributes']:
                    for attributes in objects['attributes']:
                        if attributes['name'] == '캡션 가능한 그래프 수(BBox 내)':
                            tabulization_count = get_true_value(attributes['values'])
                    
                bbox_list.append(bbox_format(_id, _type, points, tabulization_count))
        json_format(outline, total_count, bbox_list, output_json_path)