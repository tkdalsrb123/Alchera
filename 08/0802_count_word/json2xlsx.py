import os, sys, json
from collections import Counter, defaultdict
import pandas as pd

_, input_dir, output_dir, excel_dir = sys.argv
# 특수기호 종류 불러오기
df = pd.read_excel(excel_dir)
special =  list(df['특수기호'])

for root, dirs, files in os.walk(input_dir):
    list2df = []
    for file in files:
        word_count = 0
        special_count = 0
        filename, ext = os.path.splitext(file)
        if ext == '.json':
            file_path = os.path.join(root, file)
            print(file_path)
            mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
            folder = os.path.join(output_dir, mid)
            os.makedirs(folder, exist_ok=True)
            
            count_dict = defaultdict(int)
            count_dict['filename'] = file
            with open(file_path, 'r', encoding='utf-8') as f:
                json_file = json.load(f)
            # 글자수 카운팅
            for obj in json_file['objects']:
                lang = obj['name']
                for att in obj['attributes']:
                    for value in att['values']:
                        if value['selected'] == True:
                            text = value['value']
                            count = Counter(text)

                            for key, value in count.items():
                                if key in special:  # 특수기호인 글자는 따로 추출
                                    count_dict['special'] += value
                                else:
                                    count_dict[lang] += value
            list2df.append(count_dict)
            
    if len(list2df)>0:
        dict2df = pd.DataFrame.from_dict(list2df, orient='columns').fillna(0)
        output_path = os.path.join(folder, f'{filename}.xlsx')
        dict2df.to_excel(output_path, index=False)
