import cv2
import os, sys
import pandas as pd
from collections import defaultdict
from tqdm import tqdm

_, excel_dir, input_dir, output_dir = sys.argv

excel_dict = defaultdict(list)
excel = pd.read_excel(excel_dir)
excel['folder_1'] = excel['file_name'].str.split('_').str[0]
excel['folder_2'] = excel['file_name'].str.split('_').str[:3].str.join('_')
excel['mp4_name'] = excel['file_name'].str.split('_').str[:4].str.join('_')
excel = excel[['mp4_name', '저장폴더경로', 'folder_1', 'folder_2', '추출 frame_no']]
excel.apply(lambda x: excel_dict[x['mp4_name']].append({'저장폴더경로':x['저장폴더경로'], 'folder_1':x['folder_1'], 'folder_2':x['folder_2'], 'frame_no':x['추출 frame_no']}), axis=1)

mp4_dict = {}
for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.mp4':
            mp4_path = os.path.join(root, file)
            mp4_dict[mp4_path] = file

for mp4_path, file in tqdm(mp4_dict.items()):
    filename, ext = os.path.splitext(file)
    frame_dict = {}
    frame_file = excel_dict[filename]
    
    for idx, info in enumerate(frame_file):
        no = info['frame_no']
        frame_dict[no] = idx

    # mp4 읽어오기
    video = cv2.VideoCapture(mp4_path)

    currentframe = 0

    # 프레임 추출
    while True:
        ret, frame = video.read()
        if not ret:
            break

        if currentframe in frame_dict.keys():
            idx = frame_dict[currentframe]
            num = str(currentframe).zfill(8)
            frame_filename = f'{filename}_{num}.jpg'
            frame_info = frame_file[idx]
            db_name = frame_info['저장폴더경로']
            folder1 = frame_info['folder_1']
            folder2 = frame_info['folder_2']
            
            folder = os.path.join(output_dir, db_name, folder1, folder2)
            os.makedirs(folder, exist_ok=True)
            frame_path = os.path.join(folder, frame_filename)
            print(frame_path)
            
            result, n = cv2.imencode('.jpg', frame)
            
            if result:
                with open(frame_path, mode='w+b') as f:
                    n.tofile(f)
                
        currentframe += 1