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

# from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import threading

import pygame
import time

# pygame.init()
# done = False
# clock = pygame.time.Clock()
# pygame.joystick.init()

# monitor 3440 * 1440

# host = '10.10.0.10'
host = '10.30.18.18'
port1 = 5000
max_length = 65540
port2 = 5050
port3 = 6000
# host2 = '10.30.18.65'

sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock1.bind((host, port1))
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.bind((host, port2))
sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock3.bind((host, port3))

# it's for camera image sent by udp -> pyqt
running = False
# from here, it's for pyqt
form_class = uic.loadUiType("test_2.ui")[0]
class MyWindow(QMainWindow, form_class):
# class MyWindow(QMainWindow, QtWidgets.QDialog):
    def __init__(self):
        # self.QMainWindow.__init__(self)
        # self.QtWidgets.QDialog.__init__(self,parent)
        # self.ui = uic.loadUi("test_2.ui")
        # self.ui.show()

        super().__init__()
        # self.ui = uic.loadUiType("test_2.ui")[0]
        # self.ui.show()
        self.setupUi(self)
        self.pushButton_cam_on.clicked.connect(self.start)
        self.useron.clicked.connect(self.start2)
        self.pushButton_cam_off.clicked.connect(self.stop)
        self.pushButton_quit.clicked.connect(self.onExit)
        self.qlogo = QPixmap()
        self.qlogo.load("logo_fmtc.png")
        self.qlogo = self.qlogo.scaledToWidth(320)
        self.label_logo.setPixmap(self.qlogo)
        # self.lcdNumber_vx = 
        # self.lcdNumber_sas_angle = 


    def loadImagetest(self,*argv):
        # print("btn_cam_on clicked")
        global running
        self.cam_label.resize(1280, 720)
        while running:
            try:
                data1, address = sock1.recvfrom(max_length)
                if len(data1) < 50:
                    frame_info = pickle.loads(data1)
                    if frame_info:
                        # num = frame_info["num"]
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
                            resize_frame = cv2.resize(frame, dsize=(1280, 720), interpolation=cv2.INTER_AREA)
                            img = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2RGB)
                            # img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            h, w, c = img.shape
                            qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
                            pixmap = QtGui.QPixmap.fromImage(qImg)
                            self.cam_label.setPixmap(pixmap)
                            self.pushButton_cam_on.setStyleSheet("background-color: green")
                            self.pushButton_cam_off.setStyleSheet("background-color: gray")                            
            except Exception as e:
                # QtWidgets.QMessageBox.about("Error", "Cannot read frame.")
                # print("cannot read frame.")
                print(e)
                self.pushButton_cam_on.setStyleSheet("background-color: red")
                self.pushButton_cam_off.setStyleSheet("background-color: red")                
                # break
                pass
        # print("test")

    def stop(self,*argv):
        global running
        running = False
        self.pushButton_cam_on.setStyleSheet("background-color: gray")
        self.pushButton_cam_off.setStyleSheet("background-color: green")      
        self.led_ACC_status.setStyleSheet("background-color: gray")  
        self.led_MDPS_status.setStyleSheet("background-color: gray")
        print("stopped..")

    def start(self,*argv):
        global running
        running = True
        th = threading.Thread(target = self.loadImagetest)
        th.start()
        th2 = threading.Thread(target = self.car_listener)
        th2.start()
        print("started..")
        # th3 = threading.Thread(target = self.sockjoy(host,port3))
        # th3.start()
        
    def start2(self,*argv):
        th3 = threading.Thread(target = self.sockjoy)
        th3.start()

    def onExit(self,*argv):
        print("exit")
        self.stop()

    # def play_fail_sound(self):
    #     pygame.init()
    #     pygame.mixer.music.load("fail.wav")
    #     pygame.mixer.music.play()

    # def play_fail2_sound(self):
    #     pygame.init()
    #     pygame.mixer.music.load("fail2.wav")
    #     pygame.mixer.music.play()

    # def test(self,*argv):
    #     while True:
    #         data, address = sock2.recvfrom(max_length)
    #         d = pickle.loads(data)
    #         if d:
    #             x = d["data"]
    #             print("data : ",x)
    #             self.lcdNumber_test.display(x)

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
                    # print("Vx: ",vx)
                    # print("sas_angle: ",sas_angle)
                    # print("MDPS_Module_Stat: ",MDPS_Module_Stat)
                    # print("ACC_Module_Stat: ",ACC_Module_Stat)
                    # self.lcdNumber_vx.display("vx")
                    # self.lcdNumber_sas_angle.display("sas_angle")
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
                    # print("Vx err")
                    # print("sas err")
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
                    # print(axis0)
                    # print(axis2)
                    # print(axis3)
                    self.lcdNumber_acc.display(axis0)
                    self.lcdNumber_brk.display(axis3)
                    self.lcdNumber_str.display(axis2)
                    # self.lcdNumber_acc.setDigitCount(2)
                    # self.lcdNumber_brk.setDigitCount(2)
                    # self.lcdNumber_str.setDigitCount(2)
                except Exception as e:
                    print(e)
                    self.lcdNumber_acc.display("ERR")
                    self.lcdNumber_brk.display("ERR")
                    self.lcdNumber_str.display("ERR")
                    pass
    #     # pygame.init()
    #     # done = False
    #     # clock = pygame.time.Clock()
    #     # pygame.joystick.init()
    #     global done

    #     while not done:
    #         for event in pygame.event.get(): # User did something.
    #             if event.type == pygame.QUIT: # If user clicked close.
    #                 done = True # Flag that we are done so we exit this loop.
    #             elif event.type == pygame.JOYBUTTONDOWN:
    #                 print("Joystick button pressed.")
    #             elif event.type == pygame.JOYBUTTONUP:
    #                 print("Joystick button released.")
    #         joystick_count = pygame.joystick.get_count()
    #         for i in range(joystick_count):
    #             joystick = pygame.joystick.Joystick(i)
    #             joystick.init()
    #             axes = joystick.get_numaxes()
    #             print("Number of axes: {}".format(axes))
    #             tmp = []
    #             for i in range(axes):
    #                 axis = joystick.get_axis(i)*100
    #                 a = str(axis)
    #                 tmp.append(a)
    #                 print("Axis {} value: {:>6.3f}".format(i, axis))
    #             axis_info = {"axis0":tmp[0],"axis1":tmp[1],"axis2":tmp[2],"axis3":tmp[3]}
    #             sock3.sendto(pickle.dumps(axis_info),(host2,port1))
    #         clock.tick(20)
    #     pygame.quit()
        
