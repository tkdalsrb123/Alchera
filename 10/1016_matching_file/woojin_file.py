import os, sys, logging
import shutil
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

def read_depth(dir):
    file_dict = defaultdict(list)
    for root, dirs, files in os.walk(dir):
        if len(files) > 0:
            file_list = []
            for f in files:
                ext = os.path.splitext(f)[-1]
                if ext == '.jpg' or ext == '.data':
                    file_list.append(f)
                else:
                   pass
                
            sorted_file_list = sorted(file_list, key=lambda x: int(x.split('_')[0]))
            sorted_file_list = [os.path.join(root, file) for file in sorted_file_list]
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.jpg':
                    file_dict[filename] = sorted_file_list
    return file_dict

def extract_filename(file_path):
    file = os.path.split(file_path)[-1]
    filename, ext = os.path.splitext(file)
    
    return filename

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

if __name__ == '__main__':
    _, depth_input_dir, img_input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    
    jpg_dict = readfiles(img_input_dir, '.jpg')
    depth_dict = read_depth(depth_input_dir)
    
    for filename, jpg_path in jpg_dict.items():
        logger.info(jpg_path)
        # output_jpg_file = os.path.join(output_dir, f"{filename}.jpg")
        # shutil.copy2(jpg_path, output_jpg_file)
        # logger.info(output_jpg_file)
        depth_list = depth_dict.get(filename)
        if depth_list:
            for idx, file in enumerate(depth_list):
                f_name = extract_filename(file)
                if filename == f_name:
                    copyjpgpath = makeOutputPath(file, output_dir, 'jpg')
                    shutil.copy2(file, copyjpgpath)
                    logger.info(copyjpgpath)

                    if idx + 1 < len(depth_list):
                        if os.path.splitext(depth_list[idx+1])[-1] == '.data':
                            depth_file_path = depth_list[idx+1]
                            root, depthname = os.path.split(depth_file_path)
                            copydepthpath = makeOutputPath(depth_file_path, output_dir, 'data')
                            shutil.copy2(depth_file_path, copydepthpath)
                            logger.info(copydepthpath)


