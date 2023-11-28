import os, sys, shutil
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
tqdm.pandas()

def readfiles(dir, Ext):
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext == Ext:
                file_path = os.path.join(root, file)
            
                file_dict[filename] = file_path
    return file_dict

def frame_copy(x):
    no_frame_num = '_'.join(x['start'].split('_')[:5])
    start_frame_num = int(os.path.splitext(x['start'])[0].split('_')[-1])
    end_frame_num = int(os.path.splitext(x['end'])[0].split('_')[-1])
    frame_list = [f"{no_frame_num}_{str(i).zfill(8)}" for i in range(start_frame_num, end_frame_num+1)]
    for frame_name in frame_list:
        jpg_path = jpg_dict.get(frame_name)
        shutil.copy2(jpg_path, f'{output_dir}/{frame_name}.jpg')
    
if __name__ == "__main__":
    _, input_dir, csv_dir, output_dir = sys.argv

    jpg_dict = readfiles(input_dir, '.jpg')

    df = pd.read_csv(csv_dir, encoding='utf-8')
    df.progress_apply(frame_copy, axis=1)
    