import cv2, json, sys, os
from collections import defaultdict

def readfiles(dir, Ext):
    file_dict= defaultdict(str)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == Ext:
                file_path = os.path.join(root, file)
            
                file_dict[filename] = file_path
    return file_dict

_, input_dir, output_dir = sys.argv

mp4_dict = readfiles(input_dir, '.mp4')
json_dict = readfiles(input_dir, '.json')

for filename, mp4_path in mp4_dict:
    json_path = json_dict[filename]

    with open(json_path, encoding='UTF-8') as f:
        json_file = json.load(f)
    
    start_frame = json_file['sensordata']['fall_start_frame']
    end_frame = json_file['sensordata']['fall_end_frame']
    text = json_file['scene_info']['scene_cat_name']
    
    if (end_frame - start_frame) > 0:
        
        video = cv2.VideoCapture(mp4_path)
        currentframe = 0
        
        while True:
            ret, frame = video.read() 
            if not ret:
                break
                
            if currentframe >= start_frame and currentframe <= end_frame: