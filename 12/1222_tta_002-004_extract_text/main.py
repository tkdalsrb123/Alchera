import os, sys, logging, json
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

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data 

def make_xlsx(_list, col, output_path):
    df = pd.DataFrame(_list, columns=col)
    df.to_excel(output_path, index=False)
    
if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    json_dict = readfiles(input_dir, '.json')

    info_dict = defaultdict(list)
    for filename, json_path in tqdm(json_dict.items(), desc='gather data'):
        data = readJson(json_path)

        # lang = data['대화정보']['대화ID'].split('-')[-1]

        for content in data['대화내용']:
            _id = content['id']
            use_lang = content['사용언어']
            filename = content['음성파일명']
            text = content['전사문']

            info_dict[use_lang].append([filename, _id, use_lang, text])
    
    
    for lang, info in tqdm(info_dict.items(), desc='create excel'):
        make_xlsx(info, ['파일명', 'id', '사용 언어', '전사문'], f"{output_dir}/{lang}.xlsx")