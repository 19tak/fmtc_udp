import socket
import pickle
import numpy as np

import rospy
from std_msgs.msg import String

max_length = 65000
host = '10.30.18.13'
port = 5050

def sockrecv(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host,port))

    print("connect success")

    while True:
        data, address = sock.recvfrom(max_length)
        d = pickle.loads(data)

        if d:
            x = d["data"]
            print("data : ",x)

if __name__ == '__main__':
    try:
        sockrecv(host,port)
    except Exception as e:
        print(e)
        pass