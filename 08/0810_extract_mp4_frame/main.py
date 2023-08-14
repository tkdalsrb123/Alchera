import cv2
import os, sys
from collections import defaultdict
from tqdm import tqdm

def extract_frame(Video, Old_FrameList, New_FrameList, Old_Folder, New_Folder):
    currentframe = 0
    
    while True:
        ret, frame = Video.read()
        if not ret:
            break
        
        if currentframe % 10 == 0 or currentframe % 10 == 1 or currentframe % 10 == 2:
            if currentframe in Old_FrameList:
                file_num = str(currentframe).zfill(8)
                frame_filename = f'{file}_{file_num}.jpg'
                
                frame_path = os.path.join(Old_Folder, frame_filename)
                print(frame_path)

                result, n = cv2.imencode('.jpg', frame)
                if result:
                    with open(frame_path, mode='w+b') as f:
                        n.tofile(f)
            elif currentframe in New_FrameList:
                file_num = str(currentframe).zfill(8)
                frame_filename = f'{file}_{file_num}.jpg'
                
                frame_path = os.path.join(New_Folder, frame_filename)
                print(frame_path)

                result, n = cv2.imencode('.jpg', frame)
                if result:
                    with open(frame_path, mode='w+b') as f:
                        n.tofile(f)
        
        currentframe += 1
            
_, old_db_dir, new_db_dir, mp4_dir = sys.argv

db_list = []
db_dict = defaultdict(list)
for root, dirs, files in os.walk(old_db_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.jpg':
            split_file = filename.split('_')
            
            folder1 = split_file[0]
            folder2 = '_'.join(split_file[:3])
            mp4_name = '_'.join(split_file[:4])
            idx = int(split_file[-1]) - 1 
            db_dict[mp4_name].append({'folder1':folder1, 'folder2':folder2, 'idx':idx})


mp4_dict = {}
for root, dirs, files in os.walk(mp4_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.mp4':
            mp4_path = os.path.join(root, file)
            mp4_dict[mp4_path] = filename


for mp4_path, file in tqdm(mp4_dict.items()):
    old_file_list = []
    new_file_list = []
    if len(db_dict[file]) != 0:
        if (len(db_dict[file])) == (db_dict[file][-1]['idx'] - db_dict[file][0]['idx'] +1):     # 프레임이 끊기지 않는 경우
            folder1 = db_dict[file][0]['folder1']
            folder2 = db_dict[file][0]['folder2']
            video = cv2.VideoCapture(mp4_path)
            old_folder = os.path.join(new_db_dir,'old_db', folder1, folder2)
            new_folder = os.path.join(new_db_dir,'new_db', folder1, folder2)
            os.makedirs(old_folder, exist_ok=True)
            os.makedirs(new_folder, exist_ok=True)
            
            for i in range(0, len(db_dict[file]), 3):
                num = int(db_dict[file][i]['idx'])
                frame_num = 30 * (num//3) + (num%3)
                
                old_file_list.append(frame_num)
                
                if i < len(db_dict[file])-3:    # 마지막 old db 프레임이 아닐 때 
                    for i in range(2):
                        frame_num += 10
                        
                        new_file_list.append(frame_num)

                elif i >= len(db_dict[file])-3:     # 마지막 old db 프레임일 때
                    if len(db_dict[file]) % 3 == 0:
                        for i in range(2):
                            frame_num += 10

                            new_file_list.append(frame_num)
                                    
                    elif len(db_dict[file]) % 3 == 1:
                        pass
                    
                    elif len(db_dict[file]) % 3 == 2:
                        frame_num += 10

                        new_file_list.append(frame_num)
                        
            extract_frame(video, old_file_list, new_file_list, old_folder, new_folder)

        elif (len(db_dict[file])) != (db_dict[file][-1]['idx'] - db_dict[file][0]['idx'] +1):   # 중간에 프레임이 끊기는 경우
            frame_list = []
            n = 0
            for i, v in enumerate(db_dict[file]):   # 끊기는 프레임 기준으로 자르기
                if i+1 == len(db_dict[file]):
                    break
                if (v['idx'] + 1) != (db_dict[file][i+1]['idx']):
                    frame_list.append(db_dict[file][n:i+1])
                    n = i
            frame_list.append(db_dict[file][n+1:])

            for index, j in enumerate(frame_list):
                video = cv2.VideoCapture(mp4_path)
                folder1 = j[0]['folder1']
                folder2 = j[0]['folder2']
                old_folder = os.path.join(new_db_dir,'old_db', folder1, folder2)
                new_folder = os.path.join(new_db_dir,'new_db', folder1, folder2)
                os.makedirs(old_folder, exist_ok=True)
                os.makedirs(new_folder, exist_ok=True)
                if index != len(frame_list)-1:  # 끊긴 프레임 뭉치 중 마지막 뭉치가 아닌 경우
                    for z in range(0, len(j), 3):
                        num = int(j[z]['idx'])
                        frame_num = 30 * (num//3) + (num%3)
                        
                        old_file_list.append(frame_num)
                                
                        if z < len(j)-3:    # 마지막 old db 프레임이 아닐 때 
                            for i in range(2):
                                frame_num += 10
                                
                                new_file_list.append(frame_num)
                                        
                        elif z >= len(j)-3:     # 마지막 old db 프레임일 때
                            if index == 0:
                                if len(j) % 3 == 0:     
                                    n = int(j[0]['idx'])
                                    frame_n = 30 * (n//3) + (n%3)
                                    for i in range(2):
                                        frame_n -= 10
                                        new_file_list.append(frame_n)
                                        
                                elif len(j) % 3 == 1:
                                    pass
                                
                                elif len(j) % 3 == 2:
                                    frame_n -= 10
                                    new_file_list.append(frame_n)
                                    
                            elif index != 0:
                                if len(j) % 3 == 0:     
                                    frame_n -= 10
                                    for i in range(2):
                                        frame_n -= 10
                                        new_file_list.append(frame_n)
                                        
                                elif len(j) % 3 == 1:
                                    pass
                                
                                elif len(j) % 3 == 2:
                                    frame_n -= 10
                                    new_file_list.append(frame_n)
                            
                    
                elif index == len(frame_list)-1:  # 끊긴 프레임 뭉치 중 마지막 뭉치
                    for z in range(0, len(j), 3):
                        num = int(j[z]['idx'])
                        frame_num = 30 * (num//3) + (num%3)
                        
                        old_file_list.append(frame_num)
                                
                        if z < len(j)-3:    # 마지막 old db 프레임이 아닐 때 
                            for i in range(2):
                                frame_num += 10
                                
                                new_file_list.append(frame_num)
                                        
                        elif z >= len(j)-3:     # 마지막 old db 프레임일 때
                            if len(j) % 3 == 0:     
                                for i in range(2):
                                    frame_num += 10
                                    
                                    new_file_list.append(frame_num)
                            elif len(j) % 3 == 1:
                                pass
                            
                            elif len(j) % 3 == 2:
                                frame_num += 10

                                new_file_list.append(frame_num)
    
            extract_frame(video, old_file_list, new_file_list, old_folder, new_folder)
  
    elif len(db_dict[file]) == 0:
        print(mp4_path, '매칭실패!!') 