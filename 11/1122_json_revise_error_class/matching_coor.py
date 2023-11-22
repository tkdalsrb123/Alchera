import os, sys
from tqdm import tqdm
from collections import defaultdict
from revise_error_class import make_logger, makeOutputPath, readJson, saveJson

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


if __name__ == '__main__':
    _, revise_json_dir, new_json_dir, output_dir = sys.argv
    
    logger = make_logger('no_id_log.log')
    revise_dict = readfiles(revise_json_dir, '.json')
    new_json_dict = readfiles(new_json_dir, '.json')

    for filename, new_json_path in tqdm(new_json_dict.items(), desc='revise no id json..!'):
        logger.info(new_json_path)
        revise_path = revise_dict.get(filename)
        if revise_path:
            output_json_path = makeOutputPath(new_json_path, new_json_dir, output_dir, 'json')

            new_data = readJson(new_json_path)
            revise_data = readJson(revise_path)
            
            objects = revise_data['objects']
            if type(objects) == dict:
                objects = [objects]
            
            for obj in objects:
                _class = obj['class']
                _sub_class1 = obj['sub_class1']
                _sub_class2 = obj['sub_class2']
                xmin = obj['xmin']
                xmax = obj['xmax']
                ymin = obj['ymin']
                ymax = obj['ymax']

                for idx, new_obj in enumerate(new_data['objects']):
                    if new_obj['xmin'] == xmin and new_obj['xmax'] == xmax and new_obj['ymin'] == ymin and new_obj['ymax'] == ymax:
                        new_data['objects'][idx]['class'] = _class
                        new_data['objects'][idx]['sub_class1'] = _sub_class1
                        new_data['objects'][idx]['sub_class2'] = _sub_class2
                        
            saveJson(new_data, output_json_path)
