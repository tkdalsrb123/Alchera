import sys, os
import xmltodict
import random
from collections import defaultdict
import pandas as pd
from datetime import datetime
from tqdm import tqdm

def read_files(path, Ext):
    if Ext == 'img':
        file_dict = defaultdict(lambda: defaultdict(list))
        for root, dirs, files in os.walk(path):
            for file in files:
                filename, ext = os.path.splitext(file)
                if root.split('\\')[-2] == '2_Topview':
                    if ext == '.png' or ext == '.jpg':
                        filename = '-'.join(filename.split('-')[:-3])
                        k = root.split('\\')[-3]
                        file_dict[filename][k].append(file)

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

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data
            
def saveXml(pathXml, objXml):
    with open(pathXml, 'w') as f:
        f.write(xmltodict.unparse(objXml, pretty=True))
        
_, xml_dir, full_frame_dir, csv_dir, output_dir = sys.argv

label_path = './labels.xml'
label_dict = readxml(label_path)

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
        image_name = image['@name'].split('/')[-1]
        new_name = oldnew_dict[image_name]  # after 파일명으로 변경
        before_file_dict[new_name] = image

# xml 파일 만들기
df['unique'] = df['after'].str.split('-').str[:-1].str.join('-')
uni_list = df['unique'].unique()
uni_list = ['-'.join(i.split('-')[:-2]) for i in uni_list]

for uni in tqdm(uni_list):
    num_k = frame_dict[uni]
    sequence = uni.split('-')[3]
    if bool(num_k) == True:
        for k, full_frame in num_k.items():
            id = 0
            xml_img_dict = defaultdict(lambda: defaultdict(list))
            id_num = random.randint(1000,9999)
            xml_img_dict['annotations']['version'] = '1.1'
            meta = {'id':id_num, 'name':None, 'size':None, 'mode':'annotation', 'created':None, 'updated':None, 'owner':None, 'labels':label_dict['labels']}
            xml_img_dict['annotations']['meta'] = meta

            folder = os.path.join(output_dir, sequence, k)
            os.makedirs(folder, exist_ok=True)
            for frame in full_frame:
                frame_key = before_file_dict.get(frame)
                direction = frame.split('-')[6][:2]
                if direction == 'FR':
                    width = '1024'
                    height = '672'
                    if frame_key == None:
                        frame_name = f'1_Front/{frame}'
                        xml_img_dict['annotations']['image'].append({'@id':id, '@name':frame_name, '@width':width, '@height':height})
                    elif frame_key != None:
                        before_file_dict[frame]['@id'] = id
                        xml_img_dict['annotations']['image'].append(before_file_dict[frame])

                    
                elif direction == 'SD':
                    width = '624'
                    height = '1024'
                    if frame_key == None:
                        frame_name = f'2_Side/{frame}'
                        xml_img_dict['annotations']['image'].append({'@id':id, '@name':frame_name, '@width':width, '@height':height})
                    elif frame_key != None:
                        before_file_dict[frame]['@id'] = id
                        xml_img_dict['annotations']['image'].append(before_file_dict[frame])

                id += 1
            
            output_xml_path = os.path.join(folder, 'annotations.xml')
            saveXml(output_xml_path, xml_img_dict)
            print(output_xml_path, '저장!!')