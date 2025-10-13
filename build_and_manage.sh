#!/bin/bash

# Log everything to file
exec > >(tee -a /tmp/build_and_reboot.log) 2>&1
echo "🕒 Starting build at $(date)"

# Check for password env var
if [ -z "$robot_pass" ]; then
  echo "❌ 'robot_pass' environment variable not set!"
  exit 1
fi

source /opt/ros/humble/setup.bash &&
source /home/hello-robot/smarthome_ws/install/setup.bash &&
source /home/hello-robot/ament_ws/install/setup.bash &&
source /usr/share/colcon_cd/function/colcon_cd.sh &&
# Run helper script
python3 /home/hello-robot/smarthome_ws/src/smart-home-robot/external/helper_scripts/file_management.py

# Go to workspace
cd /home/hello-robot/smarthome_ws || { echo "❌ Workspace not found!"; exit 1; }

# Build and reboot
echo "🔧 Running colcon build..."
if colcon build --symlink-install; then
  echo "✅ Build finished successfully."
  echo "🔁 Rebooting in 5 seconds..."
  sleep 5
  echo "$robot_pass" | sudo -S reboot
else
  echo "❌ Build failed. Skipping reboot."
  exit 1
fi
