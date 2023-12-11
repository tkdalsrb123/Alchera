import os, sys, logging, json
import pandas as pd
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

def readfiles(dir, Ext):
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext == Ext:
                seq = os.path.split(root)[-1]
                file_path = os.path.join(root, file)
            
                file_dict[seq].append(file_path)
    return file_dict

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data 

def make_xlsx(_list, col, output_path):
    df = pd.DataFrame(_list, columns=col)
    df.to_excel(output_path, index=False)
    
if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    json_dict = readfiles(input_dir, '.json')

    class_dict = defaultdict(list)
    for sequence, json_path_list in tqdm(json_dict.items(), desc='read sequence', position=0):
        for json_path in tqdm(json_path_list, desc='read json files', position=1):
            data = readJson(json_path)

            for obj in data['objects']:
                _class = obj['class']
                sub_class = obj['sub_class1']
                class_dict[sequence].append([_class, sub_class])
                include_class = obj.get('include_class')
                if include_class:
                    for classname, info_list in include_class.items():
                        if include_class[classname]:
                            for info in info_list:
                                _class = info['class']
                                sub_class = info['sub_class1']
                                class_dict[sequence].append([_class, sub_class])
    
    df2list = []
    for sequence, class_list in tqdm(class_dict.items(), desc='counting class'):
        whole_count = len(class_list)
        ptw_moto = 0
        emergency_whole = 0
        car = 0
        vehicle_whole = 0
        for _class in class_list:
            if 'Emergency' in _class[0]:
                if 'motocycle' in _class[1]:
                    ptw_moto += 1
                else:
                    emergency_whole += 1
                
            elif 'Vehicle' in _class[0]:
                if _class[1] in ['truck', 'van', 'bus']:
                    car += 1
                else:
                    vehicle_whole += 1
                    
            elif 'ptw' in _class[0]:
                ptw_moto += 1

        df2list.append([sequence, whole_count, ptw_moto, emergency_whole, car, vehicle_whole])

    make_xlsx(df2list, ['sequence', 'whole', 'emergency', 'vehicle', 'truck-van-bus', 'ptw-motocycle'], f"{output_dir}/class_counting.xlsx")
    
    