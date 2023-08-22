import os, sys, json
import pandas as pd
from collections import defaultdict, Counter
import time
from tqdm import tqdm


def read_files(path, Ext):
    if Ext == 'json':
        file_dict = defaultdict(str)
        for root, dirs, files in os.walk(path):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.json':
                    file_path = os.path.join(root, file)

                    file_dict[filename] = file_path   
    return file_dict                 
                    
_, input_dir, output_dir = sys.argv

# class dict 만들기
class_dict = defaultdict(str)
excel_path = './신규DB_xml_class.xlsx'
excel = pd.read_excel(excel_path)
for i in range(excel.shape[0]):
    class_dict[excel.loc[i, 'NO']] = eval(excel.loc[i, 'class'])
class_list = [eval(i) for i in list(excel['class'].values)]

json_dict = read_files(input_dir, 'json')

# class counting
output_df = pd.DataFrame(class_list, columns=['class'])
for json_filename, json_filepath in tqdm(json_dict.items()):
    counter = Counter()
    print(json_filepath)
    with open(json_filepath, encoding='utf-8') as f:
        json_file = json.load(f)
    
    for ann in json_file['annotations']:
        counter[class_dict[ann['category_id']]] += 1

    df = pd.DataFrame([[k, v] for k ,v in counter.items()], columns=['class', json_filename])
    output_df = output_df.merge(df, how='outer', on='class')

output_df = output_df.fillna(0)

timestamp = time.time()
now = time.localtime(timestamp)
now_formated = time.strftime("%d일%H시%M분", now)
output_df.to_excel(f'{output_dir}/class_count_{now_formated}.xlsx', index=False)