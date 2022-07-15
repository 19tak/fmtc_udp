import base64
import cv2
import socket
import pickle
import numpy as np

import time
from datetime import datetime

import sys
import cv2

import threading

import pygame
import time

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

def sockjoy():
    while True:
        data4, address = sock3.recvfrom(200)
        # print(data4)
        axis_info = pickle.loads(data4)
        # print(axis_info)
        if axis_info:
            try:
                axis0 = axis_info["axis0"]
                axis2 = axis_info["axis2"]
                axis3 = axis_info["axis3"]
                print(axis0)
                print(axis2)
                print(axis3)
                # self.lcdNumber_acc.display(axis0)
                # self.lcdNumber_brk.display(axis2)
                # self.lcdNumber_str.display(axis3)
            except Exception as e:
                print(e)
                # self.lcdNumber_acc.display("ERR")
                # self.lcdNumber_brk.display("ERR")
                # self.lcdNumber_str.display("ERR")
                pass

if __name__ == "__main__":
    sockjoy()