# # from here, it's for joy_client        
# sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# def sockjoy(host,port):
#     pygame.init()
#     done = False
#     clock = pygame.time.Clock()
#     pygame.joystick.init()

#     while not done:
#         for event in pygame.event.get(): # User did something.
#             if event.type == pygame.QUIT: # If user clicked close.
#                 done = True # Flag that we are done so we exit this loop.
#             elif event.type == pygame.JOYBUTTONDOWN:
#                 print("Joystick button pressed.")
#             elif event.type == pygame.JOYBUTTONUP:
#                 print("Joystick button released.")
#         joystick_count = pygame.joystick.get_count()
#         for i in range(joystick_count):
#             joystick = pygame.joystick.Joystick(i)
#             joystick.init()
#             axes = joystick.get_numaxes()
#             print("Number of axes: {}".format(axes))
#             for i in range(axes):
#                 axis = joystick.get_axis(i)*100
#                 a = str(axis)
#                 sock3.sendto(a.encode(),(host,port))
#                 # print(sys.getsizeof(a.encode()))
#                 if i == 0:print("Axis {} value: {:>6.3f}".format(i, axis))
#                 # print("Axis {} value: {:>6.3f}".format(i, axis))
#         clock.tick(20)
#     pygame.quit()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
    # sockjoy(host2,port1)