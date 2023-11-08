import os, shutil, sys, logging
import xmltodict
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

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data

if __name__ == '__main__':
    _, input_dir, xml_dir, output_dir = sys.argv

    logger = make_logger('log.log')
    
    img_dict = readfiles(input_dir, '.png')
    xml_dict = readfiles(xml_dir, '.xml')

    imgname_list = []
    for filename, xml_path in tqdm(xml_dict.items(), desc='extract image path'):
        logger.info(xml_path)
        data = readxml(xml_path)
        
        for img in data['annotations']['image']:
            img_path = img['@name']
            name = os.path.split(img_path)[-1][:-4]
            imgname_list.append(name)
    
    for imgname in tqdm(imgname_list, desc='copy image'):
        img_path = img_dict.get(imgname)
        logger.info(img_path)
        if img_path:
            path_split = img_path.split('\\')[-4:] 
            file = path_split[-1]
            mid = '\\'.join(path_split[:-1])

            folder = os.path.join(output_dir, mid)
            os.makedirs(folder, exist_ok=True)
            output_img_path = os.path.join(folder, file)
            
            shutil.copy2(img_path, output_img_path)
            logger.info(output_img_path)
            

            
    
    