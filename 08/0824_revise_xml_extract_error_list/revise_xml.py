import os, sys
import xmltodict
import pandas as pd
import time
from tqdm import tqdm
import logging
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

def readfiles(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.xml':
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data
            
def saveXml(pathXml, objXml):
    with open(pathXml, 'w') as f:
        f.write(xmltodict.unparse(objXml, pretty=True))
        
_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

xml_list = readfiles(input_dir)
error_dict = defaultdict(list)
for xml_path in tqdm(xml_list):

    root, file = os.path.split(xml_path)
    mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
    folder = os.path.join(output_dir, mid)
    os.makedirs(folder,  exist_ok=True)    

    logger.info(xml_path)
    xml_file = readxml(xml_path)

    for image in xml_file['annotations']['image']:
        have_box = image.get('box')
        if have_box != None:
            for box in image['box']:
                if type(box) == list:
                    for att in box['attribute']:
                        text = att.get('#text')
                        if text == None:
                            att['#text'] = att['@name'].split(' ')[1]
                            error_dict['no_value_file'].append(image['@name'])
                elif type(box) == dict:
                    for box in image['box']:
                        for att in box['attribute']:
                            text = att.get('#text')
                            if text == None:
                                att['#text'] = att['@name'].split(' ')[1]
                                error_dict['no_value_file'].append(image['@name'])   
        elif have_box == None:
            error_dict['no_box_file'].append(image['@name'])
    output_xml_path = os.path.join(folder, file)
    saveXml(output_xml_path, xml_file)

# timestamp = time.time()
# now = time.localtime(timestamp)
# now_formated = time.strftime("%d일%H시%M분", now)

df = pd.DataFrame.from_dict(error_dict, orient='columns')
df.to_excel(f'{output_dir}/error_list.xlsx', index=False)