import base64
import cv2
import socket
import pickle
import numpy as np

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

# from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import threading

import pygame
import time

# monitor 3440 * 1440

host = '10.30.18.13'
port = 5000
max_length = 65540

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

running = False

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
        self.pushButton_cam_off.clicked.connect(self.stop)
        self.pushButton_quit.clicked.connect(self.onExit)

    def loadImagetest(self,*argv):
        # print("btn_cam_on clicked")
        global running
        self.cam_label.resize(1280, 720)
        while running:
            try:
                data, address = sock.recvfrom(max_length)
                if len(data) < 25:
                    frame_info = pickle.loads(data)
                    if frame_info:
                        nums_of_packs = frame_info["packs"]
                        for i in range(nums_of_packs):
                            data, address = sock.recvfrom(max_length)
                            if i == 0:
                                buffer = data
                            else:
                                buffer += data

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
            except Exception as e:
                # QtWidgets.QMessageBox.about("Error", "Cannot read frame.")
                print("cannot read frame.")
                print(e)
                # break
                pass
        # print("test")

    def stop(self,*argv):
        global running
        running = False
        print("stopped..")

    def start(self,*argv):
        global running
        running = True
        th = threading.Thread(target = self.loadImagetest)
        th.start()
        print("started..")

    def onExit(self,*argv):
        print("exit")
        self.stop()

    def play_fail_sound(self):
        pygame.init()
        pygame.mixer.music.load("fail.wav")
        pygame.mixer.music.play()

    def play_fail2_sound(self):
        pygame.init()
        pygame.mixer.music.load("fail2.wav")
        pygame.mixer.music.play()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()