import os, sys, logging, json, shutil
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
    file_dict = defaultdict(lambda : defaultdict(list))

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext == Ext:
                num = filename.split('_')[-1]
                unique = os.path.split(root)[-1].split('_')[0]
                file_path = os.path.join(root, file)
            
                file_dict[unique][num].append(file_path)
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

def extract_filename(path):
    return os.path.splitext(os.path.split(path)[-1])[0]

def save_file(json_data, path):
    output_json_path = makeOutputPath(path, json_dir, output_dir, 'json')
    output_jpg_path = makeOutputPath(path, json_dir, output_dir, 'jpg')

    path = os.path.splitext(path)[0] + '.jpg'

    saveJson(json_data, output_json_path)
    shutil.copy2(path, output_jpg_path)
    

if __name__ == "__main__":
    _, json_dir, img_dir, output_dir = sys.argv
    
    img_dict = readfiles(img_dir, '.jpg')
    json_dict = readfiles(json_dir, '.json')

    error_list = []
    for uni, num_dict in tqdm(img_dict.items()):
        for n, img_path in num_dict.items():
            if len(img_path) == 1:
                
                filename = extract_filename(img_path[0])
                json_path_list = json_dict[uni][n]

                copy_json_path = []

                for json_path in json_path_list:
                    if extract_filename(json_path) == filename:
                        std_json_path = json_path
                    else:
                        copy_json_path.append(json_path) 

                data = readJson(std_json_path)
                save_file(data, std_json_path)
                
                obj_list = []
                for obj in data['objects']:
                    name = obj['name']
                    if 'Object' in name or 'contact' in name or 'Void' in name:

                        obj_list.append(obj)
                
                for json_path in copy_json_path:
                    data = readJson(json_path)
                    
                    for idx, obj in reversed(list(enumerate(data['objects']))):
                        
                        name = obj['name']
                        
                        if 'Object' in name or 'contact' in name or 'Void' in name:

                            del data['objects'][idx]

                    [data['objects'].append(obj) for obj in obj_list]
                    
                    save_file(data, json_path)
                                                    
            else:
                error_list.append(img_path)
            