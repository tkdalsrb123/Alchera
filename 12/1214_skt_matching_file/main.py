import os, sys, json, logging
import pandas as pd
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from PIL import Image
from collections import defaultdict
from tqdm import tqdm
from openpyxl.drawing.image import Image as XLImage

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

def readfiles2(dir, Ext):
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext == Ext:
                folder = os.path.split(root)[-1]
                file_path = os.path.join(root, file)
            
                file_dict[folder].append(file_path)
        
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

def extract_filename(path):
    filename = os.path.splitext(os.path.basename(path))[0]
    return filename

def make_xlsx(_list, col, output_path):
    df = pd.DataFrame(_list, columns=col)
    df.to_excel(output_path, index=False)
    
def insert_image(cell, img_path, width=None, height=None):
    img = XLImage(img_path)
    img.anchor = cell

    if width and height:
        img.width = width  # 이미지 너비 설정
        img.height = height  # 이미지 높이 설정
        
    sheet.add_image(img)
    
if __name__ == "__main__":
    _, img_dir, json_dir, treed_dir, output_dir = sys.argv
    
    img_dict = readfiles(img_dir, '.jpg')
    json_dict = readfiles(json_dir, '.json')
    treed_dict = readfiles2(treed_dir, '.json')

    print('---------------json 정보 수집-----------------')
    json_info_dict = {}
    for filename, json_path in json_dict.items():
        data = readJson(json_path)
        
        json_info_dict[filename] = data
        
    treed_info_dict = defaultdict(lambda: defaultdict(dict))
    for folder, treed_path_list in treed_dict.items():
        for treed_path in treed_path_list:
            filename = extract_filename(treed_path)
            data = readJson(treed_path)

            value = ''
            for obj in data['objects']:
                if '필요' in obj['name']:
                    value = obj['attributes'][0]['values'][0]['value']

            treed_info_dict[folder][filename] = value
    
    list2df = []
    for folder, filename_list in treed_info_dict.items():
        before_info = json_info_dict[folder]
        for filename, value in filename_list.items():
            key = filename.split('_')[-1]
            before_text = before_info[key]
            after_text = value
            
            img_path = img_dict[filename]

            list2df.append([folder, filename, img_path, before_text, after_text])
    
    make_xlsx(list2df, ['폴더', '이미지 파일명', '이미지', '원본', '수정'], f'{output_dir}/main.xlsx')
    
    print('---------------이미지 삽입-----------------')
    
    # 엑셀 파일 로드
    workbook = load_workbook(f'{output_dir}/main.xlsx')  # 엑셀 파일 경로를 지정합니다.
    sheet = workbook.active

    # 이미지 파일 경로가 저장된 열 선택 (예: A열)
    image_paths = [cell.value for cell in sheet['C'][1:] if cell.value]  # 이미지 경로가 있는 열을 읽습니다.

    # 이미지 파일 경로를 엑셀의 이미지로 변환하여 삽입
    for index, img_path in enumerate(image_paths, start=2):
        cell_to_insert = f'C{index}'  # 이미지를 삽입할 셀 지정

        insert_image(cell_to_insert, img_path, 100, 100)

    # 변환된 이미지를 포함한 엑셀 파일 저장
    workbook.save(f'{output_dir}/main.xlsx')