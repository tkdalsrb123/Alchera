import json, os, sys

_, input_dir = sys.argv

for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.json':
            json_path = os.path.join(root, file)
            print(json_path)
            with open(json_path, 'r', encoding='utf-8') as f:
                json_file = json.load(f)
            
            for obj in json_file['objects']:
                if obj['type'] == 'BOX':
                    x_diff = abs(obj['points'][0][0] - obj['points'][1][0])
                    y_diff = abs(obj['points'][0][1] - obj['points'][1][1])
                    if x_diff < 5 or y_diff < 5:
                        json_file['objects'].remove(obj)
                    
                        print(obj, '객체 삭제!!')
            
            with open(json_path, 'w', encoding='utf-8') as o:
                json.dump(json_file, o, ensure_ascii=False, indent=2)
                