import os, json, sys
from collections import defaultdict
import pandas as pd

_, input_dir, output_dir = sys.argv

count_file = defaultdict(list)
for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.json':
            json_path = os.path.join(root, file)
            
            with open(json_path, encoding='UTF-8') as f:
                json_file = json.load(f)
            
            for ann in json_file['annotations']:
                count_file[ann['category_id']].append(file)
            
for key, val in count_file.items():
    count_file[key] = len(set(val))


df = pd.DataFrame([ [key, val] for key, val in count_file.items()], columns=['클래스','count'])
df.to_excel(f'{output_dir}/count.xlsx', index=False)