import os, sys, cv2, json
from collections import defaultdict
from moviepy.editor import VideoFileClip
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def pipeline(frame):
    global i
    if i < df.shape[0]:
        frame = Image.fromarray(frame)
        w, h = frame.size
        fontpath = 'C:\Windows\Fonts\H2HDRM.ttf'
        font = ImageFont.truetype(fontpath, 50)
        draw = ImageDraw.Draw(frame)
        text = df.iloc[i].sentence
        tw, th = font.getsize(text)
        draw.text((int(w/2)-tw/2, int(h//8 * 7)-int(th/2)), text, font=font, fill=(255, 0, 0))
        frame = np.array(frame)
        i += 1

    return frame

def replace_time(timestamp):
    start_m = int(timestamp[0].split('.')[0].split(':')[0])
    start_s = int(timestamp[0].split('.')[0].split(':')[-1])
    end_m = int(timestamp[1].split('.')[0].split(':')[0])
    end_s = int(timestamp[1].split('.')[0].split(':')[-1])

    if start_m > 0:
        seconds = start_m * 60
        start_s += seconds
    if end_m > 0:
        seconds = end_m * 60
        end_s += seconds
    return [start_s, end_s]

_, json_dir, mp4_dir, save_mp4_dir = sys.argv

# json 파일
json_dict = defaultdict(str)
for root, dirs, files in os.walk(json_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.json':
            json_path = os.path.join(root, file)
            
            json_dict[filename] = json_path
            
# mp4 파일
for root, dirs, files in os.walk(mp4_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.mp4':

            mp4_path = os.path.join(root, file)
            mid = '\\'.join(root.split('\\')[len(mp4_dir.split('\\')):])
            folder = os.path.join(save_mp4_dir, mid)
            os.makedirs(folder, exist_ok=True)
            output_mp4_path = os.path.join(folder, file)
            
            json_path = json_dict[filename]
            
            with open(json_path, 'r', encoding='utf-8') as f:
                json_file = json.load(f)
            
            vis_list = []
            for info in json_file['trigger_info']:
                text = info['trigger_action']
                if text != 'null':
                    timestamp = replace_time(info['timestamps'])

                    vis_list.append([timestamp, text])

            df_list = []
            for vis in vis_list: 
                duration = vis[0]
                text = vis[1]
                start_frame = duration[0]*30
                end_frame = duration[1]*30 - 1
                for i in range(start_frame, end_frame):
                    df_list.append([i, text])
                    
            df = pd.DataFrame(df_list, columns=['frame', 'sentence'])
            i=0
            video = VideoFileClip(mp4_path)
            out_video = video.fl_image(pipeline)
            out_video.write_videofile(output_mp4_path)
  
                    