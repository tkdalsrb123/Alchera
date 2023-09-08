import os, sys
import pandas as pd
from collections import defaultdict

def readfiles(dir):
    file_dict = defaultdict(list)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.jpg':
                id = int(filename.split('_')[0][:3])
                id = f"{id}".zfill(3)
                file_dict[id].append(filename)

    return file_dict

_, input_dir, output_dir = sys.argv

jpg_dict = readfiles(input_dir)

df = pd.DataFrame([[k, len(v)] for k, v in jpg_dict.items()], columns=['ID', 'count'])
df.to_csv(f'{output_dir}/count.csv', index=False)

                