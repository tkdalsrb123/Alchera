import os, sys, zipfile
import xmltodict
from collections import defaultdict
import logging
from tqdm import tqdm

def readfiles(dir, Ext):
    if Ext == 'zip':
        file_dict = defaultdict(str)
        for root, dirs, files in os.walk(dir):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.zip':
                    file_path = os.path.join(root, file)
                    file_dict[filename] = file_path
        return file_dict
    
def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data

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

_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

zip_dict = readfiles(input_dir, 'zip')

for filename, zip_path in tqdm(zip_dict.items()):
    root , file = os.path.split(zip_path)
    xml_filename = '_'.join(filename.split('-')[0].split('_')[3:])
    
    logger.info(zip_path)
    # zip 파일 해제 후 저장
    zipfile.ZipFile(zip_path).extract('annotations.xml', output_dir)
    old_name = os.path.join(output_dir, 'annotations.xml')
    
    xml_file = readxml(old_name) # xml에서 이미지 개수 가져오기

    size = xml_file['annotations']['meta']['task']['size']
    
    new_name = os.path.join(output_dir, f"{xml_filename}_{size}.xml")
    # 파일명 변경 후 저장
    os.rename(old_name, new_name)
    logger.info(new_name)