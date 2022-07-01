import cv2
import socket
import pickle
import numpy as np

import rospy
from geometry_msgs.msg import Point

host = '10.30.18.65'
# host = '10.10.0.55'
# host = '10.10.0.79'
port = 5000
max_length = 65540
length = 200

def sockrecv(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    print("-> waiting for connection")

    # pub = rospy.Publisher('UDP_input',Point,queue_size=10)
    # rospy.init_node('udp_talker',anonymous=True)
    # rate = rospy.Rate(10)

    while True:
        data, address = sock.recvfrom(length)
        if len(data) < 200:
            axes_info = pickle.loads(data)

            if axes_info:
                axis0, axis1, axis2, axis3 = axes_info["axis0"], axes_info["axis1"], axes_info["axis2"], axes_info["axis3"]
                print("Axis 0 value: ", axis0)
                print("Axis 1 value: ", axis1)
                # print("Axis 2 value: ", axis2)
                print("Axis 3 value: ", axis3)
                return axis0, axis2, axis3

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