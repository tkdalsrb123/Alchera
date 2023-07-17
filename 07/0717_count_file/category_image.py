import json, os, sys
import pandas as pd
from collections import Counter

_, json_dir, output_dir = sys.argv

cat_list = []
for root, dirs, files in os.walk(json_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.json':
            json_path = os.path.join(root, file)
            
            with open(json_path, encoding='utf-8') as f:
                json_file = json.load(f)
                
            for cat in json_file['categories']:
                cat_list.append(cat['id'])

cnt = Counter(cat_list)

df = pd.DataFrame([[key, val] for key, val in cnt.items()], columns=['id', 'count'])
df.to_excel(f'{output_dir}/count.xlsx', index=False)