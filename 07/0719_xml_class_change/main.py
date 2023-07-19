import os, sys
import xmltodict

def readxml(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        xmlString = f.read()
    dic_data = xmltodict.parse(xmlString)
    return dic_data

def saveXml(pathXml, objXml):
    with open(pathXml, 'w') as f:
        f.write(xmltodict.unparse(objXml, pretty=True))

def reviseclass(key, whattype):
    if whattype == list:
        for poly in key:
            if poly['@label'] == 'rug':
                poly['@label'] = 'mat'
    elif whattype == dict:
        if key['@label'] == 'rug':
            key['@label'] = 'mat'

_, input_dir = sys.argv

for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.xml':
            xml_path = os.path.join(root, file)
            print(xml_path, '수정!!!')
            
            xml_file = readxml(xml_path)
            
            # change label name rug to mat
            for image in xml_file['annotations']['image']:
                if 'polygon' in image.keys():
                    if 'polyline' not in image.keys():  # polygon만 있는 경우
                        reviseclass(image['polygon'], type(image['polygon']))
                    elif 'polyline' in image.keys():    # polygon polyline 둘 다 있는 경우
                        reviseclass(image['polygon'], type(image['polygon']))
                        reviseclass(image['polyline'], type(image['polyline']))
                elif 'polyline' in image.keys():    # polyline만 있는 경우
                    reviseclass(image['polyline'], type(image['polyline']))

            saveXml(xml_path, xml_file)