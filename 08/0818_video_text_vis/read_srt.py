import os, sys
from collections import defaultdict
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip


_, str_dir, mp4_dir, save_mp4_dir = sys.argv

srt_dict = defaultdict(str)
for root, dirs, files in os.walk(str_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.srt':
            srt_path = os.path.join(root, file)
            
            srt_dict[filename] = srt_path


for root, dirs, files in os.walk(mp4_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.mp4':
            mp4_path = os.path.join(root, file)
            mid = '\\'.join(root.split('\\')[len(mp4_dir.split('\\')):])
            folder = os.path.join(save_mp4_dir, mid)
            os.makedirs(folder, exist_ok=True)
            output_mp4_path = os.path.join(folder, file)
            
            
            srt_path = srt_dict[filename]
            srt_path = srt_path.encode('utf-8')
            
            generator = lambda txt: TextClip(txt, font='Georgia-Regular', fontszie=25, color='red')
            
            sub = SubtitlesClip(srt_path, generator)
            video = VideoFileClip(mp4_path)
            out_video = CompositeVideoClip([clip, subtitles])
            out_video.write_videofile(output_mp4_path, fps=video.fps)