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

def readfiles(dir, Ext, direction):
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            all_sd = filename.split('-')[0]
            unique = '-'.join(filename.split('-')[1:])
            if ext == Ext and all_sd == direction:
                file_path = os.path.join(root, file)
            
                file_dict[unique] = file_path
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

def shape_format(_class, sub_class, _id, segmentation):
    format = {
        "class": _class,
        "sub_class": sub_class,
        "id": _id,
        "segmentation": segmentation,
        "shape_type": "Polygon"
    }
    
    return format

def sd_json_format(image_name, lidar_name, segment_name, shapes, output_path):
    format = {
        "image_name": image_name,
        "lidar_name": lidar_name,
        "segment_name": segment_name,
        
        "image_size":{
            "imgWidth":1792,
            "imgHeight":1024,
            "imgDepth":3
        },
        
        "shapes": shapes
    }
    
    saveJson(format, output_path)
if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    all_json_dict = readfiles(input_dir, '.json', 'CMR_GT_ALL')
    sd_json_dict = readfiles(input_dir, '.json', 'CMR_GT_SD')

    for unique, all_json_path in tqdm(all_json_dict.items()):
        sd_json_path = sd_json_dict[unique]
        output_json_path = makeOutputPath(sd_json_path, input_dir, output_dir, 'json')
        all_data = readJson(all_json_path)
        # sd_data = readJson(sd_json_path)

        image_name = "CMR_GT_FRAME" + "-" + f"{unique}.png"
        lidar_name = "CMR_GT_Lidar" + "-" + f"{unique}.bin"
        segment_name = "CMR_SD_Color" + "-" + f"{unique}.png"
        
        shape_list = []
        for obj in all_data['object']:
            _id = obj['id']
            _class = obj['class']
            sub_class = obj['sub_class']
            segmentation = obj['segmentation']
            shape_list.append(shape_format(_class, sub_class, _id, segmentation))
            
        sd_json_format(image_name, lidar_name, segment_name, shape_list, output_json_path)