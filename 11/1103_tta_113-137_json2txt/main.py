import os, sys, logging, json
import textwrap
from tqdm import tqdm
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

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

def makeOutputPath(file_path, file_dir, output_dir, Ext, filename):
    root, file = os.path.split(file_path)
    # filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

    
if __name__ == '__main__':
    _, source_dir, label_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')

    source_dict = readfiles(source_dir, '.json')
    label_dict = readfiles(label_dir, '.json')
    
    for filename, source_path in tqdm(source_dict.items()):
        logger.info(source_path)
        
        label_path = label_dict[filename]
        logger.info(label_path)
        
        source_data = readJson(source_path)
        label_data = readJson(label_path)

        documentid = source_data['dataset']['documentId']
        abstract = source_data['dataset']['abstract']
        claims = source_data['dataset']['claims']
        sno = label_data['dataset']['Sno']
        stext = label_data['dataset']['Stext']
        
        output_filename = f'{sno}_{stext}_{documentid}'
        output_text_path = makeOutputPath(label_path, label_dir, output_dir, '.txt', output_filename)

        text = f'발명의 요약: {abstract}\n\n청구항: {claims}\n\n소분류 코드: {sno}\n\n소분류 설명: {stext}\n\n\n\nPass(o)/Fail(x):'
        
        with open(output_text_path, 'w', encoding='utf-8') as f:
            f.write(text)