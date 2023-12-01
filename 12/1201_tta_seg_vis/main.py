import os, sys, json, cv2, logging
import numpy as np
from osgeo import ogr, osr
from osgeo import gdal
from tqdm import tqdm
from collections import defaultdict

gdal.SetConfigOption('CPL_LOG', 'ERROR')

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

# def read_img(img_path):
#     img = cv2.imread(img_path , cv2.IMREAD_UNCHANGED)
#     return img

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_img(img_path, img, ext):
    result, encoded_img = cv2.imencode(f'.{ext}', img)
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)
            
def change_coor(image, polygon_coords):
    geotransform = image.GetGeoTransform()
    origin_x, pixel_width, _, origin_y, _, pixel_height = geotransform

    image_polygon = []
    for geographic_coords in polygon_coords:
        image_x = int((geographic_coords[0] - origin_x) / pixel_width)
        image_y = int((origin_y - geographic_coords[1]) / pixel_height)
        image_polygon.append([abs(image_x), abs(image_y)])
        
    return image_polygon

color = {'001':(242, 185, 182), '002': (159, 141, 242)}
if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    json_dict = readfiles(input_dir, '.json')
    img_dict = readfiles(input_dir, '.tif')

    for filename, json_path in tqdm(json_dict.items()):
        img_path = img_dict[filename]
        output_img_path = makeOutputPath(img_path, input_dir, output_dir, 'png')
        img = read_img(img_path)

        # new_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        gdal_img = gdal.Open(img_path, gdal.GA_Update)
        data = readJson(json_path)
        
        for feature in data['annotation']['features']:
            CODE = feature['properties']['CODE']
            coordinates = feature['geometry']['coordinates'][0][0]
            pts = change_coor(gdal_img, coordinates)
            pts = np.array(pts, dtype=np.int32)
            cv2.fillPoly(img, [pts], color[CODE])

        save_img(output_img_path, img, 'png')