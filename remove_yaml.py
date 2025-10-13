import os
import shutil

def replace_yaml_file(target_yaml_path, default_yaml_path):
    # Check if the target YAML file exists and remove it
    if os.path.exists(target_yaml_path):
        print(f"Removing YAML file: {target_yaml_path}")
        os.remove(target_yaml_path)
    else:
        print(f"No YAML file found at: {target_yaml_path}")

    # Copy the default YAML to the target path
    shutil.copy(default_yaml_path, target_yaml_path)
    print(f"Replaced with default YAML file from: {default_yaml_path}")

# Example usage
replace_yaml_file('/home/hello-robot/smarthome_ws/src/smart-home-robot/shr_parameters/params/shr_parameters.yaml', '/home/hello-robot/smarthome_ws/src/smart-home-robot/shr_parameters/params/shr_parameters_default.yaml')
