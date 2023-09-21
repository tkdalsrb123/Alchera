import os, sys, shutil


_, input_dir, output_dir = sys.argv

for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.png':
            file_path = os.path.join(root, file)
            output_file_path = os.path.join(output_dir, file)
            print(output_file_path)
            shutil.copy2(file_path, output_file_path)
