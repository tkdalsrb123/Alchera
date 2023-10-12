import json, os, sys
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
import logging

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
    with open(path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    return data

_, input_dir, output_dir = sys.argv

category ={ 
"ch01":	"메인 분전반",
"ch02":	"TV",
"ch03":	"선풍기",
"ch04":	"전기포트",
"ch05":	"전기밥솥",
"ch06":	"세탁기",
"ch07":	"헤어드라이기",
"ch08":	"진공 청소기(유선)",
"ch09":	"전자레인지",
"ch10":	"에어프라이어",
"ch11":	"의류건조기",
"ch12":	"식기세척기",
"ch13":	"에어컨",
"ch14":	"전기장판, 담요",
"ch15":	"온수매트",
"ch16":	"인덕션(전기레인지)",
"ch17":	"컴퓨터",
"ch18":	"전기다리미",
"ch19":	"공기청정기",
"ch20":	"제습기",
"ch21":	"일반 냉장고",
"ch22":	"김치냉장고",
"ch23":	"무선공유기/셋톱박스"}

json_dict = readfiles(input_dir, '.json')
df_list = []
for filename, json_path in tqdm(json_dict.items()):
    json_file = readJson(json_path)

    data_dict = {}
    class_id = category[json_file['label']['id']]
    data_dict.update({'파일명':filename})
    data_dict.update({'class_id':class_id})

    if len(json_file['label']['active_inactive']) > 0:
        label = eval(json_file['label']['active_inactive'])
        i = 1
        for l in label:
            label_data = ', '.join(l)
            key_name = f'label_{i}'
            data_dict.update({key_name:label_data})
            i+=1

    df_list.append(data_dict)

df = pd.DataFrame.from_dict(df_list)
df.to_excel(f'{output_dir}/105-129_class.xlsx', index=False)