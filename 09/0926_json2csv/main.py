import os, sys, json
import pandas as pd
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
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename ,ext = os.path.splitext(file)
            if ext == '.json':
                file_path = os.path.join(root, file)

                file_list.append(file_path)
    return file_list

if __name__ == '__main__':
    
    _, input_dir, output_dir = sys.argv

    logger = make_logger('log.log')

    json_list = readfiles(input_dir)

    df2list = []
    for json_path in tqdm(json_list):
        root, file = os.path.split(json_path)
        logger.info(json_path)
        with open(json_path, encoding='utf-8-sig') as f:
            json_file = json.load(f)
        obj_points = None
        sha_points = None
        con_2_points = None
        con_points = None
        nail_points = None
        hangnail_points = None
        if type(json_file) == list:
            for json_info in json_file:
                json_obj = json_info.get('objects')
                if json_obj:
                    for obj in json_obj:
                        name = obj['name']
                        if  name == "Object_segmentation":
                            obj_points = obj['points']
                            
                        elif name == "Shadow_segmentation":
                            sha_points = obj['points']
                        
                        elif name == "contact_line_2":
                            con_2_points = obj['points']
                        
                        elif name == "contact_line":
                            con_points = obj['points']
                else:
                    name = json_info['name']

                    if name == "nail":
                        nail_points = json_info['points']
                    
                    elif name == 'hangnail':
                        hangnail_points = json_info['points']
        elif type(json_file) == dict:
                json_obj = json_file.get('objects')
                if json_obj:
                    for obj in json_obj:
                        name = obj['name']
                        if  name == "Object_segmentation":
                            obj_points = obj['points']
                            
                        elif name == "Shadow_segmentation":
                            sha_points = obj['points']
                        
                        elif name == "contact_line_2":
                            con_2_points = obj['points']
                        
                        elif name == "contact_line":
                            con_points = obj['points']
                else:
                    name = json_info['name']

                    if name == "nail":
                        nail_points = json_info['points']
                    
                    elif name == 'hangnail':
                        hangnail_points = json_info['points']
            

            
        df2list.append([file, obj_points, sha_points, con_points, con_2_points, nail_points, hangnail_points])

    df = pd.DataFrame(df2list, columns=['filename', 'Object_segmentation', 'Shadow_segmentation', 'contact_lin', 'contact_line_2', 'nail', 'hangnail'])
    df.to_csv(f"{output_dir}/seg_points.csv", encoding='utf-8', index=False)
