import os, sys, subprocess

if __name__ == '__main__':
    _ = sys.argv
    
    if os.path.exists('./company_names.csv') == False:
        subprocess.run(['python', 'next_unicon.py'])
    
    subprocess.run(['python', 'the_vc.py'])