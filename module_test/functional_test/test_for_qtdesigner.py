import base64
import cv2
import socket
import pickle
import numpy as np

import time
from datetime import datetime

import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import threading

import pygame
import time

# monitor 3440 * 1440

# host = '10.30.18.65'
# port = 5000
# max_length = 65540

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((host, port))

# form_class = uic.loadUiType("test.ui")[0]

# class MyWindow(QMainWindow, form_class):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     mywindow = MyWindow()
#     mywindow.show()
#     app.exec_()

class MyApp(QtWidgets.QDialog, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        QtWidgets.QDialog.__init__(self,parent)

        self.ui = uic.loadUi("test.ui")
        self.ui.show()

    def play_fail_sound(self):
        pygame.init()
        pygame.mixer.music.load("fail.wav")
        pygame.mixer.music.play()

    def play_fail2_sound(self):
        pygame.init()
        pygame.mixer.music.load("fail2.wav")
        pygame.mixer.music.play()

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
    gui_thread = threading.Thread(target=gui_thread_func_mod)
    gui_thread.start()
    print("started..")