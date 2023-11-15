import os, sys, logging
import pandas as pd
from tqdm import tqdm

def readfile(dir):
    for root, _, files in tqdm(os.walk(dir)):
        if len(files)>0:
            path = root.split('\\')[2:]
            count = len(files)
            path.append(count)
            
            file_info.append(path)

def main(dir):
    raw_dir = os.path.join(dir, '01.원천데이터')
    label_dir = os.path.join(dir, '02.라벨링데이터')
    
    print('원천데이터')
    readfile(raw_dir)
    print('라벨링데이터')
    readfile(label_dir)
    
    df = pd.DataFrame(file_info)
    df.to_excel('./nas_filecount.xlsx', index=False, header=False)
    
if __name__ == '__main__':
    _, input_dir = sys.argv
    file_info = []
    main(input_dir)
    
    