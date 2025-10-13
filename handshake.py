import stretch_body.robot
import time
import os
import subprocess
from datetime import datetime

def log_error(error_message):
    log_dir = "/tmp/stretch_logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(log_dir, f"robot_startup_error_{timestamp}.txt")
    with open(log_path, "w") as f:
        f.write(f"[{timestamp}] Startup Error:\n{error_message}\n")
    print(f"⚠️ Error logged to: {log_path}")

def reboot_robot():
    password = os.getenv("robot_pass")
    if not password:
        print("❌ Environment variable 'robot_pass' is not set!")
        return

    print("🔁 Rebooting the robot system now...")
    try:
        subprocess.run(
            ["sudo", "-S", "reboot"],
            input=(password + "\n").encode(),
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to reboot: {e}")

r = stretch_body.robot.Robot()
did_succeed = False

while not did_succeed:
    try:
        did_succeed = r.startup()
    except Exception as e:
        error_message = str(e)
        print(f"❌ Error during robot startup: {error_message}")
        log_error(error_message)
        reboot_robot()
        break
    finally:
        r.stop()

if did_succeed:
    print("✅ Successfully connected to Stretch!")
