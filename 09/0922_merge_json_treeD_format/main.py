import json, os, sys
import logging
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

def readfiles(dir):
    file_dict = defaultdict(lambda : defaultdict(str))
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.json':
                file_path = os.path.join(root, file)
                relpath = os.path.relpath(root, dir)
                cat = relpath.split('\\')[0]
                
                file_dict[filename][cat] = file_path

    return file_dict

def openJson(path):
    with open(path, encoding='utf-8') as f:
        json_file = json.load(f)
    
    return json_file

def saveJson(path, new_json):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(new_json, f, indent=2, ensure_ascii=False)

def JsonTree(o_obj, s_obj, c_obj, p_obj, s_info, output_path):
    tree_dict = {}
    if p_obj:
        if c_obj:
            tree_dict['objects'] = [o_obj, s_obj, c_obj, p_obj]
        else:
            tree_dict['objects'] = [o_obj, s_obj]
    else:
        if c_obj:
            tree_dict['objects'] = [o_obj, s_obj, c_obj]
        else:
            tree_dict['objects'] = [o_obj, s_obj]
            
    tree_dict['info'] = s_info
    logger.info(output_path)
    saveJson(output_path, tree_dict)
    
_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

json_dict = readfiles(input_dir)

for filename, cat in tqdm(json_dict.items()):
    output_folder = os.path.join(output_dir, f"{filename.split('_')[1]}_furniture")
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, f"{filename}.json")
    obj_json = cat.get('object_seg')
    shadow_json = cat.get('shadow_seg')
    contact_json = cat.get('contact_line')
    poly_json = cat.get('c_poly')

    if obj_json:
        obj_json_file = openJson(obj_json)
        obj_obj = obj_json_file['objects'][0]
        obj_obj['classId'] = ""     # Object_segmentation classId 변경

    if shadow_json:
        shadow_json_file = openJson(shadow_json)
        shadow_obj = shadow_json_file['objects'][0]
        shadow_info = shadow_json_file['info']
        shadow_obj['classId'] = ""      # shadow_segmentation classId 변경
        shadow_info['dirPath'] = ""     # info dirPath 변경
        shadow_info['projectName'] = ""     # info projectName 변경
        shadow_info['taskName'] = ""        # info taskName 변경
        
    if contact_json:
        contact_json_file = openJson(contact_json)
        contact_obj = contact_json_file['objects'][0]
        contact_obj['classId'] = ""     # contact_line classId 변경
    else:
        contact_obj = None
    
    if poly_json:
        poly_json_file = openJson(poly_json)
        poly_obj = poly_json_file['objects'][0]
        poly_obj['classId'] = ""         # contact_line_2 classId 변경
    else:
        poly_obj = None
        
    
    JsonTree(obj_obj, shadow_obj, contact_obj, poly_obj, shadow_info, output_path)
        
