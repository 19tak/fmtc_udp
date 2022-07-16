import base64
import cv2
import socket
import pickle
import numpy as np

import math

import time
from datetime import datetime

import sys
import cv2

from PyQt5 import QtWidgets, uic, QtCore, QtGui

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5 import uic

from PyQt5.QtCore import pyqtSignal, pyqtSlot

import threading

import pygame
import time

# pygame.init()
# done = False
# clock = pygame.time.Clock()
# pygame.joystick.init()

# monitor 3440 * 1440

host = '10.10.0.10'
# host = '10.30.18.27'
port1 = 5000
max_length = 65540
port2 = 5050
port3 = 6000

'''
port1 for camera udp server
port2 for info data from car udp server
port3 for pyjoy data from udp server
'''

sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock1.bind((host, port1))
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.bind((host, port2))
sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock3.bind((host, port3))

# it's for camera image sent by udp -> pyqt
running = False
# from here, it's for pyqt
form_class = uic.loadUiType("ui_3440_720.ui")[0]
class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_cam_on.clicked.connect(self.start)
        self.pushButton_joy_on.clicked.connect(self.start2)
        # self.pushButton_cam_off.clicked.connect(self.stop)
        # self.pushButton_quit.clicked.connect(self.stop)
        self.pushButton_quit.clicked.connect(self.onExit)
        self.qlogo = QPixmap()
        self.qlogo.load("logo_fmtc.png")
        self.qlogo = self.qlogo.scaledToWidth(440)
        self.label_logo.setPixmap(self.qlogo)

    def loadImagetest(self,*argv):
        global running
        self.cam_label.resize(2560, 1440)
        while running:
            try:
                data1, address = sock1.recvfrom(max_length)
                if len(data1) < 150:
                    frame_info = pickle.loads(data1)
                    if frame_info:
                        stime = frame_info["stime"]
                        stimet = datetime.strptime(stime,'%Y-%m-%d %H:%M:%S.%f')
                        ntime = datetime.utcnow()
                        dtime = str(abs(stimet - ntime))
                        self.label_latency.setText(dtime)
                        nums_of_packs = frame_info["packs"]
                        for i in range(nums_of_packs):
                            data2, address = sock1.recvfrom(max_length)
                            if i == 0:
                                buffer = data2
                            else:
                                buffer += data2

                        frame = np.frombuffer(base64.b64decode(buffer), np.uint8)
                        frame = frame.reshape(frame.shape[0], 1)
                        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                        if frame is not None and type(frame) == np.ndarray:
                            resize_frame = cv2.resize(frame, dsize=(2560, 1440), interpolation=cv2.INTER_AREA)
                            img = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2RGB)
                            h, w, c = img.shape
                            qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
                            pixmap = QtGui.QPixmap.fromImage(qImg)
                            self.cam_label.setPixmap(pixmap)
                            self.led_cam_on.setStyleSheet("background-color: green")
                            self.led_cam_off.setStyleSheet("background-color: gray")                            
            except Exception as e:
                print(e)
                self.label_err.setText(str(e))
                self.led_cam_on.setStyleSheet("background-color: red")
                self.led_cam_off.setStyleSheet("background-color: red")                
                pass

    def stop(self,*argv):
        global running
        running = False
        self.led_cam_on.setStyleSheet("background-color: gray")
        self.led_cam_off.setStyleSheet("background-color: green")      
        self.led_ACC_status.setStyleSheet("background-color: gray")  
        self.led_MDPS_status.setStyleSheet("background-color: gray")
        self.pushButton_cam_on.setStyleSheet("background-color: gray")
        # self.pushButton_joy_on.setStyleSheet("background-color: gray")
        # print("stopped..")

    def start(self,*argv):
        global running
        running = True
        th = threading.Thread(target = self.loadImagetest)
        th.start()
        th2 = threading.Thread(target = self.car_listener)
        th2.start()
        self.pushButton_cam_on.setStyleSheet("background-color: green")
        # print("started..")
        
    def start2(self,*argv):
        th3 = threading.Thread(target = self.sockjoy)
        th3.start()
        self.pushButton_joy_on.setStyleSheet("background-color: green")

    def onExit(self,*argv):
        # print("exit")
        self.stop()

    def car_listener(self,*argv):
        while True:
            data3, address = sock2.recvfrom(max_length)
            d = pickle.loads(data3)
            if d:
                try:
                    vx = d["Vx"]
                    sas_angle = d["sas_angle"]
                    MDPS_Module_Stat = d["MDPS_Module_Stat"]
                    ACC_Module_Stat = d["ACC_Module_Stat"]
                    self.lcdNumber_vx.display(vx)
                    self.lcdNumber_sas_angle.display(sas_angle)
                    if (MDPS_Module_Stat):
                        self.led_MDPS_status.setStyleSheet("background-color: green")
                    else:
                        self.led_MDPS_status.setStyleSheet("background-color: gray")
                    if (ACC_Module_Stat):
                        self.led_ACC_status.setStyleSheet("background-color: green")
                    else:
                        self.led_ACC_status.setStyleSheet("background-color: gray")
                except Exception as e:
                    print(e)
                    self.label_err.setText(str(e))
                    self.lcdNumber_vx.display("ERR")
                    self.lcdNumber_sas_angle.display("ERR")
                    self.led_MDPS_status.setStyleSheet("background-color: red")
                    self.led_ACC_status.setStyleSheet("background-color: red")
                    pass

    def sockjoy(self,*argv):
        while True:
            data4, address = sock3.recvfrom(max_length)
            axis_info = pickle.loads(data4)
            if axis_info:
                try:
                    axis0 = axis_info["axis0"]
                    axis2 = axis_info["axis2"]
                    axis3 = axis_info["axis3"]
                    axis0,axis2,axis3 = int(float(axis0)), int(float(axis2)), int(float(axis3))
                    self.lcdNumber_acc.display(axis2)
                    self.lcdNumber_brk.display(axis3)
                    self.lcdNumber_str.display(axis0)
                except Exception as e:
                    print(e)
                    self.lcdNumber_acc.display("ERR")
                    self.lcdNumber_brk.display("ERR")
                    self.lcdNumber_str.display("ERR")
                    pass
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()