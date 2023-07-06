import os, sys
import xmltodict
import pandas as pd
from collections import defaultdict

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data

_, xml_dir, excel_path, output_dir = sys.argv

all_list = []   # 최종 엑셀파일로 바꿔 줄 리스트
class_list = []     # class 명이 들어갈 리스트
excel = pd.read_excel(excel_path)
# class excel파일에서 class 가져오기
for label in excel['class']:
    label = label.replace('"', '')
    class_list.append(label)
all_list.append(class_list)

# column에 파일명이 들어갈 리스트
columns = ['class']
# class의 개수가 들어갈 리스트
xml_list= []
# xml 파일 읽기
for root, dirs, files in os.walk(xml_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.xml':
            columns.append(file)
            
            label_dict = defaultdict(int)
            for label in excel['class']:
                label = label.replace('"', '')
            
            xml_path = os.path.join(root, file)
            
            print(f'{xml_path} 읽는 중!!!')
            xml = readxml(xml_path)
            
            for image in xml['annotations']['image']:
                if 'polygon' in image.keys():
                    if type(image['polygon']) == list:
                        for poly in image['polygon']:
                            label_dict[poly['@label']] += 1
                    else:
                        label_dict[image['polygon']['@label']] += 1

            all_list.append([label_dict[v] for v in class_list])


count_df = pd.DataFrame(all_list).transpose()
count_df.columns = columns

count_df.to_excel(f'{output_dir}/xml_count.xlsx', index=False)
print(f'{output_dir}/xml_count.xlsx 저장!!!!') 
                    