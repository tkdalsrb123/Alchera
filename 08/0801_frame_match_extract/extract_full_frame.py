import cv2
import os, sys

_, input_dir, output_dir = sys.argv

for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.mp4':
            mp4_path = os.path.join(root, file)
            mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
            folder = os.path.join(output_dir, mid)
            os.makedirs(folder, exist_ok=True)

            # mp4 읽어오기
            video = cv2.VideoCapture(mp4_path)

            currentframe = 0
            fps = 1
            # 프레임 추출
            while True:
                ret, frame = video.read()
                if not ret:
                    break
                
                if currentframe % fps == 0:
                    num = str(currentframe).zfill(8)
                    frame_filename = f'{filename}_{num}.jpg'
                    frame_path = os.path.join(folder, frame_filename)
                    print(frame_path)
                    
                    result, n = cv2.imencode('.jpg', frame)
                    
                    if result:
                        with open(frame_path, mode='w+b') as f:
                            n.tofile(f)
                        
                currentframe += 1