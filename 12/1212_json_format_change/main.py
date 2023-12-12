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

def shape_format(shapes_type, label, points):
    tree = {
      "shapes_type": shapes_type,
      "label": label,
      "points": points
        }
    
    return tree

def json_format(imageWidth, imageHeight, imagePath, shapes, output_path):
    tree = {
    "imageWidth": imageWidth,
    "imageHeight": imageHeight,
    "imageData": "",
    "imagePath": imagePath,
    "shapes": shapes
    }
    
    saveJson(tree, output_path)
    
if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv

    logger = make_logger('log.log')
    json_dict = readfiles(input_dir, '.json')

    for filename, json_path in tqdm(json_dict.items()):
        logger.info(json_path)
        output_json_path = makeOutputPath(json_path, input_dir, output_dir, 'json')
        data = readJson(json_path)

        imagePath = data['info']['imageName']
        imageWidth = str(data['info']['width'])
        imageHeight = str(data['info']['height'])
        
        shape_list = []
        for obj in data['objects']:
            shapes_type = obj['type']
            label = obj['name']
            points = [[round(p[0], 1), round(p[1], 1)]for p in obj['points']]
            shape_list.append(shape_format(shapes_type, label, points))
        
        json_format(imageWidth, imageHeight, imagePath, shape_list, output_json_path)

