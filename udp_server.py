import cv2
import socket
import pickle
import numpy as np

# host = '10.30.18.10'
host = '10.10.0.79'
port = 5000
max_length = 65540

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

    while True:
        axis0, address = sock.recvfrom(max_length)
        data0 = axis0.decode()
        # print(type(float(data0)))
        print("Axis 0 value: ", data0)
        axis1, address = sock.recvfrom(max_length)
        data1 = axis1.decode()
        print("Axis 1 value: ", data1)
        axis2, address = sock.recvfrom(max_length)
        data2 = axis2.decode()
        print("Axis 2 value: ", data2)
        axis3, address = sock.recvfrom(max_length)
        data3 = axis3.decode()
        print("Axis 3 value: ", data3)

if __name__ == '__main__':
    # sockrecv(host,port)
    sockrecv2(host,port)
    # sockrecv3(host,port)