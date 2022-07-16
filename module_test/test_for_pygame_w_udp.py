import cv2
import socket
import math
import pickle
import sys

import random

max_length = 65000
host = '10.30.18.18'
# host = '10.10.0.55'
# host = '10.10.0.79'
port = 5050

def sockmsg(host,port):
    a = [True, False]
    b = [True,True]
    # b = [False,False]
    # b = [True, False]

    # while True:
    # v = random.randint(-30,30)
    # s = random.randint(-350,350)
    v,s = 20, 4
    v,s = float(v), float(s)
    random.shuffle(a)
    # mdps, accs = a[0], a[1]
    mdps, accs = b[0], b[1]
    d = {"Vx":v,"sas_angle":s,"MDPS_Module_Stat":mdps,"ACC_Module_Stat":accs}
    print(v,s,mdps,accs)
    sock.sendto(pickle.dumps(d),(host,port))


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def sockmsg2(host,port):
    pygame.init()
    done = False
    clock = pygame.time.Clock()
    pygame.joystick.init()

    while not done:
        for event in pygame.event.get(): # User did something.
            if event.type == pygame.QUIT: # If user clicked close.
                done = True # Flag that we are done so we exit this loop.
            elif event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
            elif event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            axes = joystick.get_numaxes()
            print("Number of axes: {}".format(axes))
            tmp = []
            for i in range(axes):
                axis = joystick.get_axis(i)*100
                a = str(axis)
                tmp.append(a)
                # sock.sendto(a.encode(),(host,port))
                # print(sys.getsizeof(a.encode()))
                # if i == 0:print("Axis {} value: {:>6.3f}".format(i, axis))
                print("Axis {} value: {:>6.3f}".format(i, axis))
            axis_info = {"axis0":tmp[0],"axis1":tmp[1],"axis2":tmp[2],"axis3":tmp[3]}
            sock.sendto(pickle.dumps(axis_info),(host,port))
            # print(sys.getsizeof(pickle.dumps(axis_info),(host,port)))
        clock.tick(20)
    pygame.quit()


if __name__ == '__main__':
    sockmsg(host,port)
    # sockmsg2(host,port)