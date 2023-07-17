import json, os, sys
import pandas as pd
from collections import Counter

_, json_dir, output_dir = sys.argv

df_list = []
for root, dirs, files in os.walk(json_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.json':
            json_path = os.path.join(root, file)
            
            with open(json_path, encoding='utf-8') as f:
                json_file = json.load(f)
            
            filename = file
            for ann in json_file['annotations']:
                ann_id = ann['id']
                img_id = ann['image_id']
                cat_id = ann['category_id']
                
                for cat in json_file['categories']:
                    if cat['id'] == cat_id:
                        level1 = cat['level1']
                        level2 = cat['level2']
                        name = cat['name']
                        
                        df_list.append([filename, ann_id, img_id, cat_id, level1, level2, name])

df = pd.DataFrame(df_list, columns=['filename', 'ann_id', 'image_id', 'category_id', 'level1', 'level2', 'name'])
df.to_excel(f'{output_dir}/final.xlsx', index=False)