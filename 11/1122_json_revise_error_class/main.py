import subprocess, sys

if __name__ == "__main__":
    _, in_id_json_path, no_id_json_path, in_id_output_path, no_id_output_path = sys.argv
    
    subprocess.run(['python', 'revise_error_class.py', in_id_json_path, in_id_output_path])
    subprocess.run(['python', 'matching_coor.py', in_id_output_path, no_id_json_path, no_id_output_path])
    