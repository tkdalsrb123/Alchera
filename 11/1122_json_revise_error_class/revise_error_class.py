import os, sys, logging, json   
import pandas as pd
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
        
def readfiles(dir):
    file_dict = defaultdict(list)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()            
            if ext == '.json':
                folder = os.path.split(root)[-1]
                file_path = os.path.join(root, file)

                file_dict[folder].append(file_path)

    return file_dict

def get_objects(data):
    obj = data['objects']

    if type(obj) == dict:
        obj = [obj]

    return obj

def collect_objects(folder, path):
    data = readJson(path)
    obj = get_objects(data)
    for o in obj:
        _class = o['class']
        _sub_class1 = o["sub_class1"]
        _sub_class2 = o["sub_class2"]
        _id = o['HDP_VRFC']['id']
        
        count_dict[folder][_id].append({'path':path, 'class':_class, 'sub_class1':_sub_class1, 'sub_class2':_sub_class2})    

def revise_objects(count_dict, folder, path, output_path):
    data = readJson(path)
    if type(data['objects']) == list:
        for idx, o in enumerate(data['objects']):
            _id = o['HDP_VRFC']['id']
            value = count_dict[folder][_id]
            if data['objects'][idx]['class'] != value['class'] or data['objects'][idx]["sub_class1"] != value['sub_class1'] or data['objects'][idx]["sub_class2"] != value['sub_class2']:
                data['objects'][idx]['class'] = value['class']
                data['objects'][idx]["sub_class1"] = value['sub_class1']
                data['objects'][idx]["sub_class2"] = value['sub_class2']
                revise_list.append([path, output_path])

    elif type(data['objects']) == dict:
        _id = data['objects']['HDP_VRFC']['id']
        value = count_dict[folder][_id]

        if data['objects'][idx]['class'] != value['class'] or data['objects'][idx]["sub_class1"] != value['sub_class1'] or data['objects'][idx]["sub_class2"] != value['sub_class2']:
            data['objects']['class'] = value['class']
            data['objects']["sub_class1"] = value['sub_class1']
            data['objects']["sub_class2"] = value['sub_class2']
            revise_list.append([path, output_path])
            
    saveJson(data, output_path)
                
def get_max_value(_list, key):
    data = [i[key] for i in _list]
    val = max(set(data), key=data.count)
    return val
    
def sorted_dict(_dict):
    for f, _i in _dict.items():
        for i, c in _i.items():
            if len(c) <= 2:
                for j in c:
                    special_list.append([f, j['path'], i])
                
            _class = get_max_value(c, 'class')
            _sub_class1 = get_max_value(c, 'sub_class1')
            _sub_class2 = get_max_value(c, 'sub_class2')

            _dict[f][i] = {'class':_class, 'sub_class1':_sub_class1, 'sub_class2':_sub_class2}
    
    return _dict

def make_excel(_list, col, output_excel_path):
    df = pd.DataFrame(_list, columns=col)
    df.to_excel(output_excel_path, index=False)
                
if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('in_id_log.log')
    
    json_dict = readfiles(input_dir)

    count_dict = defaultdict(lambda : defaultdict(list))

    for folder, json_path_list in tqdm(json_dict.items(), desc='collecting id..!'):
        for json_path in json_path_list:
            logger.info(f"{json_path} collecting id")
            collect_objects(folder, json_path)
    
    special_list = []
    count_dict = sorted_dict(count_dict)
    
    revise_list = []
    for folder, json_path_list in tqdm(json_dict.items(), desc='revise class..!'):
        for json_path in json_path_list:
            logger.info(f"{json_path} revise class")
            output_json_path = makeOutputPath(json_path, input_dir, output_dir, 'json')
            revise_objects(count_dict, folder, json_path, output_json_path)
    
    make_excel(special_list, ['sequence', 'file_path', 'id'], f"{output_dir}/special_list.xlsx")
    make_excel(special_list, ['input_file_path', 'output_file_path'], f"{output_dir}/revise_list.xlsx")
    

    