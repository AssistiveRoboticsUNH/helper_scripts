import argparse
from ruamel.yaml import YAML
from pathlib import Path

yaml = YAML()
yaml.preserve_quotes = True

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.load(f)

def save_yaml(data, path):
    with open(path, 'w') as f:
        yaml.dump(data, f)

def parse_time(time_str):
    """Parses a time string like '8' or '8:30' into (hour, minute)."""
    parts = time_str.split(':')
    if len(parts) == 1:
        return int(parts[0]), 0
    elif len(parts) == 2:
        return int(parts[0]), int(parts[1])
    else:
        raise ValueError(f"Invalid time format: {time_str}")

def update_protocol_time(config, protocol_type, instance_name, start_str, end_str):
    try:
        start_hour, start_min = parse_time(start_str)
        end_hour, end_min = parse_time(end_str)

        protocol = config["shr_parameters"]["pddl"][protocol_type]
        instances = protocol["instances"]["default_value"]

        if instance_name not in instances:
            raise ValueError(f"Instance '{instance_name}' not found in {protocol_type}.")

        index = instances.index(instance_name)
        time_key = next((k for k in protocol if k.endswith("_times")), None)
        if time_key is None:
            raise KeyError(f"No time-related key found in {protocol_type}.")

        new_time = f"Everyday {start_hour:02d}h{start_min:02d}m0s/{end_hour:02d}h{end_min:02d}m0s"
        protocol[time_key]["default_value"][index] = new_time
        print(f"✅ Updated '{protocol_type}' instance '{instance_name}' to: {new_time}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update protocol time in shr_parameters.yaml")
    parser.add_argument("protocol_type", help="Protocol type (e.g., MedicineProtocols)")
    parser.add_argument("instance_name", help="Instance name (e.g., pm_meds)")
    parser.add_argument("start_time", help="Start time (e.g., 8 or 8:30)")
    parser.add_argument("end_time", help="End time (e.g., 17 or 17:45)")
    parser.add_argument("--file", default="/home/hello-robot/smarthome_ws/src/smart-home-robot/shr_parameters/params/shr_parameters.yaml", help="Path to YAML file")

    args = parser.parse_args()

    config = load_yaml(Path(args.file))
    update_protocol_time(config, args.protocol_type, args.instance_name, args.start_time, args.end_time)
    save_yaml(config, Path(args.file))

## python3 parameters_change.py MedicineProtocols pm_meds 8:30 17
## python3 parameters_change.py OneReminderProtocols trash 6:25 17