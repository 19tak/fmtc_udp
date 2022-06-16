import cv2
import socket
import math
import pickle
import sys

import pygame

max_length = 65000
# host = '10.30.18.10'
host = '10.10.0.79'
port = 5000

def sockmsg(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        msg = input("->")
        sock.sendto(msg.encode(), (host,port))

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
            # try:
            #     jid = joystick.get_instance_id()
            # except AttributeError:
            #     jid = joystick.get_id()
            # name = joystick.get_name()
            # try:
            #     guid = joystick.get_guid()
            # except AttributeError:
            #     pass
            # else:
            #     pass
            axes = joystick.get_numaxes()
            print("Number of axes: {}".format(axes))
            for i in range(axes):
                axis = joystick.get_axis(i)*100
                a = str(axis)
                sock.sendto(a.encode(),(host,port))
                print("Axis {} value: {:>6.3f}".format(i, axis))
            # buttons = joystick.get_numbuttons()
            # for i in range(buttons):
            #     button = joystick.get_button(i)
            # hats = joystick.get_numhats()
            # for i in range(hats):
            #     hat = joystick.get_hat(i)
        clock.tick(20)
    pygame.quit()


if __name__ == '__main__':
    # sockmsg(host,port)
    sockmsg2(host,port)