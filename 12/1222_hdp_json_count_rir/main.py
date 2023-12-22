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
        info_dict = {"normal_sedan":0,"normal_etc":0,"normal_emergency":0,"midsize_normal":0,"midsize_emergency":0,"large_normal":0,"large_emergency":0,"motorcycle_normal":0,"motorcycle_emergency":0}
        data = readxml(xml_path)

        for image in data['annotations']['image']:
            
            points = image.get('points')
            if points:
                if type(points) == dict:
                    points = [points]
                for point in points:
                    info_dict[point['@label']] += 1
            

        list2df.append([filename, info_dict["normal_sedan"],info_dict["normal_etc"],info_dict["normal_emergency"],info_dict["midsize_normal"],info_dict["midsize_emergency"],info_dict["large_normal"],info_dict["large_emergency"],info_dict["motorcycle_normal"],info_dict["motorcycle_emergency"]])
        
    make_csv(list2df, ['sequence', "normal_sedan","normal_etc","normal_emergency","midsize_normal","midsize_emergency","large_normal","large_emergency","motorcycle_normal","motorcycle_emergency"],  f'./{os.path.split(input_dir)[-1]}.csv')

    
        
                    
        
        