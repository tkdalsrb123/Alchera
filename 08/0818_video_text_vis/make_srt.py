import cv2, os, sys, json
from collections import defaultdict
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import pandas as pd

def str_time(timestamp):
    start = '00:0' + timestamp[0].replace('.', ',')[:-2]
    end = '00:0' + timestamp[1].replace('.', ',')[:-2]
    
    str_time = f'{start} --> {end}'

    return str_time

_, json_dir, output_dir = sys.argv

# srt 파일 만들기
json_dict = defaultdict(str)
for root, dirs, files in os.walk(json_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.json':
            json_path = os.path.join(root, file)
            mid = '\\'.join(root.split('\\')[len(json_dir):])
            folder = os.path.join(output_dir, mid)
            os.makedirs(folder, exist_ok=True)
            output_path = os.path.join(folder, filename)
            
            json_dict[filename] = json_path

            with open(json_path, 'r', encoding='utf-8') as f:
                json_file = json.load(f)
            
            subtitle_list = []
            seq = 1
            for info in json_file['trigger_info']:
                text = info['trigger_action']
                if text != 'null':
                    timestamps = str_time(info['timestamps'])
                    subtitle_list.append([f'{seq}\n{timestamps}\n{text}\n\n'])
                    seq += 1
                    
            df = pd.DataFrame(subtitle_list, columns=['srt'])
            
            df['srt'].to_csv(f'{output_path}.srt', header=None, mode='w', index=False, encoding='utf-8')

            with open(f'{output_path}.srt', 'r', encoding='utf-8') as file:
                srt_file = file.read()
                
                srt_file = srt_file.replace('"', '')
                
            with open(f'{output_path}.srt', 'w', encoding='utf-8') as file:
                file.write(srt_file)


# for root, dirs, files in os.walk(mp4_dir):
#     for file in files:
#         filename, ext = os.path.splitext(file)
#         if ext == '.mp4':
#             mp4_path = os.path.join(root, file)
            
#             json_path = json_dict[filename]
            
            # with open(json_path, 'r', encoding='utf-8') as f:
            #     json_file = json.load(f)
            
            # subtitle_list = []
            # seq = 0
            # for info in json_file['trigger_info']:
            #     text = info['trigger_action']
            #     if text != 'null':
            #         timestamps = str_time(info['timestamps'])
            #         subtitle_list.append([f{seq}{timestamps} text])
            #         seq += 1
                    
            # pd.DataFrame()
            
            # generator = lambda txt: TextClip(txt, font='Georgia-Regular', fontszie=25, color='red')
            # sub = SubtitlesClip("subtitles.srt", generator)
            # video = VideoFileClip(mp4_path)
            # out_video = Compos
            #     subtitle_list.append([timestamps, text])
            
            # video = VideoFileClip(mp4_path)
            