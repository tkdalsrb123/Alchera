import os, sys, logging, json, cv2, itertools, math
import numpy as np
from collections import defaultdict, Counter
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
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext == Ext:
                file_path = os.path.join(root, file)
            
                file_dict[filename] = file_path
    return file_dict

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def readJson(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_img(img_path, img, ext):
    result, encoded_img = cv2.imencode(f'.{ext}', img)
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)

def img_vis(img, pts, color, text=None):
    cv2.circle(img, pts, n, color, -1)
    if text:
        cv2.putText(img, (pts[0]+n+8, pts[1]), text, cv2.FONT_HERSHEY_SIMPLEX, 1, color)

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def calculate_distances(points):
    distances = {}
    for pair in itertools.combinations(points, 2):
        if pair[0] != pair[1]:
            distances[pair] = distance(pair[0], pair[1])
    return distances

if __name__ == '__main__':
    _, img_dir, json_dir, output_dir = sys.argv
    
    img_dict = readfiles(img_dir, '.jpg') 
    json_dict = readfiles(json_dir, '.json')
    
    for filename, json_path in tqdm(json_dict.items()):
        
        img_path = img_dict[filename]

        output_img_path = makeOutputPath(img_path, img_dir, output_dir, 'jpg')
        json_file = readJson(json_path)

        pts_list = json_file['face_landmark']
        pts_len = len(pts_list)
        
        pts_list = [tuple(p) for p in pts_list]
    
        distances = calculate_distances(pts_list)
        
        sorted_distances = sorted(distances.items(), key=lambda x: x[1])
                
        first_distance_pts = sorted_distances[0][0]
        second_distance_pts = sorted_distances[1][0]
        
        pts_count = Counter(pts_list)
        
        pts_set = set(pts_list)
        
        img = read_img(img_path)
        
        n = 5
        for pts in pts_list:
            color = (0, 0, 255)
            if pts in pts_set:
                color = (0, 255, 0)
                text = pts_count[pts]
                img_vis(img, pts, color, text)
            elif pts == first_distance_pts[0] or pts == second_distance_pts[0]:
                color = (255, 255, 0)
                img_vis(img, pts, color)
            elif pts == first_distance_pts[1] or pts == second_distance_pts[1]:
                color = (0, 255, 255)
                img_vis(img, pts, color)
            else:
                img_vis(img, pts, color)
        
        cv2.putText(img, (5, 5), str(pts_len), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        
        
        
        save_img(output_img_path, img)