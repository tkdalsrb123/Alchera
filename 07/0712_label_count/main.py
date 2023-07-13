import json, os, sys
import pandas as pd

_, input_dir, output_dir = sys.argv

count_list = []
for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.json':
            json_path = os.path.join(root, file)
            
            with open(json_path, encoding='UTF-8') as f:
                json_file = json.load(f)
            
            sur_count = 0
            el_count = 0
            for ann in json_file['annotations']:
                if ann['name'] != 'surface':
                    el_count += 1
                elif ann['name'] == 'surface':
                    sur_count += 1
            
            count_list.append([file, sur_count, el_count])

df = pd.DataFrame(count_list, columns = ['파일명', 'surface', 'else'])

df.to_excel(f'{output_dir}/count.xlsx', index=False)