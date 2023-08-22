import sys, os
import xmltodict
import random
from collections import defaultdict
import pandas as pd
from datetime import datetime
from tqdm import tqdm

def read_files(path, Ext):
    if Ext == 'img':
        file_dict = defaultdict(list)
        for root, dirs, files in os.walk(path):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.png' or ext == '.jpg':
                    filename = '-'.join(filename.split('-')[:-1])
                    file_dict[filename].append(file)
                    
        return file_dict

    elif Ext == 'xml':
        file_list = []
        for root, dirs, files in os.walk(xml_dir):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.xml':
                    xml_path = os.path.join(root, file)
                    file_list.append(xml_path)
                    
        return file_list

def xml_image_info(dir, key, frame):
    if dir == 'FR':
        width = '1024'
        height = '672'
        if key == False:
            frame_name = f'1_Front/{frame}'
            xml_img_dict['annotations']['image'].append({'@id':id, '@name':frame_name, '@width':width, '@height':height})
        elif key == True:
            xml_img_dict['annotations']['image'].append(before_file_dict[uni])
            
    elif dir == 'SD':
        width = '624'
        height = '1024'
        if key == False:
            frame_name = f'1_Front/{frame}'
            xml_img_dict['annotations']['image'].append({'@id':id, '@name':frame_name, '@width':width, '@height':height})
        elif key == True:
            xml_img_dict['annotations']['image'].append(before_file_dict[uni])

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data
            
def saveXml(pathXml, objXml):
    with open(pathXml, 'w') as f:
        f.write(xmltodict.unparse(objXml, pretty=True))
        
_, xml_dir, full_frame_dir, csv_dir, output_dir = sys.argv

# csv 파일
df = pd.read_csv(csv_dir, encoding='utf-8')
df = df.dropna()
oldnew_dict = defaultdict(str)
for i in range(df.shape[0]):
    oldnew_dict[df.loc[i, 'before']] = df.loc[i, 'after']


xml_list = read_files(xml_dir, 'xml')
frame_dict = read_files(full_frame_dir, 'img')

# xml에서 프레임 정보들 가져오기
before_file_dict = defaultdict(str)
for xml_path in xml_list:
    xml_file = readxml(xml_path)
    
    for image in xml_file['annotations']['image']:
        new_name = oldnew_dict[image['@name']]  # after 파일명으로 변경
        before_file_dict[new_name] = image

# xml 파일 만들기
df['unique'] = df['after'].str.split('-').str[:-1].str.join('-')
uni_list = df['unique'].unique()

xml_img_dict = defaultdict(lambda: defaultdict(list))
for uni in uni_list:
    full_frame = frame_dict[uni]
    id = 0
    for frame in full_frame:
        print(frame)
        frame_key = before_file_dict.get(frame)
        direction = frame_key.split('-')[6]
        xml_image_info(direction, frame_key, frame)

print(xml_img_dict)
