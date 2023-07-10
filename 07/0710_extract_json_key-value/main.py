import json, os, sys
import pandas as pd

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
                cat_list.append([cat['id'], cat['name'], cat['level2'], cat['level1']])

df = pd.DataFrame(cat_list, columns=['id', 'name', 'level2', 'level1'])
df.to_excel(f'{output_dir}/category.xlsx', index=False)