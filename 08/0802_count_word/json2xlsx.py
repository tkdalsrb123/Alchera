import os, sys, json
from collections import Counter
import pandas as pd

_, input_dir, output_dir = sys.argv

df = pd.read_excel(r"C:\Users\Alchera115\wj.alchera\Alchera_data\08\0802_count_word\특수문자셋.xlsx")
print(list(df['특수기호']))


# for root, dirs, files in os.walk(input_dir):
#     for file in files[:1]:
#         filename, ext = os.path.splitext(file)
#         if ext == '.json':
#             file_path = os.path.join(root, file)
            
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 json_file = json.load(f)
            
#             for obj in json_file['objects']:
#                 for att in obj['attributes']:
#                     for value in att['values']:
#                         text = value['value']
#                         count = Counter(text)
                        
#                         print(count)


