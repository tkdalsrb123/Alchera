import os, sys, logging, xmltodict
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
    file_list = []

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext == Ext:
                file_path = os.path.join(root, file)
            
                file_list.append(file_path)
    return file_list

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data


if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    xml_list = readfiles(input_dir, '.xml')

    class_dict = defaultdict(lambda : defaultdict(int))
    for xml_path in tqdm(xml_list):
        logger.info(xml_path)
        filename = os.path.split(xml_path)[-1]
        data = readxml(xml_path)

        images = data['annotations']['image']

        for image in images:
            polygon = image['polygon']
            if type(polygon) == dict:
                polygon = [polygon]

            count_dict = defaultdict(set)
            for poly in polygon:
                if poly['@label'] == 'Road':
                    road_text = poly['attribute']['#text']
                    count_dict[road_text].add(road_text)
                
                else:
                    
                    attribute = poly['attribute']

                    if type(poly['attribute']) == dict:
                        attribute = [poly['attribute']]
                        
                    for att in attribute:
                        if att['@name'] == 'ID':
                            id_text = att['#text']
                            count_dict[poly['@label']].add(id_text)
                            
            for key, val in count_dict.items():
                class_dict[filename][key] += len(val)
    

    dict2list = []
    for key, val in class_dict.items():
        dict2df = {}
        dict2df['filename'] = key
        val_sum = sum(val.values())
        for k, v in val.items():
            dict2df[k] = v
            
        dict2df['Total'] = val_sum
        dict2list.append(dict2df)
    
    
    df = pd.DataFrame(dict2list)
    df.to_excel(f"{output_dir}/output.xlsx", index=False)
            
            