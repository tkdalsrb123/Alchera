import cv2, json, sys, os
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont
import logging
from tqdm import tqdm
from label import label
import numpy as np

def make_logger(log):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # formatter
    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s:%(lineno)d] -- %(message)s")
    # file_handler
    file_handler = logging.FileHandler(log, mode='w')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    # logger.add
    logger.addHandler(file_handler)
    
    return logger


def readfiles(dir, Ext):
    file_dict= defaultdict(str)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == Ext:
                file_path = os.path.join(root, file)
            
                file_dict[filename] = file_path
    return file_dict

def saveImage(saveDir, img):
    result, encoded_img = cv2.imencode('.jpg', img)
    if result:
        with open(saveDir, mode='w+b') as f:
            encoded_img.tofile(f)

def get_time_text(second, current):
    current_second = round(second * current, 3)
    return str(current_second)
    
_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

mp4_dict = readfiles(input_dir, '.mp4')
json_dict = readfiles(input_dir, '.json')

for filename, mp4_path in tqdm(mp4_dict.items()):
    json_path = json_dict[filename]
    root, file = os.path.split(mp4_path)
    mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
    folder = os.path.join(output_dir, mid, filename)
    os.makedirs(folder, exist_ok=True)
    
    with open(json_path, encoding='UTF-8') as f:
        json_file = json.load(f)
    
    start_frame = json_file['sensordata']['fall_start_frame']
    end_frame = json_file['sensordata']['fall_end_frame']
    text = json_file['scene_info']['scene_cat_name']
    text2 = json_file['scene_info']['scene_IsFall']
    start_text = f"# {start_frame} / {text2} : {text}"
    end_text = f"# {end_frame} / {text2} : {text}"
    
    text_size = 200
    if (end_frame - start_frame) > 0:
        
        video = cv2.VideoCapture(mp4_path)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS) 
        duration = frame_count/fps

        perSecond = duration/frame_count

        currentframe = 0

        while True:
            ret, frame = video.read() 
            if not ret:
                break
            h, w, _ = frame.shape
            num = str(currentframe).zfill(8)
            frame_filename = f'{filename}_{num}.jpg'
            output_img_path = os.path.join(folder, frame_filename)
            if currentframe >= start_frame-20 and currentframe <= end_frame+20:
                if currentframe == start_frame:
                    time = get_time_text(perSecond, currentframe)
                    frame = label(frame, time, text_size, (0,0,0), (0, h), 0.5)
                    frame = label(frame, start_text, text_size, (0,0,255), (0,0), 0.5)
                    
                elif currentframe == end_frame:
                    time = get_time_text(perSecond, currentframe)
                    frame = label(frame, time, text_size, (0,0,0), (0, h), 0.5)
                    frame = label(frame, end_text, text_size, (0,0,255), (0,0), 0.5)
                    
                else:
                    time = get_time_text(perSecond, currentframe)
                    frame = label(frame, time, text_size, (0,0,0), (0, h), 0.5)
                    frame = label(frame, f'# {currentframe}', text_size, (0,0,255), (0,0), 0.5)
                
                saveImage(output_img_path, frame)
                logger.info(f"{output_img_path} 저장!!")
                
            currentframe += 1