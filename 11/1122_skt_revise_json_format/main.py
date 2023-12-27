import os, sys, json, logging
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

def json_format(filename, contents, output_path):
    tree = [{"filename":filename,
            "contents":contents}]
    
    saveJson(tree, output_path)
    
def revise(text):

    while True:
        
        if text[0] != " " and text[0] != "\n":
            break
        
        else:
            text = text[1:]
            
    while True:
        
        if text[-1] != " " and text[-1] != "\n":
            break
        
        else:
            text = text[:-1]
    
    i=0
    while i < len(text)-1:
        
        if text[i] == " ":
        
            if text[i+1] in ["®", "\n", "ml", "kcal", "g", "mL",  "mg", "㎍", "%", "㎖", '.']:
                
                text = text[:i] + text[i+1:]
                
                i -= 1
        
            if text[i-1] == '.':
                
                text = text[:i] + text[i+1:]
                
                i -= 1
            
            if text[i-1].isdigit() and text[i+1] == '정':

                text = text[:i] + text[i+1:]
                
                i -= 1
                
        if text[i] == 'x' or text[i] == 'X':
            if text[i+1] == " " and text[i-1] == " ":
                
                text = text[:i-1] + text[i] + text[i+2]
                
                i -= 1
            
        if text[i] in [":", "(", "["]:
            if text[i-1] != " " and text[i-1] != "\"":
                
                text = text[:i] + " " + text[i:]
                
                i += 1
        
        if text[i] == ":":
            if text[i+1] != " ":
                
                text = text[:i] + " " + text[i:]
                
                i += 1
        
        i += 1
    return text

if __name__ == "__main__":
    _, input_dir ,output_dir = sys.argv
    
    logger = make_logger('log.log')

    json_dict = readfiles(input_dir, '.json')
    
    for filename, json_path in tqdm(json_dict.items()):
        # filename = f"{filename}.jpg"
        output_json_path = makeOutputPath(json_path, input_dir, output_dir, 'json')    
        logger.info(json_path)
        data = readJson(json_path)
        
        imagename = data['info']['imageName']
        obj = data['objects']
        if type(obj) == dict:
            obj = [obj]

        content_list = []
        for o in obj:
            value = o['attributes'][0]['values'][0]['value']
            value = revise(value)

            content_list.append(value)
        
        json_format(imagename, content_list, output_json_path)