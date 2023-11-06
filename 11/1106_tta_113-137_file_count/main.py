import os, sys
import pandas as pd

if __name__ == '__main__':
    _, input_dir, output_dir =  sys.argv

    list2df = []
    for root, dirs, files in os.walk(input_dir):
        if files:
            files = [file for file in files if os.path.splitext(file)[-1] == '.json']
            depth = root.split('\\') 
            count = len(files)
            
            depth.append(count)
            list2df.append(depth)
            
    df = pd.DataFrame(list2df)
    df.to_excel(f'{output_dir}/file_count.xlsx', index=False, header=None)
