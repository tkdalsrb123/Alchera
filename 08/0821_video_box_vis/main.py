import os, sys, json
from collections import defaultdict
from tqdm import tqdm
import pandas as pd
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def read_files(path, Ext):
    
    file_dict = defaultdict(str)
    for root, dirs, files in os.walk(path):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == Ext:
                file_path = os.path.join(root, file)

                file_dict[filename] = file_path
    
    return file_dict


def replace_time(timestamp):
    m = int(timestamp.split('.')[0].split(':')[0])
    s = int(timestamp.split('.')[0].split(':')[-1])

    if m > 0:
        seconds = m * 60
        s += seconds
    if m > 0:
        seconds = m * 60
        s += seconds
    return s

_, mp4_dir, json_dir, save_dir = sys.argv

json_dict = read_files(json_dir, '.json')
mp4_dict = read_files(mp4_dir, '.mp4')

for filename, mp4_filepath in tqdm(mp4_dict.items()):
    json_filepath = json_dict[filename]
    
    root = os.path.split(mp4_filepath)[0]
    mid = '\\'.join(root.split('\\')[len(mp4_dir.split('\\')):])
    folder = os.path.join(save_dir, mid)
    os.makedirs(folder, exist_ok=True)
    
    with open(json_filepath, encoding='utf-8') as f:
        json_file = json.load(f)
    
    vis_list = []
    for info in json_file['trigger_info']:
        key = info.get('bbox')
        if key != None:
            text = info['trigger_object']
            coor = info['bbox'] # 딕셔너리 구조 {x1: , y1: , x2: , y2: }
            times = replace_time(info['time'])

            vis_list.append([times, text, coor])
            
    df_list = []
    for vis in vis_list: 
        time = vis[0]
        text = vis[1]
        coor = vis[2]
        frame = time*30
        df_list.append([frame, text, coor])
            
    df = pd.DataFrame(df_list, columns=['frame', 'text', 'coor'])
    
    if df.shape[0] > 0:
        # mp4 읽어오기
        video = cv2.VideoCapture(mp4_filepath)

        currentframe = 0

        # 프레임 추출
        i = 1
        while True:
            ret, frame = video.read()
            if not ret:
                break

            if currentframe in list(df['frame']):
                # box 시각화
                num = str(i).zfill(2)
                output_file_path = os.path.join(folder, f"{filename}_{num}.jpg")
                frame = Image.fromarray(frame)
                w, h = frame.size
                fontpath = 'C:\Windows\Fonts\H2HDRM.ttf'
                font = ImageFont.truetype(fontpath, 20)
                draw = ImageDraw.Draw(frame)
                text = df.loc[df['frame'] == currentframe, 'text'].values[0]
                coor = df.loc[df['frame'] == currentframe, 'coor'].values[0]
                
                x1 = round(w * coor['x1'])
                y1 = round(h * coor['y1'])
                x2 = round(w * coor['x2'])
                y2 = round(h * coor['y2'])
                
                if x2 > x1:
                    draw.rectangle((x1, y1, x2, y2), outline=(255, 0, 0), width=3)
                    draw.text((x1, y1, x2, y2), text, font=font, fill=(0, 0, 255))
                elif x1 < x2:
                    draw.rectangle((x2, y1, x1, y2), outline=(255, 0, 0), width=3)
                    draw.text((x2, y1, x1, y2), text, font=font, fill=(0, 0, 255))       
                
                frame = np.array(frame)
                result, n = cv2.imencode('.jpg', frame)
                
                if result:
                    with open(output_file_path, mode='w+b') as f:
                        n.tofile(f)
                print(output_file_path)
                
                i += 1
            
            currentframe += 1
    else:
        print(mp4_filepath, '시각화 데이터 없음!!')