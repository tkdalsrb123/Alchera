import os, sys, shutil, logging
from tqdm import tqdm
from collections import defaultdict


def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}{ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path  

def copy_file(light_dict, folder):
    for light, file_path_list in light_dict.items():
        for file_path in file_path_list:
            root, file = os.path.split(file_path)
            user = os.path.split(root)[-1]
            root = os.path.join(output_dir, folder, user, light)
            os.makedirs(root, exist_ok=True)

            output_file_path = os.path.join(root, file)

            shutil.move(file_path , output_file_path)

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
  
if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    
    file_dict = defaultdict(lambda : defaultdict(list))    
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            
            file_path = os.path.join(root, file)
            if len(filename.split('_')) > 1:
                device = filename.split('_')[1]
                light = filename.split('_')[2]
            
                file_dict[device][light].append(file_path)
    
    for device, light_dict in tqdm(file_dict.items(), desc="copy file"):
        if device in ["E1S", "E2Q"]:
            folder = 'Alchera_DB_1'
            copy_file(light_dict, folder)
        elif device in ["13PROMAX", "12PRO"]:
            folder = 'Alchera_DB_1_PA1'
            copy_file(light_dict, folder)
        else:
            for light, file_path_list in light_dict.items():
                for file_path in file_path_list:
                    output_file_path = makeOutputPath(file_path, input_dir, output_dir)
                    shutil.move(file_path , output_file_path)