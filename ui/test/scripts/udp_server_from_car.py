import cv2
import socket
import pickle
import numpy as np

import rospy
from std_msgs.msg import String
from chassis_msgs.msg import Chassis

max_length = 65000
host = '10.10.0.79'
port = 5000

def sockrecv(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host,port))

    print("connection")

    while True:
        data, address = sock.recvfrom(max_length)
        d = pickle.loads(data)

        if d:
            x = d["data"]
            print("data: ",x)

if __name__ == '__main__':
    try:
        sockrecv(host,port)
    except Exception as e:
        print(e)
        pass
