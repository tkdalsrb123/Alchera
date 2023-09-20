import os, sys, json

def readfiles(dir, Ext):
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == Ext:
                file_path = os.path.join(root, file)

                file_list.append(file_path)
    return file_list

json_format = {
  "objects": [
    {
      "id": "",
      "classId": "",
      "name": "",
      "type": "",
      "valid": True,
      "color": "",
      "zOrder": 0,
      "options": [],
      "childrens": [],
      "points": [
        [
          0,
          0
        ],
        [
          1080,
          1920
        ]
      ],
      "attributes": []
    }
  ],
  "info": {
    "imageName": "",
    "width": None,
    "height": None,
    "labeler": "",
    "examinator": "",
    "timestamp": 0,
    "format": "jpg",
    "fileSize": 0,
    "dirPath": "",
    "projectName": "",
    "taskName": ""
  }
}

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    file = file.replace('.jpg', '.json')
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

_, input_dir, output_dir = sys.argv

jpg_list = readfiles(input_dir, '.jpg')

for jpg_path in jpg_list:
    output_json_path = makeOutputPath(jpg_path, input_dir, output_dir)
    print(output_json_path, '저장!')
    with open(output_json_path, 'w', encoding='utf-8') as o:
        json.dump(json_format, o, ensure_ascii=False, indent=2)