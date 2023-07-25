import os, sys
import pandas as pd
from collections import defaultdict

_, input_dir, output_dir = sys.argv

file_dict = defaultdict(dict)
for root, dirs, files in os.walk(input_dir):
    if len(files) > 0:
        lhrh = root.split('\\')[-2]
        count = 0
        if 'LH' in lhrh and os.path.splitext(files[0])[-1] == '.jpg':
            seq_name = root.split('\\')[-4]
            for file in files:
                if os.path.splitext(file)[-1] == '.jpg':
                    count += 1
            file_dict[seq_name]['LH'] = count
    
        elif 'RH' in lhrh and os.path.splitext(files[0])[-1] == '.jpg':
            seq_name = root.split('\\')[-4]
            for file in files: 
                if os.path.splitext(file)[-1] == '.jpg':
                    count += 1
            file_dict[seq_name]['RH'] = count

file_list = []   
for key, val in file_dict.items():
    file_list.append([key, val['LH'], val['RH']])

df = pd.DataFrame(file_list, columns=['시퀀스 명', 'left개수', 'right개수'])
df.to_csv(f'{output_dir}/file_count.csv', index=False)
print(f'{output_dir}/file_count.csv', '저장!!')