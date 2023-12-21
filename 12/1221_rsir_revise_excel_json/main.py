import os, sys, json, logging
import pandas as pd
from tqdm import tqdm
from collections import defaultdict

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

def saveJson(file, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(file, f, indent=2, ensure_ascii=False)

def preprocessing(data):
    data_dict = {key:val for key, val in data.to_dict().items() if val != ""}
    
    info_list.append(data_dict)

def json_format(data, quantity, name, city):
    format = {
        "Frame": quantity,
        "Source": name,
        "Time": "",
        "Location": "",
        "Weather": "",
        "RoadType": "",
        "RoadSurface": "",
        "GPSCoordinate": "41.402588,41.402588",
        "Place": city,
        "TrafficCondition": "",
        "IlluminationCondition": "",
        "CameraCondition": "",
        "TargetObjectMovement": "",
        "Label": "3d_detection_RSIR_v3"
    }
    for key, value in data.items():
        if value == 1:
            val = mapping1[key]
            if val != 'Normal':
                format[mapping2[val]] = val
            else:
                if key == '일반.2':
                    format["IlluminationCondition"] = val
                elif key == '일반.3':
                    format["CameraCondition"] = val
                elif key == '차선변경':
                    format["TargetObjectMovement"] = val
                    
    return format

mapping1 = {
    '주간': 'Day',
    '야간': 'Night',
    '고속화': 'D_Expressway',
    '도심': 'D_Road',
    '맑음': 'Sunny',
    '흐림': 'Cloudy',
    '안개': 'Fog',
    '비': 'Rain',
    '눈': 'Snow',
    '일반.1': 'General',
    'TG': 'TG',
    'IC/JC': 'IC_JC',
    '터널': 'Tunnel',
    '교차로': 'Intersection',
    '공사구간': 'RoadConstruction',
    '아스팔트': 'Asphalt',
    '콘크리트': 'Concrete',
    '보도블럭': 'Pavement',
    '흙': 'Dirt',
    '자갈': 'Pebble',
    '눈길': 'Icy',
    '빗길': 'Waterly',
    '원활': 'Light',
    '혼잡': 'Congested',
    '일반.2': 'Normal',
    '태양역광': 'DirectSunlight',
    '헤드램프': 'DirectHeadLight',
    '가로등': 'DirectStreetLight',
    '초저도도': 'VeryLowLight',
    '일반.3': 'Normal',
    '얼룩': 'Smear',
    '물맺힘': 'WaterDrop',
    '부분가림': 'PartialOcclusion',
    '물체반사': 'ReflectionFromDashboard',
    '차선유지': 'Cut-in',
    '차선변경': 'Normal',
    '기타': 'Others'
}

mapping2 = {
    'Day': 'Time',
    'Night': 'Time',
    'D_Expressway': 'Location',
    'D_Road': 'Location',
    'Sunny': 'Weather',
    'Cloudy': 'Weather',
    'Fog': 'Weather',
    'Snow': 'Weather',
    'Rain': 'Weather',
    'General': 'RoadType',
    'TG': 'RoadType',
    'IC_JC': 'RoadType',
    'Tunnel': 'RoadType',
    'Intersection': 'RoadType',
    'RoadConstruction': 'RoadType',
    'Asphalt': 'RoadSurface',
    'Concrete': 'RoadSurface',
    'Pavement': 'RoadSurface',
    'Dirt': 'RoadSurface',
    'Pebble': 'RoadSurface',
    'Icy': 'RoadSurface',
    'Waterly': 'RoadSurface',
    'Light': 'TrafficCondition',
    'Congested': 'TrafficCondition',
    'Normal': ['IlluminationCondition', "CameraCondition", "TargetObjectMovement"],    
    'DirectSunlight': 'IlluminationCondition',
    'DirectHeadLight': 'IlluminationCondition',
    'DirectStreetLight': 'IlluminationCondition',
    'VeryLowLight': 'IlluminationCondition',
    'Smear': 'CameraCondition',
    'WaterDrop': 'CameraCondition',
    'PartialOcclusion': 'CameraCondition',
    'ReflectionFromDashboard': 'CameraCondition',
    'Cut-in': 'TargetObjectMovement',
    'Others': 'TargetObjectMovement'
}

if __name__ == "__main__":
    _, excel_dir, input_dir, output_dir = sys.argv
    logger = make_logger('log.log')
    info_list = []
    df = pd.read_excel(excel_dir, na_filter=0)
    df.apply(preprocessing, axis=1)
    
    for info in tqdm(info_list):
        input_dirs = os.path.join(input_dir, info['시나리오'], info['시퀀스'], f"RR_SD_CMR_{info['위치']}")
        
        frame_list = []
        logger.info(input_dirs)
        try:
            for file in os.listdir(input_dirs):
                
                if 'Property' in file:
                    json_path = os.path.join(input_dirs, file)
                    output_json_path = makeOutputPath(json_path, input_dir, output_dir, 'json')
                elif 'Frame' in file:
                    frame_dir = os.path.join(input_dirs, file)
                    frame_list = os.listdir(frame_dir)
        except FileNotFoundError:
            print(input_dirs, '경로가 없습니다!!')
            
        if frame_list:
            json_data_list = []
            frame_list = [f"{os.path.splitext(frame)[0]}.jpg" for frame in frame_list if os.path.splitext(frame)[-1] == '.png']
            for frame in frame_list:
                json_data_list.append(json_format(info, info['수량'], frame, info['도시']))
        

            saveJson(json_data_list, output_json_path)
