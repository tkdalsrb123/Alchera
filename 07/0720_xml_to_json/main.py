import os, sys, json
import xmltodict

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlstring = f.read()
    dic_data = xmltodict.parse(xmlstring)
    return dic_data

def jsonformat(width, imagename, shapes, height):
    json_format = {"imageWidth": width,
                   "imageData": "",
        "imagePath": imagename,
        "shapes":shapes,
        "imageHeight": height}
    return json_format

def sort_list(sample_list):
    key_list = ['shapes_type', 'label', 'points']
    sample_list = sorted(sample_list, key=lambda x: int(x[-1]), reverse=True)   # z_order 크기 순으로 정렬
    sample_list = list(map(lambda x: dict(zip(key_list, x[:-1])), sample_list)) # z_order 삭제
    return sample_list
    
_, input_dir, output_dir = sys.argv

for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.xml':
            xml_path = os.path.join(root, file)
            mid_dir = root.replace(input_dir, '')[1:]
            # mid_dir = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
            folder = os.path.join(output_dir, mid_dir)
            os.makedirs(folder, exist_ok=True)
            
            xml_data = readxml(xml_path)
            
            for image in xml_data['annotations']['image']:
                if len(image.keys()) > 4:   # polygon이 있는 경우
                    sub_list = []
                    for key, val in image.items():
                        if key == '@name':
                            imagename = val
                        elif key == '@width':
                            width = val
                        elif key == '@height':
                            height = val
                        elif '@' not in key:    # image 자식 태그일 경우(polygon)
                            shape_type = key
                            for poly in val:
                                label = poly['@label']
                                points = [ [float(xy.split(',')[0]),float(xy.split(',')[1])]  for xy in poly['@points'].split(';')]
                                z_order = poly['@z_order']
                                
                                sub_list.append([shape_type, label, points, z_order])
                        shapes_list = sort_list(sub_list)
                    
                    json_data = jsonformat(width, imagename, shapes_list, height)
                    
                    json_name = os.path.splitext(imagename)[0]
                    save_json_dir = os.path.join(folder, f'{json_name}.json')
                    
                    with open(save_json_dir, 'w') as o:
                        json.dump(json_data, o, ensure_ascii=False, indent=2)
                    print(save_json_dir, '저장!!')
                            
                        
                                
                                
                                
                            