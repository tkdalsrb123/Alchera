import os, sys, xmltodict, logging
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

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data

def make_csv(_list, col, output_path):
    df = pd.DataFrame(_list, columns=col)
    df.to_csv(output_path, index=False)
    
if __name__ == "__main__":
    _, input_dir = sys.argv
    
    xml_dict = readfiles(input_dir, '.xml')
    
    list2df = []
    for filename, xml_path in tqdm(xml_dict.items()):
        data = readxml(xml_path)
        count = 0
        for image in data['annotations']['image']:
            polygon = image.get("polygon")
            if polygon:
                if type(polygon) == dict:
                    polygon = [polygon]
                
                for poly in polygon:
                    if poly['@label'] in ["Vehicl_Body", "Vehicle_Tire"]:
                        count += 1
                        break
                    
        list2df.append([filename, count])
    make_csv(list2df, ['sequence', 'frame'], f'./{os.path.split(input_dir)[-1]}.csv')