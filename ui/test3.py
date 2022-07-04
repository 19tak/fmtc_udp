import base64
import cv2
import socket
import pickle
import numpy as np

import time
from datetime import datetime

import threading
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

host = '10.30.18.13'
port = 5000
max_length = 65540

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

running = False

def test():
    global running
    # cap = cv2.VideoCapture(0)
    # width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    label.resize(1280, 720)
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

                    # stime, address = sock.recvfrom(26)

                    frame = np.frombuffer(base64.b64decode(buffer), np.uint8)
                    frame = frame.reshape(frame.shape[0], 1)
                    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                    # try:
                    #     stime2 = stime.decode('utf-8')
                    #     stimet = datetime.strptime(stime2,'%Y-%m-%d %H:%M:%S.%f')
                    #     dtime =  datetime.utcnow() - stimet
                    #     text = 'time difference : ' + str(dtime)
                    #     org = (50,100)
                    #     font = cv2.FONT_HERSHEY_SIMPLEX
                    #     cv2.putText(frame,text,org,font,1,(0,0,0),2)
                    # except Exception as e:
                    #     print(e)
                    #     pass
                    
                    if frame is not None and type(frame) == np.ndarray:
                        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        h, w, c = img.shape
                        qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
                        pixmap = QtGui.QPixmap.fromImage(qImg)
                        label.setPixmap(pixmap)
                        # cv2.imshow("Stream", frame)
                        # if cv2.waitKey(1) == 27:
                        #     break

        except Exception as e:
            QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
            print("cannot read frame.")
            print(e)
            # break
            pass

    # print("Thread end.")


def run(): 
    global running
    cap = cv2.VideoCapture(0)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    label.resize(width, height)
    while running: 
        ret, img = cap.read()
        if ret : 
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, c = img.shape
            qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            label.setPixmap(pixmap)
        else : 
            QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
            print("cannot read frame.")
            break 
    cap.release()
    print("Thread end.")

def stop() : 
    global running 
    running = False 
    print("stoped..")
    
def start() : 
    global running 
    running = True 
    th = threading.Thread(target = test)
    th.start()
    print("started..")
    
def onExit() : 
    print("exit")
    stop()

app = QtWidgets.QApplication([])
win = QtWidgets.QWidget()
vbox = QtWidgets.QVBoxLayout()
label = QtWidgets.QLabel()
btn_start = QtWidgets.QPushButton("Camera On")
btn_stop = QtWidgets.QPushButton("Camera Off")
vbox.addWidget(label)
vbox.addWidget(btn_start)
vbox.addWidget(btn_stop)
win.setLayout(vbox)
win.show()
btn_start.clicked.connect(start)
btn_stop.clicked.connect(stop)
app.aboutToQuit.connect(onExit)
sys.exit(app.exec_())