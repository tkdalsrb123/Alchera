import os, sys, xmltodict
import pandas as pd
from tqdm import tqdm
from collections import defaultdict

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

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data

if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    xml_dict = readfiles(input_dir, '.xml')

    file_list = []
    for filename, xml_path in tqdm(xml_dict.items()):
        path_split = xml_path.split('\\')

        lhrh = path_split[-4]
        seq = path_split[-5]
        data = readxml(xml_path)
        objects = data['annotation']['object']

        if type(objects) == dict:
            objects = [objects]
        
        for obj in objects:
            ID = obj['cuboid_id']
  
            if ID == 0:
                file_list.append([seq, lhrh, filename])
                break
        
    
    df = pd.DataFrame(file_list, columns=['sequence', 'lhrh', 'filename'])
    df.to_csv(f"{output_dir}/file_list.csv", index=False, encoding='utf-8')