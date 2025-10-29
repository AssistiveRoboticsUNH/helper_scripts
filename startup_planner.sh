#!/bin/bash

######################
# STRETCH BASHRC SETUP
#
# Fill Up the token and ids where MISSING is indicated
#
######################

export HELLO_FLEET_PATH=/home/hello-robot/stretch_user &&
export HELLO_FLEET_ID=MISSING &&
export PATH=${PATH}:~/.local/bin &&
export LRS_LOG_LEVEL=None &&
export PYTHONWARNINGS='ignore:setup.py install is deprecated,ignore:Invalid dash-separated options,ignore:pkg_resources is deprecated as an API,ignore:Usage of dash-separated' &&
export _colcon_cd_root=/home/hello-robot/ament_ws &&
source /opt/ros/humble/setup.bash &&

export CAMERA1_dock='MISSING' &&
export ROS_MASTER_URI=http://192.168.1.32:11311 &&
export ROS_DOMAIN_ID=25 &&
export plug_ip="192.168.50.4" &&


export TWILIO_TOKEN=MISSING &&
export TWILIO_ACCOUNT_SID=MISSING &&

export SMARTTHINGS_TOKEN=MISSING &&
export APIKEY=MISSING &&

export cmd_vel="stretch/cmd_vel" &&

export robot_pass="MISSING" &&
export ROBOT_NAME="MISSING" &&
export DISCORD_TOKEN="MISSING" &&
export DISCORD_LOGGING_CHANNEL=MISSING &&
export DISCORD_EMERGENCY_CHANNEL=1415364437782560871 &&


source /opt/ros/humble/setup.bash &&
source /home/hello-robot/smarthome_ws/install/setup.bash &&
source /home/hello-robot/ament_ws/install/setup.bash &&
source /usr/share/colcon_cd/function/colcon_cd.sh &&

echo "Checking wifi ..."
# Warn if connected to 2.4 GHz instead of 5 GHz

# Network interface (change if needed)
IFACE="wlo1"

# Get frequency from iwconfig
FREQ=$(iwconfig $IFACE 2>/dev/null | grep -o "Frequency:[0-9.]*" | cut -d: -f2)

if [[ -z "$FREQ" ]]; then
  echo "  Interface $IFACE not connected or Wi-Fi unavailable."
  exit 1
fi

# Convert frequency to numeric (GHz)
FREQ_NUM=$(echo "$FREQ" | awk '{print $1}')

if (( $(echo "$FREQ_NUM < 3.0" | bc -l) )); then
  echo " WARNING: Connected to 2.4 GHz Wi-Fi ($FREQ_NUM GHz) — expect latency spikes!"
  echo " Tip: Switch to 5 GHz SSID (e.g., r1_5G)."
else
  echo " Connected to 5 GHz Wi-Fi ($FREQ_NUM GHz) — all good."
fi

echo "Setting external speaker "
bash /home/hello-robot/smarthome_ws/src/smart-home-robot/external/helper_scripts/select_external_audio.sh

echo "Starting processes..."
python3 /home/hello-robot/smarthome_ws/src/smart-home-robot/external/helper_script/handshake.py
sleep 1s
python3 /home/hello-robot/smarthome_ws/src/smart-home-robot/external/helper_script/reposition_display.py
sleep 1s

echo "Launching Realsense"
ros2 launch realsense2_camera rs_launch.py > /tmp/realsense.txt 2>&1 &
sleep 20s

echo "Launching Real Robot"
ros2 launch shr_plan real_robot.launch.py > /tmp/real_robot.txt 2>&1 &

sleep 20s

# ros2 run tf2_ros static_transform_publisher 0.5680000185966492 1.8179999589920044 -1.1649999618530273 0.0 0.0 0.7071067811865475 0.7071067811865476 map base_link &

ros2 run shr_plan planning_controller_node > /tmp/planning_controller_node_.txt &


wait

