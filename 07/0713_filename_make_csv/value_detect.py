import json, os, sys
import pandas as pd

_, input_dir, output_dir, category_id = sys.argv

id_list = []
for root, dirs, files in os.walk(input_dir):
    for file in files:
        ext = os.path.splitext(file)[-1]
        if ext == '.json':
            json_path = os.path.join(root, file)
            
            with open(json_path, encoding='utf-8') as f:
                json_file = json.load(f)
            
            for ann in json_file['annotations']:
                id = ann['category_id']
                id_list.append([id, file])

df = pd.DataFrame(id_list, columns=['id', 'json'])
save_df = df[df['id'] == int(category_id)]
save_df.to_excel(f'{output_dir}/count_id_{category_id}.xlsx', index=False)
print(f'{output_dir}/count_id_{category_id}.xlsx', '저장!!')