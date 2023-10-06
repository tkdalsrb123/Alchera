import json, os, sys, re
import logging
import pandas as pd
from tqdm import tqdm
from collections import defaultdict

def extract_patterns(text):
    byte = 0
    for t in text:
        if type(t) == str:
            # 1. 공백 (Whitespace)
            whitespace_matches = re.findall(r'\s+', t)
            
            # 2. 한글 (Korean)
            korean_matches = re.findall(r'[가-힣]+', t)
            
            # 3. 영어 (English)
            english_matches = re.findall(r'[a-zA-Z]+', t)
            
            # 4. 숫자 (Numbers)
            number_matches = re.findall(r'\d+', t)
            
            # 5. 특수 문자 (Special Characters)
            special_characters_matches = re.findall(r'[^a-zA-Z0-9가-힣\s]+', t)
        elif type(t) == list:
            for i in t:
                # 1. 공백 (Whitespace)
                whitespace_matches = re.findall(r'\s+', i)
                
                # 2. 한글 (Korean)
                korean_matches = re.findall(r'[가-힣]+', i)
                
                # 3. 영어 (English)
                english_matches = re.findall(r'[a-zA-Z]+', i)
                
                # 4. 숫자 (Numbers)
                number_matches = re.findall(r'\d+', i)
                
                # 5. 특수 문자 (Special Characters)
                special_characters_matches = re.findall(r'[^a-zA-Z0-9가-힣\s]+', i)

        byte += sum([len(j) for j in whitespace_matches])
        byte += sum([len(j)*2 for j in korean_matches])
        byte += sum([len(j) for j in english_matches])
        byte += sum([len(j) for j in number_matches])
        byte += sum([len(j) for j in special_characters_matches])

    return byte
        
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

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    key_list = ['title', 'source', 'additional', 'writer']
    sub_key_list = ['legend', 'x', 'y', 'unit', 'x-unit', 'y-unit', 'unit-range']
    json_dict = readfiles(input_dir, '.json')

    df_list = []
    for filename, json_path in tqdm(json_dict.items()):
        json_file = readJson(json_path)

        info_dict = {'filename':filename}
        for key in key_list:
            score = extract_patterns(json_file[key])
            info_dict.update({key:score})
    
        for sub_key in sub_key_list:
            value = json_file['contents'][0][sub_key]
            score = extract_patterns(value)
            info_dict.update({sub_key:score})

        df_list.append(info_dict)
    
    df = pd.DataFrame.from_dict(df_list)
    df.to_excel(f"{output_dir}/report_byte.xlsx", index=False)