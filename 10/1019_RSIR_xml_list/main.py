import os, sys, xmltodict, logging
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
                file_path = os.path.join(root, file)
                relpath = os.path.relpath(file_path, dir)
                name = relpath.split('\\')[0]
                
                file_dict[name].append(file_path) 
    return file_dict

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data

if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    xml_dict = readfiles(input_dir, '.xml')
    
    listup = []
    for filename, xml_path_list in tqdm(xml_dict.items(), 'all xml', position=0):
        stop = 'continue'
        for idx, xml_path in tqdm(enumerate(xml_path_list), desc=f"{filename}", position=1):
            logger.info(xml_path)
            data = readxml(xml_path)
            
            obj = data['annotation'].get('object')
            if obj:
                if type(obj) == dict:
                    obj = [obj]
                    
                for o in obj:
                    truncation = o['truncation']
                    occlusion = o['occlusion']

                    if truncation != '0' and occlusion != '0':
                        stop = "break"
                        
            if stop == 'break':
                break
                
        if idx+1 == len(xml_path_list):
            listup.append(filename)
    
    df = pd.DataFrame(listup, columns=['sequence'])
    df.to_excel(f'{output_dir}/xml_list.xlsx', index=False)
