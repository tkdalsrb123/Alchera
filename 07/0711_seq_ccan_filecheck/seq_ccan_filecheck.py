import os, sys
import pandas as pd
from collections import Counter

_, input_dir = sys.argv

csv_list = []
for root, dirs, files in os.walk(input_dir):
    if len(files) > 0:
        filename = list(map(lambda x: os.path.splitext(x)[0], files))
        count = Counter(filename)   # 시퀀스 파일 안에 중복 개수 체크
        for file in files:
            sequence = os.path.split(root)[-1]
            path = os.path.join(root, file)
            
            csv_list.append([sequence, file, count[os.path.splitext(file)[0]], path])

df = pd.DataFrame(csv_list, columns=['sequence', '파일명', '중복', '경로'])

df.to_csv('./seq_ccan_filecheck.csv', index=False)