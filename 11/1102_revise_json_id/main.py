import os, sys, json, logging
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

def readfiles(dir):
    file_list = []
    for root, dirs, files in os.walk(json_dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            index = filename.split('-')[-1]
            if ext == '.json':
                fil_path = os.path.join(root, file)
                file_list.append((index, filename, fil_path))
    return file_list

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def readJson(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def saveJson(file, path):
    with open(path, 'w') as f:
        json.dump(file, f, indent=2, ensure_ascii=False)
        

if __name__ == '__main__':
    _, json_dir, output_dir = sys.argv

    json_list = readfiles(json_dir)
    
    
    json_list = sorted(json_list, key=lambda x: int(x[0]))
    
    sequence_list = []
    s = 0
    for i in range(0, len(json_list)-1):
        if int(json_list[i][0])+1 != int(json_list[i+1][0]):
            sequence_list.append(json_list[s:i+1])
            s = i+1
        if i == len(json_list)-2:
            sequence_list.append(json_list[s:])
            
    for sequence in sequence_list:
        obj_list = []
        for json_data in sequence:
            data = readJson(json_data[2])
            obj_list.append((len(data['objects']), data['objects']))
        max_obj = max(obj_list, key=lambda x: x[0])[1]
        x_list = [obj['points'][1][0] for obj in max_obj]
        x_list = sorted(x_list)
        
        for json_data in sequence:
            data = readJson(json_data[2])
            
        
        