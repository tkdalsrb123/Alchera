import os, sys
import pandas as pd
from collections import defaultdict
from tqdm import tqdm


if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    file_dict = defaultdict(lambda: defaultdict(str))
    for root, dirs, files in os.walk(input_dir):
        if len(files) > 0 and 'annotation' in root:
            depth1 = root.split('\\')[-4]
            depth2 = root.split('\\')[-3]
            files = [ file for file in files if os.path.splitext(file)[-1] == '.xml']
            count = len(files)
            file_dict[depth1][depth2] = count
  
    tf = 'true'
    list2df = []
    for depth1, depth2 in file_dict.items():
        for key, val in depth2.items():
            
            if 'LH' in key:
                lh_count = val
            elif 'RH' in key:
                rh_count = val
        
        if lh_count != rh_count:
            tf = 'false'
        
        list2df.append([depth1, lh_count, rh_count, tf])

    df = pd.DataFrame(list2df, columns=['Depth', 'LH', 'RH', 'True/False'])
    df.to_excel(f'{output_dir}/file_count.xlsx', index=False)