import os, sys, xmltodict, json, logging
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
    file_list = []

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext == Ext:
                file_path = os.path.join(root, file)
            
                file_list.append(file_path)
    return file_list

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_folder = os.path.join(output_dir, mid_dir)
    os.makedirs(os.path.dirname(output_folder), exist_ok=True)

    return output_folder

def saveJson(file, path):
    with open(path, 'w') as f:
        json.dump(file, f, indent=2, ensure_ascii=False)
        
def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data

def jsonTree(image_name, lidar_name, segment_name, image_size, shapes_list, output_path):
    tree = {
        "image_name": image_name,
        "lidar_name": lidar_name,
        "segment_name": segment_name,
        "image_size": image_size,
        "shapes": shapes_list
    }

    logger.info(output_path)
    saveJson(tree, output_path)
if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    logger = make_logger('log.log')

    xml_list = readfiles(input_dir, '.xml')

    shapes_seq = ['Road', 'Background', 'Car']
    depth_num = '3'
    for xml_path in tqdm(xml_list, desc='read xml', position=0):
        logger.info(xml_path)
        data = readxml(xml_path)
        output_folder = makeOutputPath(xml_path, input_dir, output_dir)
        
        for img in tqdm(data['annotations']['image'], desc='create json', position=1):
            output_filename = f"{os.path.splitext(img['@name'])[0]}.json"
            image_name = img['@name'].replace('jpg', 'png')
            lidar = image_name.split('_')[2].split('-')[0]
            lidar_name = image_name.replace(lidar, 'Lidar').replace('png', 'bin')
            segment_name = image_name.replace(f'GT_{lidar}', 'SD_Color')
            
            image_size = {
                        "imgWidth": img['@width'],
                        "imgHeight": img['@height'],
                        "imgDepth": depth_num
                        }

            shapes_dict = {}
            img_poly = img['polygon']
            if type(img_poly) == dict:
                img_poly = [img_poly]
                
            for polygon in img_poly:
                Class = polygon['@label']
                points = [[float(pts.split(',')[0]), float(pts.split(',')[1])] for pts in polygon['@points'].split(';')]

                poly_att = polygon.get('attribute')
                if poly_att:
                    if type(poly_att) == dict:
                        poly_att = [poly_att]
                    Id = ""
                    # print(poly_att)
                    for att in poly_att:
                        if att['@name'] == 'ID':
                            Id = att['#text']
                        elif att['@name'] == 'subClass':
                            subclass = att['#text']
                    
                    if Class != 'Background':
                        shapes_dict.update({Class:{"class":Class, "subclass":subclass, "id":Id, "points": points, "shape_type": "Polygon"}})

                else:
                    shapes_dict.update({Class:{"class":Class, "subclass":"", "id":"", "points":[[1792.0, 0.0], [1792.0,1024.0], [-0.0,1024.0], [-0.0,0.0]], "shape_type": "Polygon"}})
        
            shapes_list = []
            for seq in shapes_seq:
                v = shapes_dict.get(seq)
                if v:
                    shapes_list.append(v)
                    
            for key, val in shapes_dict.items():
                if key not in shapes_seq:
                    shapes_list.append(val)                 
            
            output_json_path = os.path.join(output_folder, output_filename)
            
            jsonTree(image_name, lidar_name, segment_name, image_size, shapes_list, output_json_path)