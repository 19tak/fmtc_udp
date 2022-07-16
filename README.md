# FMTC_UDP

This is Project for Using G29 and UDP protocol to controll Ioniq (Electric car of Hyundai)

Some Rights Reserved by FMTC of Seoul National University

---

# Contents

1. Description of Project
2. Procedure of using these codes
3. References

---

# Description of Project



---

# Procedure of using these codes

## On Computer (User) Sides

1. activate `udp_joy_client_pickle.py`
2. activate `udp_ui.py` in **3440 by 720 monitor** or `udp_ui_small.py` in **1920 by 720 monitor**
3. on **QtDesigner UI**, push buttons `TH_JOY` to start thread for joy_udp and `TH_CAM` to start thread for cam_udp
4. If camera states or vehicle information packet has broken, push button `Quit` and re-push `TH_CAM` button.

## On Car (Vehicle) Sides

1. start `roscore`
2. activate all the packages for `ROS-CAN` bridges
3. activate `udp_server_ros_pickle.py`
4. activate `udp_camera_client.py`
5. If you want to give powers to **User Side**, push `Cruise Mode` button on Handle

---

# References