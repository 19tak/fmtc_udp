import cv2
import socket
import pickle
import numpy as np

import rospy
from geometry_msgs.msg import Point

host = '10.30.18.22'
# host = '10.10.0.55'
# host = '10.10.0.79'
port = 5000
max_length = 65540
length = 50

def sockrecv(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    # print("-> waiting for connection")

    while True:
        axis0, address = sock.recvfrom(length)
        data0 = float(axis0.decode())
        # print(type(float(data0)))
        print("Axis 0 value: ", data0)
        axis1, address = sock.recvfrom(length)
        data1 = float(axis1.decode())
        # don't use this axes
        # print("Axis 1 value: ", data1)
        axis2, address = sock.recvfrom(length)
        data2 = float(axis2.decode())
        # print("Axis 2 value: ", data2)
        axis3, address = sock.recvfrom(length)
        data3 = float(axis3.decode())
        # print("Axis 3 value: ", data3)
        return data0, data2, data3

def talker(host,port):
    pub = rospy.Publisher('UDP_input',Point,queue_size=10)
    rospy.init_node('udp_talker',anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        vals = Point()
        vals.x, vals.y, vals.z = sockrecv(host,port)
        pub.publish(vals)
        rate.sleep()

if __name__ == '__main__':
    # sockrecv(host,port)
    # sockrecv2(host,port)
    try:
        # sockrecv(host,port)
        talker(host,port)
    except rospy.ROSInterruptException:
        pass