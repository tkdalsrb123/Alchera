import json, os, sys
from collections import defaultdict, OrderedDict
import logging
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
                file_path = os.path.join(root, file)

                file_dict[filename] = file_path
    return file_dict

def reviseJson(JsonPath):
    with open(JsonPath, encoding='utf-8') as f:
        json_file = json.load(f)

    x_list = []
    y_list = []
    coor_list = []
    json_dict = {}
    for point in json_file["points"]:
        coor_list.append([float(point['points']['x']), float(point['points']['y'])])
        x_list.append(float(point['points']['x']))
        y_list.append(float(point['points']['y']))
    
    box_x = min(x_list)
    box_y = min(y_list)
    box_w = max(x_list) - box_x
    box_h = max(y_list) - box_y

    json_dict['box'] = {'x':box_x, 'y':box_y, 'w':box_w, 'h':box_h}
    json_dict['points'] = coor_list
    
    return json_dict

_, A_dir, B_dir, output_dir = sys.argv

logger = make_logger('log.log')

A_dict = readfiles(A_dir)
B_dict = readfiles(B_dir)

for filename, ajson_path in tqdm(A_dict.items()):
    have_json = B_dict.get(filename)
    if have_json != None:
        logger.info(filename)
        root, file = os.path.split(ajson_path)
        mid = '\\'.join(root.split('\\')[len(A_dir.split('\\')):])
        folder = os.path.join(output_dir, mid)
        os.makedirs(folder, exist_ok=True)
        output_json_path = os.path.join(folder, file)
        
        bjson_path = B_dict[filename]
        
        ajson_dict = reviseJson(ajson_path)
        bjson_dict = reviseJson(bjson_path)

        merge_json = [ajson_dict, bjson_dict]
        
        logger.info(f"{output_json_path} 저장!!")
        with open(output_json_path, 'w', encoding='utf-8') as o:
            json.dump(merge_json, o, indent=2, ensure_ascii=False)