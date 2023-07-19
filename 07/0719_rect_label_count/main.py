import json, os, sys
import pandas as pd

_, input_dir = sys.argv

count_list = []
for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.json':
            json_path = os.path.join(root, file)
            
            with open(json_path, encoding='UTF-8') as f:
                json_file = json.load(f)
            
            rect_count = 0
            for ann in json_file['annotations']:
                if ann['labeling']['type'] == 'rect':
                    rect_count += 1

            
            count_list.append([file, rect_count])

df = pd.DataFrame(count_list, columns = ['Filname', 'bbox개수'])

df.to_excel('./2-128-269_label_count.xlsx', index=False)
