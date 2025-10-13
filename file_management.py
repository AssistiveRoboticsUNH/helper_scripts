import os
import shutil

def empty_text_file(file_path):
    with open(file_path, 'w'):
        pass
    print(f"Emptied: {file_path}")

def replace_yaml_file(target_yaml, default_yaml):
    if os.path.exists(target_yaml):
        os.remove(target_yaml)
        print(f"Removed: {target_yaml}")
    shutil.copy(default_yaml, target_yaml)
    print(f"Replaced with default: {default_yaml}")

if __name__ == "__main__":
    empty_text_file("/home/hello-robot/smarthome_ws/src/smart-home-robot/shr_plan/include/shr_plan/intersection.txt")
    replace_yaml_file(
        "/home/hello-robot/smarthome_ws/src/smart-home-robot/shr_parameters/params/shr_parameters.yaml",
        "/home/hello-robot/smarthome_ws/src/smart-home-robot/shr_parameters/params/shr_parameters_default.yaml"
    )

