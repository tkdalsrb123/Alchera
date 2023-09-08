import cv2, json, sys, os
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont
import logging
from tqdm import tqdm

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

_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

mp4_dict = readfiles(input_dir, '.mp4')
json_dict = readfiles(input_dir, '.json')

for filename, mp4_path in tqdm(mp4_dict.items()):
    json_path = json_dict[filename]
    root, file = os.path.split(mp4_path)
    mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
    folder = os.path.join(output_dir, mid)
    test_folder = os.path.join(folder, 'test')
    os.makedirs(folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)
    
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
            
            num = str(currentframe).zfill(8)
            frame_filename = f'{filename}_{num}.jpg'
            output_test_img_path = os.path.join(test_folder, frame_filename)
            output_img_path = os.path.join(folder, frame_filename)
            if currentframe == start_frame or currentframe == end_frame:
                x1 = 10
                y1 = 10

                font = cv2.FONT_HERSHEY_PLAIN
            
                overlay = frame.copy()
                
                fontScale = 3   # background 크기 조절(글씨 크기를 조절하면서 같이 조절해야함)
                text_w, text_h = cv2.getTextSize(text, font, fontScale=fontScale, thickness=1)[0]
                cv2.rectangle(overlay, (x1, y1), (x1+(text_w//5)*3+20, y1+text_h+20), (255,255,255), -1)
                alpha = 0.5  # 배경 투명도 조절
   
                fontSize = 40   # 글씨 크기 조절
                frame = cv2.addWeighted(frame, alpha, overlay, 1-alpha, 0)
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)        
                frame = Image.fromarray(frame)
                fontpath = "malgunbd.ttf"
                pil_font = ImageFont.truetype(fontpath, fontSize)
                draw = ImageDraw.Draw(frame)

                draw.text((x1+15, y1), text, font=pil_font, fill=(255, 0, 0) )

                logger.info(f"{output_img_path} 저장!!")
                frame.save(output_img_path, 'JPEG')
                frame.save(output_test_img_path, 'JPEG')

            elif currentframe >= start_frame-15 and currentframe <= start_frame+15:
                logger.info(f"{output_img_path} 저장!! 시각화 x")
                result, encoded_img = cv2.imencode('.jpg', frame)
                if result:
                    with open(output_img_path, mode='w+b') as f:
                        encoded_img.tofile(f)
                    with open(output_test_img_path, mode='w+b') as f:
                        encoded_img.tofile(f)
                            
            elif currentframe >= end_frame-15 and currentframe <= end_frame+15:
                logger.info(f"{output_img_path} 저장!! 시각화 x")
                result, encoded_img = cv2.imencode('.jpg', frame)
                if result:
                    with open(output_img_path, mode='w+b') as f:
                        encoded_img.tofile(f)
                    with open(output_test_img_path, mode='w+b') as f:
                            encoded_img.tofile(f)
            
            else:
                logger.info(f"{output_img_path} 저장!! 시각화 x")
                result, encoded_img = cv2.imencode('.jpg', frame)
                if result:
                    with open(output_img_path, mode='w+b') as f:
                        encoded_img.tofile(f)

                
            
            
            currentframe += 1