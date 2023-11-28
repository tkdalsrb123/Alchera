import os, sys, shutil,json, logging
import pandas as pd
from collections import defaultdict
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
                if filename == 'video':
                                
                    file_dict[root.split('\\')[-2]] = file_path
                else:
                    file_dict[filename] = file_path
                    
    return file_dict

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def makeOutputPath(file_path, file_dir, output_dir, new_name, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    if filename == 'video':
        mid_dir = '\\'.join(relpath.split('\\')[:-3])
    else:
        mid_dir = os.path.split(relpath)[0]
        
    output_path = os.path.join(output_dir, mid_dir, f"{new_name}{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def error_check(text=""):
    if len(text) > 10:
        error_list.append(filename)
        text = ""
    return text
        
def make_env_text(environment):
    space = environment['space_type']
    if space == 'indoor' or space == '실내':
        back = error_check(environment['indoor']['background_type'])
        lig_type = error_check(environment['indoor']['lighting_type'])
        lig_color = error_check(environment['indoor']['lighting_color'])
        text = '_'.join([back, lig_type, lig_color])

    elif space == 'outdoor' or space == '실외':
        day = environment['outdoor']['day_night']
        sun = str(environment['outdoor']['is_sunlight'])
        place = environment['outdoor']['place']
        text = '_'.join([day, sun, place])
    
    return text


if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    
    mp4_dict = readfiles(input_dir, '.mp4')
    json_dict = readfiles(input_dir, '.json')
    
    error_list = []
    for filename, json_path in tqdm(json_dict.items()):
        logger.info(json_path)
        mp4_path = mp4_dict.get(filename)
        if mp4_path:
            logger.info(mp4_path)
            data = readJson(json_path)
            
            mobile_no = data['tester']['mobile_no']
            gender = data['tester']['gender']
            env_text = make_env_text(data['environment'])
            text_type = data['test_type']

            new_filename = '_'.join([mobile_no, gender, env_text, text_type])
            output_json_path = makeOutputPath(json_path, input_dir, output_dir, new_filename, '.json')        
            output_mp4_path = makeOutputPath(mp4_path, input_dir, output_dir, new_filename, '.mp4')
            
            shutil.copy2(json_path, output_json_path)
            shutil.copy2(mp4_path, output_mp4_path)
    
    df = pd.DataFrame(error_list, columns=['filename'])
    df.to_excel(f'./error_list.xlsx', index=False)
        
        
        