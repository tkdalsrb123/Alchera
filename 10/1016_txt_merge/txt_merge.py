import os, sys, logging
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
                folder = os.path.split(root)[-1]
                file_path = os.path.join(root, file)

                file_dict[folder].append(file_path)
    return file_dict

def extract_filename(path):
    file = os.path.split(path)[-1]
    filename = os.path.splitext(file)[0]
    
    return filename

if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv

    logger = make_logger('log.log')

    txt_dict = readfiles(input_dir, '.txt')

    for folder, txt_path_list in tqdm(txt_dict.items()):
        txt_path_list = sorted(txt_path_list, key=lambda x: int(extract_filename(x)))
        merge_file = extract_filename(txt_path_list[0]) + '~' + extract_filename(txt_path_list[-1]) + '.txt'
        merge_path = os.path.join(output_dir, merge_file)
        with open(merge_path, 'w') as outfile:
            for txt_path in txt_path_list:
                logger.info(txt_path)
                with open(txt_path, encoding='utf-8') as f:
                    for line in f:
                        outfile.write(line)
                    outfile.write('\n')
