import os, sys, logging, json, cv2
import numpy as np
from tqdm import tqdm
from collections import defaultdict
from label import label

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
    with open(path, 'r', encoding='utf-8') as f:
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
            
def add_margin_to_image(image, margin_color=(255, 255, 255)):
    # Get the image dimensions
    height, width = image.shape[:2]

    margin = round(width//3)
    # Create a new blank image with extended width for the margin
    new_width = width + margin
    new_image = np.zeros((height, new_width, 3), np.uint8)

    # Fill the new image with a specific color (default: white)
    new_image[:, :] = margin_color

    # Place the original image onto the new image with margin
    new_image[:, :width] = image

    return new_image, margin

def check_duplication(data):
    point_list = [joint_array['point'] for joint_array in data]
  
    set_point = extract_duplicate_points(point_list)
    return set_point

def extract_duplicate_points(nested_points):
    point_tuples = [tuple(point) for point in nested_points]

    unique_points = set()
    duplicate_points = set()

    for point_tuple in point_tuples:
        if point_tuple not in unique_points:
            unique_points.add(point_tuple)
        else:
            duplicate_points.add(point_tuple)

    duplicate_points = [list(point) for point in duplicate_points]
    return duplicate_points

def get_points(_type, joint_data):
    points_list = []
    for t in _type:
        p_list = []
        for idx in t:
            points = ([round(point) for point in joint_data[idx]['point']], joint_data[idx]['occlusion_yn'], joint_data[idx]['joint_category'])
            p_list.append(points)
        points_list.append(p_list)
    return points_list

def vis(image, all_point_list, duplicate_point, margin):
    h, w, _ = image.shape
    w = w - margin
    duplicate_point =  [[round(p) for p in point] for point in duplicate_point]
    val = 30
    for point_list in all_point_list:
        
        points = np.array([p[0] for p in point_list], np.int32)
        cv2.polylines(image, [points], isClosed=False, color=(0, 255, 255), thickness=2)
        
        for point, occlusion, category in point_list:
            
            if occlusion == 'N':
                color = (0, 255, 255)
            else:
                color = (0, 0, 255)
            
            if point not in duplicate_point:
                cv2.circle(image, tuple(point), radius=3, color=color, thickness=-1)
            
            else:

                cv2.circle(image, tuple(point), radius=3, color=(255,0,0), thickness=-1)
                cv2.putText(image, f"{category} : {occlusion}", (w, val), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
                val += 30
        
def visualization(uni1, uni2, data, image, output_path):
    if uni1 == "MOVE":
        image, margin = add_margin_to_image(image)
        joint_dict = {joint_array['joint_id']: joint_array for joint_array in data['horse_move']['joint_array']}
        duplication_points = check_duplication(data['horse_move']['joint_array'])
        if uni2 == 'REAR':
            points = get_points(rear, joint_dict)
            vis(image, points, duplication_points, margin)
            
        elif uni2 == 'FRONT':
            points = get_points(front, joint_dict)
            vis(image, points, duplication_points, margin)
            
        elif uni2 == "LEFT":
            points = get_points(left, joint_dict)
            vis(image, points, duplication_points, margin)
            
        elif uni2 == 'RIGHT':
            points = get_points(right, joint_dict)
            vis(image, points, duplication_points, margin)
                        
    
    elif uni1 == "HOOF":
        text = data['horse_hoof']['balance']
        image = label(image, text, 50, (0,0,0), (0, 0), 0.5)
        for name, point in data['horse_hoof']['balance_point'].items():
            
            color = hoof_color[name.split('_')[-1]]
            if point != None:
                cv2.circle(image, tuple(point), radius=15, color=color, thickness=-1)
                
    save_img(output_path, image, 'png')
    
rear = [[71, 69, 67, 63, 65, 61, 60, 62, 66, 64, 68, 70, 72]]
front = [[40, 41, 42], [51, 49, 47, 44, 45, 43, 46, 48, 50]]
left = [[1, 2, 3, 4, 5, 6, 7, 9, 10], [4, 12, 11, 14, 16, 18, 20, 22], [5, 24], [5, 25, 27, 29, 31, 33, 35, 37]]
right = [[1, 2, 3, 4, 5, 6, 8, 9, 10], [4, 13, 11, 15, 17, 19, 21, 23], [5, 24], [5, 26, 28, 30, 32, 34, 36, 38]]

hoof_color = {
    'point01': (47, 255, 173),
    'point02': (255, 0, 0),
    'point03': (0, 0, 255),
    'point04': (0, 255, 255)
}

if __name__ == "__main__":
    _, img_dir, json_dir, output_dir = sys.argv
    
    img_dict = readfiles(img_dir, '.png')
    json_dict = readfiles(json_dir, '.json')

    for filename, json_path in tqdm(json_dict.items()):
        MH = filename.split('_')[1]
        DREC = filename.split('_')[-2]
        
        img_path = img_dict[filename]
        output_img_path = makeOutputPath(img_path, img_dir, output_dir, 'png')
        img = read_img(img_path)
        data = readJson(json_path)
        
        visualization(MH, DREC, data, img, output_img_path)
        
