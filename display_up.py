#!/usr/bin/env python3
'''
This script is used to move the robot's wrist and lift to a specific pose while strech driver is already running by nav2. 
Running this standalone script will not work as it requires the stretch driver to be running.

If you want to run this script without nav2, make sure to start the stretch driver first using:
ros2 launch stretch_core stretch_driver.launch.py
'''
import hello_helpers.hello_misc as hm
node = hm.HelloNode.quick_create('temp')
node.move_to_pose({'joint_lift': 0.7}, blocking=True)
node.move_to_pose({'joint_wrist_yaw': 1.57, 'joint_wrist_roll': 0.0, 'joint_wrist_pitch': 0.5}, blocking=True)