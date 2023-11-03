# open_file.py
import os
import json
import cv2
import numpy as np
import xmltodict
import pandas as pd

def open_file(path, index_col=None):
    _, ext = os.path.splitext(path)

    if ext == '.json':
        with open(path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)

        return data
    elif ext in ['.png', '.jpg']:
        img_arr = np.fromfile(path, np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

        return img
    elif ext == '.xml':
        with open(path, 'r', encoding='utf-8-sig') as f:
            xml_data = f.read()

        xml_dict = xmltodict.parse(xml_data)

        return xml_dict
    elif ext == '.xlsx':
        data = pd.read_excel(path, index_col=index_col)

        return data
    elif ext == '.csv':
        data = pd.read_csv(path, index_col=index_col)

        return data
    else:
        with open(path, 'r') as f:
            data = f.read()

        return data

def save_file(data, path, index=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    _, ext = os.path.splitext(path)

    if ext == '.json':
        with open(path, 'w', encoding='utf-8-sig') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return
    elif ext in ['.png', '.jpg']:
        proceed, encoded_img = cv2.imencode('.png', data)

        if proceed:
            with open(path, mode='w+b') as f:
                encoded_img.tofile(f)

        return
    elif ext == '.xml':
        with open(path, 'w', encoding='utf-8-sig') as f:
            f.write(xmltodict.unparse(data, encoding='utf-8-sig', pretty=True))

        return
    elif ext == '.xlsx':
        data.to_excel(path, engine='xlsxwriter', index=index, header=True)

        return
    elif ext == '.csv':
        data.to_csv(path, index=index, header=True)

        return
    else:
        with open(path, 'w') as f:
            f.write(data)