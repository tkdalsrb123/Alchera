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

def change(text):
    if '+' in text:
        ts = text.split('+')
        ts = [i.strip() for i in ts]
        ts = [category.get(i) for i in ts]
        text = '+'.join(ts)

    else:   
        t = category.get(text)
        if t:
            text = t
    
    return text

def make_env_text(environment):
    space = environment['space_type']
    if space == 'indoor' or space == '실내':
        back = error_check(environment['indoor']['background_type'])
        lig_type = error_check(environment['indoor']['lighting_type'])
        lig_color = error_check(environment['indoor']['lighting_color'])
        text = '_'.join([change(space), change(back), change(lig_type), change(lig_color)])

    elif space == 'outdoor' or space == '실외':
        day = environment['outdoor']['day_night']
        sun = str(environment['outdoor']['is_sunlight'])
        place = environment['outdoor']['place']
        text = '_'.join([change(space), change(day), change(sun), change(place)])
    
    return text

def change_filename(newname, path):
    root, file = os.path.split(path)
    filename, ext = os.path.splitext(file)
    new_filename = f"{newname}{ext}"

    new_path = os.path.join(root, new_filename)
    return new_path


category = {
"실내":"indoor",
"실외":"outdoor",
"단순":"SB",
"순광":"PL",
"역광":"BL",
"백색":"WL",
"주백색":"D",
"네온":"N",
"자연광":"NL",
"복잡":"CB",
"True":"T",
"False":"F",
"버스정류장":"Bus",
"가로등":"Steetlight",
"편의점":"Store",
"주간":"Day",
"야간":"Night"}

filename_category = {'real_indoor_SB_PL_WL': '001', 'real_indoor_SB_PL_D': '002', 'real_indoor_SB_PL_N': '003', 'real_indoor_SB_PL_NL': '004', 'real_indoor_SB_PL_WL+N': '005', 'real_indoor_SB_PL_WL+NL': '006', 'real_indoor_SB_PL_WL+D': '007', 'real_indoor_SB_BL_WL': '008', 'real_indoor_SB_BL_D': '009', 'real_indoor_SB_BL_N': '010', 'real_indoor_SB_BL_NL': '011', 'real_indoor_SB_BL_WL+N': '012', 'real_indoor_SB_BL_WL+NL': '013', 'real_indoor_SB_BL_WL+D': '014', 'real_indoor_CB_PL_WL': '015', 'real_indoor_CB_PL_D': '016', 'real_indoor_CB_PL_N': '017', 'real_indoor_CB_PL_NL': '018', 'real_indoor_CB_PL_WL+N': '019', 'real_indoor_CB_PL_WL+NL': '020', 'real_indoor_CB_PL_WL+D': '021', 'real_indoor_CB_BL_WL': '022', 'real_indoor_CB_BL_D': '023', 'real_indoor_CB_BL_N': '024', 'real_indoor_CB_BL_NL': '025', 'real_indoor_CB_BL_WL+N': '026', 'real_indoor_CB_BL_WL+NL': '027', 'real_indoor_CB_BL_WL+D': '028', 'real_outdoor_Day_T_Bus': '029', 'real_outdoor_Day_T_Steetlight': '030', 'real_outdoor_Day_T_Store': '031', 'real_outdoor_Day_F_Bus': '032', 'real_outdoor_Day_F_Steetlight': '033', 'real_outdoor_Day_F_Store': '034', 'fake_indoor_SB_PL_WL': '035', 'fake_indoor_SB_PL_D': '036', 'fake_indoor_SB_PL_N': '037', 'fake_indoor_SB_PL_NL': '038', 'fake_indoor_SB_PL_WL+N': '039', 'fake_indoor_SB_PL_WL+NL': '040', 'fake_indoor_SB_PL_WL+D': '041', 'fake_indoor_SB_BL_WL': '042', 'fake_indoor_SB_BL_D': '043', 'fake_indoor_SB_BL_N': '044', 'fake_indoor_SB_BL_NL': '045', 'fake_indoor_SB_BL_WL+N': '046', 'fake_indoor_SB_BL_WL+NL': '047', 'fake_indoor_SB_BL_WL+D': '048', 'fake_indoor_CB_PL_WL': '049', 'fake_indoor_CB_PL_D': '050', 'fake_indoor_CB_PL_N': '051', 'fake_indoor_CB_PL_NL': '052', 'fake_indoor_CB_PL_WL+N': '053', 'fake_indoor_CB_PL_WL+NL': '054', 'fake_indoor_CB_PL_WL+D': '055', 'fake_indoor_CB_BL_WL': '056', 'fake_indoor_CB_BL_D': '057', 'fake_indoor_CB_BL_N': '058', 'fake_indoor_CB_BL_NL': '059', 'fake_indoor_CB_BL_WL+N': '060', 'fake_indoor_CB_BL_WL+NL': '061', 'fake_indoor_CB_BL_WL+D': '062', 'fake_outdoor_Day_T_Bus': '063', 'fake_outdoor_Day_T_Steetlight': '064', 'fake_outdoor_Day_T_Store': '065', 'fake_outdoor_Day_F_Bus': '066', 'fake_outdoor_Day_F_Steetlight': '067', 'fake_outdoor_Day_F_Store': '068'}

if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    
    mp4_dict = readfiles(input_dir, '.mp4')
    json_dict = readfiles(input_dir, '.json')
    
    error_list = []
    copy_dict = defaultdict(list)
    for filename, json_path in tqdm(json_dict.items()):
        logger.info(json_path)
        mp4_path = mp4_dict.get(filename)
        if mp4_path:
            logger.info(mp4_path)
            data = readJson(json_path)
            
            mobile_no = data['tester']['mobile_no']
            env_text = make_env_text(data['environment'])
            text_type = data['test_type']

            new_filename = '_'.join([change(text_type), env_text])
            num = filename_category.get(new_filename)
            if num:
                new_filename = f"{num}_{new_filename}_{mobile_no}"
            else:
                new_filename = f"{new_filename}_{mobile_no}"
            output_json_path = makeOutputPath(json_path, input_dir, output_dir, new_filename, '.json')        
            output_mp4_path = makeOutputPath(mp4_path, input_dir, output_dir, new_filename, '.mp4')
            
            copy_dict[new_filename].append([json_path, output_json_path, mp4_path, output_mp4_path])
            
            # shutil.copy2(json_path, output_json_path)
            # shutil.copy2(mp4_path, output_mp4_path)
    
    df = pd.DataFrame(error_list, columns=['filename'])
    df.to_excel(f'./error_list.xlsx', index=False)
    
    for filename, copy_list in tqdm(copy_dict.items()):
        if len(copy_list) > 1:
            num = 1
            for copy_path in copy_list:
                new_filename = f"{filename}_{num}"
                new_copy_path = [change_filename(new_filename, path) for path in copy_path]
                shutil.copy2(copy_path[0], new_copy_path[1])
                print(copy_path[0], new_copy_path[1])
                shutil.copy2(copy_path[2], new_copy_path[3])
                num += 1
        else:
            shutil.copy2(copy_list[0][0], copy_list[0][1])
            
            shutil.copy2(copy_list[0][2], copy_list[0][3])

        