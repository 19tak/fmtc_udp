import cv2
import socket
import pickle
import numpy as np

# import rospy
# from geometry_msgs.msg import Point

host = '10.30.18.22'
# host = '10.10.0.55'
# host = '10.10.0.79'
port = 5000
max_length = 65540
length = 50

# def sockrecv(host,port):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.bind((host, port))

#     print("-> waiting for connection")

#     while True:
#         recvMsg, address = sock.recvfrom(max_length)
#         data = recvMsg.decode()
#         print(data)

def sockrecv2(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    print("-> waiting for connection")

    # pub = rospy.Publisher('UDP_input',Point,queue_size=10)
    # rospy.init_node('udp_talker',anonymous=True)
    # rate = rospy.Rate(10)

    while True:
        axis0, address = sock.recvfrom(length)
        data0 = float(axis0.decode())
        # print(type(float(data0)))
        print("Axis 0 value: ", data0)
        axis1, address = sock.recvfrom(length)
        data1 = float(axis1.decode())
        # print("Axis 1 value: ", data1)
        axis2, address = sock.recvfrom(length)
        data2 = float(axis2.decode())
        # print("Axis 2 value: ", data2)
        axis3, address = sock.recvfrom(length)
        data3 = float(axis3.decode())
        # print("Axis 3 value: ", data3)

        # vals = Point()
        # # while not rospy.is_shutdown():
        # vals.x = data0
        # # vals.x, vals.y, vals.z = data0, data1, data2
        # pub.publish(vals)
        # rate.sleep()

if __name__ == '__main__':
    # sockrecv(host,port)
    # sockrecv2(host,port)
    try:
        sockrecv2(host,port)
    # except rospy.ROSInterruptException:
    #     pass
    except Exception as e:
        print(e)
        pass