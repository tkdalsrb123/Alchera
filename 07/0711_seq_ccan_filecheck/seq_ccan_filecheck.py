import os, sys
import pandas as pd
from collections import Counter

def processing(x):
    name, ext = os.path.splitext(x)
    if ext == '.bin' or ext == '.timestamp':
        count_name = name.split('_')[0] + ext
    elif ext == '.yuv' and 'rsir' not in name:
        count_name = name.split('_')[1] + ext
    elif ext == '.txt' and 'rsir' not in name:
        if 'time' in name:
            count_name = name.split('_')[0] + '_' + name.split('_')[2] + ext
        else:
            count_name = 'other_txt(sensorinfo, hamperv)'
    else:
        count_name = None
    
    return count_name


_, input_dir = sys.argv

count_filename = ['ccan.bin', 'ccan.timestamp', 'imu.bin', 'imu.timestamp', 'lidar.bin',
                  'lidar.timestamp','front.yuv','left.yuv','rear.yuv','right.yuv','time_front.txt',
                  'time_left.txt','time_rear.txt','time_right.txt', 'other_txt(sensorinfo, hamperv)']

csv_list = []
for root, dirs, files in os.walk(input_dir):
    if len(files) > 0:
        print(root, '체크중!!!')
        filename = list(map(processing, files))
        count = Counter(filename)   # 시퀀스 파일 안에 중복 개수 체크
        sequence = os.path.split(root)[-1]
        List = [sequence,root]
        for name in count_filename:
            List.append(count[name])
        csv_list.append(List)

count_filename.insert(0, 'sequence')
count_filename.insert(1, '경로')
df = pd.DataFrame(csv_list, columns=count_filename)

df.to_csv('./seq_ccan_filecheck.csv', index=False)
