import os, sys
import shutil


_, input_dir = sys.argv

parser = './can_parser.txt'
parser_file = os.path.split(parser)[-1]
for root, dirs, files in os.walk(input_dir):
    if 'ccan_0000.bin' in files and 'ccan_0000.timestamp' in files:
        
        parser_path = os.path.join(root, parser_file)
        shutil.copy2(parser, parser_path)
        os.system(f'{parser} {root} -v')