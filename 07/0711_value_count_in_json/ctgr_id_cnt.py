import json, os, sys
from collections import Counter
import pandas as pd
from tqdm import tqdm

_, input_dir, output_dir = sys.argv

count_list = []
for root, dirs, files in tqdm(os.walk(input_dir)):
    for file in files:
        ext = os.path.splitext(file)[-1]
        if ext == '.json':
            json_path = os.path.join(root, file)
            print(json_path, '읽는중!!')
            
            with open(json_path, encoding='utf-8') as f:
                data = json.load(f)
                
            for ann in data['annotations']:
                count_list.append(ann['category_id'])

cnt = Counter(count_list)

df = pd.DataFrame([[k,v] for k, v in cnt.items()], columns=['id', 'count'])
df.to_excel(f'{output_dir}/ctgr_id_cnt.xlsx', index=False)
print(f'{output_dir}/ctgr_id_cnt.xlsx', '저장!!!')

                