import cv2
import os, sys
from collections import defaultdict
from tqdm import tqdm

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
    if (len(db_dict[file])) == (db_dict[file][-1]['idx'] - db_dict[file][0]['idx'] +1):     # 프레임이 끊기지 않는 경우
        for i in range(0, len(db_dict[file]), 3):
            folder1 = db_dict[file][i]['folder1']
            folder2 = db_dict[file][i]['folder2']
            num = int(db_dict[file][i]['idx'])
            frame_num = 30 * (num//3) + (num%3)
            
            video = cv2.VideoCapture(mp4_path)
            video.set(cv2.CAP_PROP_FRAME_COUNT, frame_num)
            
            old_folder = os.path.join(new_db_dir,'old_db', folder1, folder2)
            os.makedirs(old_folder, exist_ok=True)

            ret, frame = video.read()

            file_num = str(frame_num).zfill(8)
            frame_filename = f'{file}_{file_num}.jpg'
            
            frame_path = os.path.join(old_folder, frame_filename)
            print(frame_path)

            result, n = cv2.imencode('.jpg', frame)
            if result:
                with open(frame_path, mode='w+b') as f:
                    n.tofile(f)
            
            if i < len(db_dict[file])-3:    # 마지막 old db 프레임이 아닐 때 
                for i in range(2):
                    new_folder = os.path.join(new_db_dir,'new_db', folder1, folder2)
                    os.makedirs(new_folder, exist_ok=True)
                    
                    frame_num += 10

                    video.set(cv2.CAP_PROP_FRAME_COUNT, frame_num)

                    ret, frame = video.read()

                    file_num = str(frame_num).zfill(8)
                    frame_filename = f'{file}_{file_num}.jpg'
                    
                    frame_path = os.path.join(new_folder, frame_filename)
                    print(frame_path)

                    result, n = cv2.imencode('.jpg', frame)

                    if result:
                        with open(frame_path, mode='w+b') as f:
                            n.tofile(f)

            elif i >= len(db_dict[file])-3:     # 마지막 old db 프레임일 때
                if len(db_dict[file]) % 3 == 0:
                    for i in range(2):
                        new_folder = os.path.join(new_db_dir,'new_db', folder1, folder2)
                        os.makedirs(new_folder, exist_ok=True)
                        
                        frame_num += 10

                        video.set(cv2.CAP_PROP_FRAME_COUNT, frame_num)

                        ret, frame = video.read()

                        file_num = str(frame_num).zfill(8)
                        frame_filename = f'{file}_{file_num}.jpg'
                        
                        frame_path = os.path.join(new_folder, frame_filename)
                        print(frame_path)

                        result, n = cv2.imencode('.jpg', frame)

                        if result:
                            with open(frame_path, mode='w+b') as f:
                                n.tofile(f)
                                
                elif len(db_dict[file]) % 3 == 1:
                    pass
                
                elif len(db_dict[file]) % 3 == 2:
                    new_folder = os.path.join(new_db_dir,'new_db', folder1, folder2)
                    os.makedirs(new_folder, exist_ok=True)
                    
                    frame_num += 10

                    video.set(cv2.CAP_PROP_FRAME_COUNT, frame_num)

                    ret, frame = video.read()

                    file_num = str(frame_num).zfill(8)
                    frame_filename = f'{file}_{file_num}.jpg'
                    
                    frame_path = os.path.join(new_folder, frame_filename)
                    print(frame_path)

                    result, n = cv2.imencode('.jpg', frame)

                    if result:
                        with open(frame_path, mode='w+b') as f:
                            n.tofile(f)
                
                
            
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
            if index != (len(frame_list) -1):   # 마지막이 아닐 때
                for z in range(0, len(j), 3):
                    folder1 = j[z]['folder1']
                    folder2 = j[z]['folder2']
                    num = int(j[z]['idx'])
                    frame_num = 30 * (num//3) + (num%3)
                    
                    video = cv2.VideoCapture(mp4_path)
                    video.set(cv2.CAP_PROP_FRAME_COUNT, frame_num)
                    
                    old_folder = os.path.join(new_db_dir,'old_db', folder1, folder2)
                    os.makedirs(old_folder, exist_ok=True)

                    ret, frame = video.read()

                    file_num = str(frame_num).zfill(8)
                    frame_filename = f'{file}_{file_num}.jpg'
                    
                    frame_path = os.path.join(old_folder, frame_filename)
                    print(frame_path)

                    result, n = cv2.imencode('.jpg', frame)
                    if result:
                        with open(frame_path, mode='w+b') as f:
                            n.tofile(f)
                            
                    if z < len(j)-3:    # 마지막 old db 프레임이 아닐 때 
                        for i in range(2):
                            new_folder = os.path.join(new_db_dir,'new_db', folder1, folder2)
                            os.makedirs(new_folder, exist_ok=True)
                            
                            frame_num += 10

                            video.set(cv2.CAP_PROP_FRAME_COUNT, frame_num)

                            ret, frame = video.read()

                            file_num = str(frame_num).zfill(8)
                            frame_filename = f'{file}_{file_num}.jpg'
                            
                            frame_path = os.path.join(new_folder, frame_filename)
                            print(frame_path)

                            result, n = cv2.imencode('.jpg', frame)

                            if result:
                                with open(frame_path, mode='w+b') as f:
                                    n.tofile(f)
                    elif z > len(j)-3:  # 마지막 old db 프레임일 때
                        pass
                    
            elif index == (len(frame_list)-1):  # 마지막일 때
                for z in range(0, len(j), 3):
                    folder1 = j[z]['folder1']
                    folder2 = j[z]['folder2']
                    num = int(j[z]['idx'])
                    frame_num = 30 * (num//3) + (num%3)
                    
                    video = cv2.VideoCapture(mp4_path)
                    video.set(cv2.CAP_PROP_FRAME_COUNT, frame_num)
                    
                    old_folder = os.path.join(new_db_dir,'old_db', folder1, folder2)
                    os.makedirs(old_folder, exist_ok=True)

                    ret, frame = video.read()

                    file_num = str(frame_num).zfill(8)
                    frame_filename = f'{file}_{file_num}.jpg'
                    
                    frame_path = os.path.join(old_folder, frame_filename)
                    print(frame_path)

                    result, n = cv2.imencode('.jpg', frame)
                    if result:
                        with open(frame_path, mode='w+b') as f:
                            n.tofile(f)
                            
                    if z < len(j)-3:    # 마지막 old db 프레임이 아닐 때 
                        for i in range(2):
                            new_folder = os.path.join(new_db_dir,'new_db', folder1, folder2)
                            os.makedirs(new_folder, exist_ok=True)
                            
                            frame_num += 10

                            video.set(cv2.CAP_PROP_FRAME_COUNT, frame_num)

                            ret, frame = video.read()

                            file_num = str(frame_num).zfill(8)
                            frame_filename = f'{file}_{file_num}.jpg'
                            
                            frame_path = os.path.join(new_folder, frame_filename)
                            print(frame_path)

                            result, n = cv2.imencode('.jpg', frame)

                            if result:
                                with open(frame_path, mode='w+b') as f:
                                    n.tofile(f)
                                    
                    elif z >= len(j)-3:     # 마지막 old db 프레임일 때
                        if len(j) % 3 == 0:     
                            for i in range(2):
                                new_folder = os.path.join(new_db_dir,'new_db', folder1, folder2)
                                os.makedirs(new_folder, exist_ok=True)
                                
                                frame_num += 10

                                video.set(cv2.CAP_PROP_FRAME_COUNT, frame_num)

                                ret, frame = video.read()

                                file_num = str(frame_num).zfill(8)
                                frame_filename = f'{file}_{file_num}.jpg'
                                
                                frame_path = os.path.join(new_folder, frame_filename)
                                print(frame_path)

                                result, n = cv2.imencode('.jpg', frame)

                                if result:
                                    with open(frame_path, mode='w+b') as f:
                                        n.tofile(f)
                        elif len(j) % 3 == 1:
                            pass
                        
                        elif len(j) % 3 == 2:
                            new_folder = os.path.join(new_db_dir,'new_db', folder1, folder2)
                            os.makedirs(new_folder, exist_ok=True)
                            
                            frame_num += 10

                            video.set(cv2.CAP_PROP_FRAME_COUNT, frame_num)

                            ret, frame = video.read()

                            file_num = str(frame_num).zfill(8)
                            frame_filename = f'{file}_{file_num}.jpg'
                            
                            frame_path = os.path.join(new_folder, frame_filename)
                            print(frame_path)

                            result, n = cv2.imencode('.jpg', frame)

                            if result:
                                with open(frame_path, mode='w+b') as f:
                                    n.tofile(f)