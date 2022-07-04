#!/usr/bin/python
from __future__ import print_function

#TODO: set rate properly

#import roslib
#roslib.load_manifest('vdcl_gui')
import sys
import rospy
import cv2
import os
from std_msgs.msg import String, Bool
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import threading
import numpy as np
from math import *
import copy
import rospkg
import pygame
import time

from vdcl_gui.msg import gui_msg

from vehicle_filter_msgs.msg import Msg_host_vehicle_filter
from chassis_msgs.msg import Chassis
from decision_msgs.msg import route_manager_result, v2x_processed
from acu_new_ioniqw_msgs.msg import acu_new_ioniqw, acu_new_ioniqw_TX
from inertial_labs_msgs.msg import ilgps_RTtype
from decision_msgs.msg import vehicle_motion_planner_result, decision_maker_result

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
#vdcl_mainWnd, QtBaseClass = uic.loadUiType("ros_low_ctrl.ui")

gui_msg_global = gui_msg()
gui_msg_global.map_number = 8
gui_msg_global.gps_heading_offset = 0.0

class ros_qt_interface(QObject):

    webcam_image_updated = pyqtSignal(np.ndarray)
    avm_image_updated = pyqtSignal(np.ndarray)
    vehicle_filter_updated = pyqtSignal(Msg_host_vehicle_filter)
    chassis_updated = pyqtSignal(Chassis)
    can1_fail = pyqtSignal(Bool)
    can2_fail = pyqtSignal(Bool)
    can3_fail = pyqtSignal(Bool)
    can4_fail = pyqtSignal(Bool)
    ibeo_fail = pyqtSignal(Bool)
    velo_fail = pyqtSignal(Bool)
    map_fail = pyqtSignal(Bool)
    webcam_image_updated = pyqtSignal(np.ndarray)
    route_updated = pyqtSignal(route_manager_result)
    v2x_updated = pyqtSignal(v2x_processed)
    acu_updated = pyqtSignal(acu_new_ioniqw)
    acuTX_updated = pyqtSignal(acu_new_ioniqw_TX)
    decision_msg_updated = pyqtSignal(decision_maker_result)
    motion_msg_updated = pyqtSignal(vehicle_motion_planner_result)
    GPS_updated = pyqtSignal(ilgps_RTtype)

    gui_msg = gui_msg_global

    def __init__(self):
        QObject.__init__(self)
        # self.image_pub = rospy.Publisher("/opencv",Image,queue_size=1)

        self.bridge = CvBridge()
        #self.webcam_image_sub = rospy.Subscriber("/webcam/image_raw",Image,self.webcam_callback)
        #self.avm_image_sub = rospy.Subscriber("/avm/image_raw",Image,self.avm_callback)
        self.vehicle_filter_sub = rospy.Subscriber("/host_vehicle_filter_msg",Msg_host_vehicle_filter, self.vehicle_filter_callback)
        self.chassis_sub = rospy.Subscriber("/chassis",Chassis, self.chassis_callback)


        self.can1_sub = rospy.Subscriber("/can1_status",Bool,self.can1_callback)
        self.can2_sub = rospy.Subscriber("/can2_status",Bool,self.can2_callback)
        self.can3_sub = rospy.Subscriber("/can1_status",Bool,self.can3_callback)
        self.can4_sub = rospy.Subscriber("/can2_status",Bool,self.can4_callback)
        self.map_sub = rospy.Subscriber("/route_status",Bool,self.map_callback)
        self.ibeo_status_sub = rospy.Subscriber("/ibeo_status",Bool,self.ibeo_callback)
        self.velo_status_sub = rospy.Subscriber("/velodyne_status",Bool,self.velo_callback)
        self.webcam_image_sub = rospy.Subscriber("/front_camera/image_raw/raw",Image,self.webcam_callback)
        self.route_sub = rospy.Subscriber("/route_manager_result",route_manager_result,self.route_callback)
        self.v2x_sub = rospy.Subscriber("/v2x_processed",v2x_processed,self.v2x_callback)
        self.acu_sub = rospy.Subscriber("/acu_new_ioniqw",acu_new_ioniqw,self.acu_callback)
        self.acuTX_sub = rospy.Subscriber("/acu_new_ioniqw_TX",acu_new_ioniqw_TX,self.acuTX_callback)
        self.decision_msg_sub = rospy.Subscriber("/decision_maker_result",decision_maker_result,self.decision_msg_callback)
        self.motion_msg_sub = rospy.Subscriber("/vehicle_motion_planner_result",vehicle_motion_planner_result,self.motion_msg_callback)
        self.GPS_sub = rospy.Subscriber("/ilgps_utm",ilgps_RTtype,self.GPS_callback)


    def can1_callback(self,data):
        self.can1_fail.emit(data)
    def can2_callback(self,data):
        self.can2_fail.emit(data)
    def can3_callback(self,data):
        self.can3_fail.emit(data)
    def can4_callback(self,data):
        self.can4_fail.emit(data)
    def ibeo_callback(self,data):
        self.ibeo_fail.emit(data)
    def velo_callback(self,data):
        self.velo_fail.emit(data)
    def map_callback(self,data):
        self.map_fail.emit(data)

    def chassis_callback(self,data):
        self.chassis_updated.emit(data)

    def vehicle_filter_callback(self,data):
        self.vehicle_filter_updated.emit(data)

    def webcam_callback(self,data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        try:
            cv_image_rgb = cv2.cvtColor(cv_image,cv2.COLOR_BGR2RGB)
            cv_resized = cv2.resize(cv_image_rgb, dsize=(320, 180), interpolation=cv2.INTER_AREA)
            self.webcam_image_updated.emit(cv_resized)
        except CvBridgeError as e:
            print(e)

    def route_callback(self,data):
        self.route_updated.emit(data)
    def v2x_callback(self,data):
        self.v2x_updated.emit(data)
    def acu_callback(self,data):
        self.acu_updated.emit(data)
    def acuTX_callback(self,data):
        self.acuTX_updated.emit(data)
    def decision_msg_callback(self,data):
        self.decision_msg_updated.emit(data)
    def motion_msg_callback(self,data):
        self.motion_msg_updated.emit(data)
    def GPS_callback(self,data):
        self.GPS_updated.emit(data)
#class MyApp(QtGui.QMainWindow,vdcl_mainWnd):
class MyApp(QtWidgets.QDialog, QtWidgets.QMainWindow):
    
    
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        QtWidgets.QDialog.__init__(self, parent)

        self.ui = uic.loadUi("vdcl_gui.ui")
        self.ui.show()
        self.rqi = ros_qt_interface()

        self.rqi.can1_fail.connect(self.on_can1_fail)
        self.rqi.can2_fail.connect(self.on_can2_fail)
        self.rqi.can3_fail.connect(self.on_can3_fail)
        self.rqi.can4_fail.connect(self.on_can4_fail)
        self.rqi.ibeo_fail.connect(self.on_ibeo_fail)
        self.rqi.velo_fail.connect(self.on_velo_fail)
        self.rqi.map_fail.connect(self.on_map_fail)

        self.rqi.chassis_updated.connect(self.on_chassis_updated)
        self.rqi.vehicle_filter_updated.connect(self.on_vehicle_filter_updated)
        self.rqi.webcam_image_updated.connect(self.on_webcam_image_updated)
        self.rqi.route_updated.connect(self.on_route_updated)
        self.rqi.v2x_updated.connect(self.on_v2x_updated)
        self.rqi.acu_updated.connect(self.on_acu_updated)
        self.rqi.acuTX_updated.connect(self.on_acuTX_updated)
        self.rqi.decision_msg_updated.connect(self.on_decision_msg_updated)
        self.rqi.motion_msg_updated.connect(self.on_motion_msg_updated)
        self.rqi.GPS_updated.connect(self.on_GPS_updated)


        #--- connect pushbutton and method
        self.ui.pushButton_Initialize.clicked.connect(self.on_button_Initialize_clicked)
        self.ui.pushButton_Automation.clicked.connect(self.on_button_Automation_clicked)
        self.ui.pushButton_SCC.clicked.connect(self.on_button_SCC_clicked)
        self.ui.pushButton_LKAS.clicked.connect(self.on_button_LKAS_clicked)
        self.ui.pushButton_EStop.clicked.connect(self.on_button_EStop_clicked)
        self.ui.pushButton_quit.clicked.connect(self.ui.close)

        self.ui.pushButton_vx_change.clicked.connect(self.on_vx_change)
        self.ui.gui_vx_des.textChanged.connect(self.on_gui_vx_des)
        self.ui.gui_map_number.valueChanged.connect(self.on_map_num_change)
        self.ui.gui_gps_heading_offset.valueChanged.connect(self.on_gps_heading_offset_change)

        self.sas_angle = 0.0
        self.swa_cmd_max_diff =0.0
        self.swa_cmd_pre =0.0

    def play_fail_sound(self):
        pygame.init()
        pygame.mixer.music.load("fail.wav")
        pygame.mixer.music.play()

    def play_fail2_sound(self):
        pygame.init()
        pygame.mixer.music.load("fail2.wav")
        pygame.mixer.music.play()

    def on_button_clicked_change(self, Qbutton):
        curr_text = Qbutton.text()
        if (curr_text == "OFF"):
            Qbutton.setText("ON")
            Qbutton.setStyleSheet("background-color: rgb(0,255,0) ; color: red")
        else:
            Qbutton.setText("OFF")
            Qbutton.setStyleSheet("color: grey")
    
    def on_button_Initialize_clicked(self):
        self.on_button_clicked_change(self.ui.pushButton_Initialize)        
        if (self.ui.pushButton_Initialize.text() == "ON") :
            self.rqi.gui_msg.initflag = True
            self.swa_cmd_max_diff =0.0
        elif (self.ui.pushButton_Initialize.text() == "OFF"):
            self.rqi.gui_msg.initflag = False

    def on_button_Automation_clicked(self):
        self.on_button_clicked_change(self.ui.pushButton_Automation)        
        if (self.ui.pushButton_Automation.text() == "ON"):
            self.rqi.gui_msg.Automation_on = True
        elif (self.ui.pushButton_Automation.text() == "OFF"):
            self.rqi.gui_msg.Automation_on = False

    def on_button_SCC_clicked(self):
        self.on_button_clicked_change(self.ui.pushButton_SCC)        
        if (self.ui.pushButton_SCC.text() == "ON"):
            self.rqi.gui_msg.SCC_switch = True
        elif (self.ui.pushButton_SCC.text() == "OFF"):
            self.rqi.gui_msg.SCC_switch = False

    def on_button_LKAS_clicked(self):
        self.on_button_clicked_change(self.ui.pushButton_LKAS)        
        if (self.ui.pushButton_LKAS.text() == "ON"):
            self.rqi.gui_msg.LKAS_switch = True
        elif (self.ui.pushButton_LKAS.text() == "OFF"):
            self.rqi.gui_msg.LKAS_switch = False

    def on_button_EStop_clicked(self):
        self.on_button_clicked_change(self.ui.pushButton_EStop)        
        if (self.ui.pushButton_EStop.text() == "ON"):
            self.rqi.gui_msg.Stop_signal = True
        elif (self.ui.pushButton_EStop.text() == "OFF"):
            self.rqi.gui_msg.Stop_signal = False


    def on_gui_vx_des(self):
        print(self.ui.gui_vx_des.text())

    def on_vx_change(self):
        if(0<=int(self.ui.gui_vx_des.text()) and int(self.ui.gui_vx_des.text())<=50):
            self.rqi.gui_msg.vx_des = int(self.ui.gui_vx_des.text())
            print("vx_des change: ",self.rqi.gui_msg.vx_des )

    def on_map_num_change(self):
        self.rqi.gui_msg.map_number = int(self.ui.gui_map_number.value())
        print("map change: ", self.rqi.gui_msg.map_number)

    def on_gps_heading_offset_change(self):
        self.rqi.gui_msg.gps_heading_offset = self.ui.gui_gps_heading_offset.value()
        print("offset change: ", self.rqi.gui_msg.gps_heading_offset)

    @pyqtSlot(Msg_host_vehicle_filter)
    def on_vehicle_filter_updated(self,vehicle_filter_data):
        self.ui.lcdNumber_ax_curr.display(vehicle_filter_data.long_accel)
        self.ui.lcdNumber_vx_curr.display(vehicle_filter_data.v_x*3.6)

    @pyqtSlot(np.ndarray)
    def on_webcam_image_updated(self,cv_img):
        height,width,bpc = cv_img.shape
        bpl = width*bpc
        qt_img = QtGui.QImage(cv_img.data,width,height,bpl,\
                              QtGui.QImage.Format_RGB888)
        qt_pixmap = QtGui.QPixmap.fromImage(qt_img)
        self.ui.mainCameraView.setPixmap(qt_pixmap)

    @pyqtSlot(route_manager_result)
    def on_route_updated(self,route):
        self.ui.lcdNumber_vx_des.display(route.vx_des*3.6)
        self.ui.lcdNumber_nearmap_idx.display(route.near_map_ind)
        self.ui.lcdNumber_closest_idx.display(route.closest_ind)
        if (route.map_main_ind == 0):
            self.ui.led_main.setStyleSheet("background-color: green")
        else:
            self.ui.led_main.setStyleSheet("background-color: gray")
        self.ui.LC_left_progress.setValue(route.lc_avail[0])
        self.ui.LC_right_progress.setValue(route.lc_avail[1])

    @pyqtSlot(v2x_processed)
    def on_v2x_updated(self,v2x):
        if (v2x.event_state[0] == 5):
            self.ui.led_v2x_1.setStyleSheet("background-color: green;\nborder-radius: 25px;")
        elif (v2x.event_state[0] == 3):
            self.ui.led_v2x_1.setStyleSheet("background-color: red;\nborder-radius: 25px;")
        elif (v2x.event_state[0] == 7):
            self.ui.led_v2x_1.setStyleSheet("background-color: yellow;\nborder-radius: 25px;")
        else:
            self.ui.led_v2x_1.setStyleSheet("background-color: gray;\nborder-radius: 25px;")
        if (v2x.event_state[1] == 5):
            self.ui.led_v2x_2.setStyleSheet("background-color: green;\nborder-radius: 25px;")
        elif (v2x.event_state[1] == 3):
            self.ui.led_v2x_2.setStyleSheet("background-color: red;\nborder-radius: 25px;")
        elif (v2x.event_state[1] == 7):
            self.ui.led_v2x_2.setStyleSheet("background-color: yellow;\nborder-radius: 25px;")
        else:
            self.ui.led_v2x_2.setStyleSheet("background-color: gray;\nborder-radius: 25px;")
        if (v2x.event_state[2] == 5):
            self.ui.led_v2x_3.setStyleSheet("background-color: green;\nborder-radius: 25px;")
        elif (v2x.event_state[2] == 3):
            self.ui.led_v2x_3.setStyleSheet("background-color: red;\nborder-radius: 25px;")
        elif (v2x.event_state[2] == 7):
            self.ui.led_v2x_3.setStyleSheet("background-color: yellow;\nborder-radius: 25px;")
        else:
            self.ui.led_v2x_3.setStyleSheet("background-color: gray;\nborder-radius: 25px;")

    @pyqtSlot(acu_new_ioniqw)
    def on_acu_updated(self,acu):
        if (acu.MDPS_Module_Stat or acu.ACC_Module_Stat):
            self.ui.led_AD_status.setStyleSheet("background-color: green")
        else:
            self.ui.led_AD_status.setStyleSheet("background-color: gray")
        if (acu.MDPS_Module_Stat):
            self.ui.led_MDPS_status.setStyleSheet("background-color: green")
        else:
            self.ui.led_MDPS_status.setStyleSheet("background-color: gray")
        if (acu.ACC_Module_Stat):
            self.ui.led_ACC_status.setStyleSheet("background-color: green")
        else:
            self.ui.led_ACC_status.setStyleSheet("background-color: gray")

    @pyqtSlot(acu_new_ioniqw_TX)
    def on_acuTX_updated(self,acuTX):
        self.ui.lcdNumber_ax_des.display(acuTX.Ax_cmd)
        self.ui.lcdNumber_des_sas_angle.display(acuTX.SWA_cmd)
        self.ui.lcdNumber_sas_angle_error.display(acuTX.SWA_cmd - self.sas_angle)

        if (abs(acuTX.SWA_cmd - self.swa_cmd_pre) > abs(self.swa_cmd_max_diff)):
            self.swa_cmd_max_diff = acuTX.SWA_cmd - self.swa_cmd_pre
            self.ui.lcdNumber_swa_cmd_max_diff.display(self.swa_cmd_max_diff)
        self.swa_cmd_pre = acuTX.SWA_cmd

    @pyqtSlot(decision_maker_result)
    def on_decision_msg_updated(self,decision_msg):
        if (decision_msg.lc_demand==1):
            self.ui.LC_left_demand.setValue(1)
        elif (decision_msg.lc_demand==-1):
            self.ui.LC_right_demand.setValue(1)
        else:
            self.ui.LC_left_demand.setValue(0)
            self.ui.LC_right_demand.setValue(0)
#        if(decision_msg.lc_risk[0]==1 or decision_msg.lc_risk[1]==1):
#            self.ui.led_lcmode.setStyleSheet("background-color: red")
#        else:
        if (decision_msg.lc_execution):
            self.ui.led_lcmode.setStyleSheet("background-color: green")
        else:
            self.ui.led_lcmode.setStyleSheet("background-color: gray")

    @pyqtSlot(vehicle_motion_planner_result)
    def on_motion_msg_updated(self,motion_msg):
        self.ui.gui_vx_final.display(motion_msg.vx_des[0]*3.6)
        self.ui.gui_s_final.display(motion_msg.s_des[0])


    @pyqtSlot(ilgps_RTtype)
    def on_GPS_updated(self,GPS):
        self.ui.lcdNumber_pos_x.display(GPS.X_RT)
        self.ui.lcdNumber_pos_y.display(GPS.Y_RT)
        self.ui.lcdNumber_yaw_angle.display(GPS.H_RT)

    @pyqtSlot(Bool)
    def on_can1_fail(self,status):
        if status.data:
            self.ui.led_can1_status.setStyleSheet("background-color: green")
        else:
            self.ui.led_can1_status.setStyleSheet("background-color: red")
            self.play_fail_sound()

    @pyqtSlot(Bool)
    def on_can2_fail(self,status):
        if status.data:
            self.ui.led_can2_status.setStyleSheet("background-color: green")
        else:
            self.ui.led_can2_status.setStyleSheet("background-color: red")
            self.play_fail_sound()

    @pyqtSlot(Bool)
    def on_can3_fail(self,status):
        if status.data:
            self.ui.led_can3_status.setStyleSheet("background-color: green")
        else:
            self.ui.led_can3_status.setStyleSheet("background-color: red")
            self.play_fail_sound()

    @pyqtSlot(Bool)
    def on_can4_fail(self,status):
        if status.data:
            self.ui.led_can4_status.setStyleSheet("background-color: green")
        else:
            self.ui.led_can4_status.setStyleSheet("background-color: red")
            self.play_fail_sound()

    @pyqtSlot(Bool)
    def on_ibeo_fail(self,status):
        if status.data:
            self.ui.led_lidar1_status.setStyleSheet("background-color: green")
        else:
            self.ui.led_lidar1_status.setStyleSheet("background-color: red")
            self.play_fail_sound()

    @pyqtSlot(Bool)
    def on_velo_fail(self,status):
        if status.data:
            self.ui.led_lidar2_status.setStyleSheet("background-color: green")
        else:
            self.ui.led_lidar2_status.setStyleSheet("background-color: red")
            self.play_fail_sound()

    @pyqtSlot(Bool)
    def on_map_fail(self,status):
        if status.data:
            self.ui.led_map_status.setStyleSheet("background-color: green")
        else:
            self.ui.led_map_status.setStyleSheet("background-color: red")
            self.play_fail_sound()


    @pyqtSlot(Chassis)
    def on_chassis_updated(self,chassis_data):
        self.ui.lcdNumber_sas_angle.display(chassis_data.sas_angle)
        self.ui.lcdNumber_sas_torque.display(chassis_data.cr_mdps_strtq)
        self.sas_angle = chassis_data.sas_angle

def gui_thread_func():
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

def gui_thread_func_mod():
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    rospy.init_node('vdcl_gui_new_ioniqw', anonymous=False)
    rospy.loginfo("Thanks to arojo...")

    gui_thread = threading.Thread(target=gui_thread_func_mod)
    gui_thread.start()
#
    pub = rospy.Publisher("gui_msg", gui_msg, queue_size=1)

    rate = rospy.Rate(10) #10hz
    while (not rospy.is_shutdown()) and gui_thread.isAlive():
        pub.publish(gui_msg_global)
        rate.sleep()
    rospy.spin()
