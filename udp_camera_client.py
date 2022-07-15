import cv2
import socket
import math
import pickle
import sys

import time
from datetime import datetime
import base64
import numpy as np

max_length = 65000
host = '10.10.0.10'
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
ret, frame = cap.read()
while ret:
    retval, buffer = cv2.imencode(".jpg", frame)
    if retval:
        buffer = buffer.tobytes()
        buffer_size = len(buffer)

        num_of_packs = 1
        if buffer_size > max_length:
            num_of_packs = math.ceil(buffer_size/max_length)+2

        stime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

        frame_info = {"packs":num_of_packs, "stime":stime}
        sock.sendto(pickle.dumps(frame_info), (host, port))

        left = 0
        right = max_length
        for i in range(num_of_packs):
            d = np.array(buffer)
            stringData = base64.b64encode(d)
            data = stringData[left:right]
            left = right
            right += max_length
            # send the frames accordingly
            sock.sendto(data, (host, port))
    
    ret, frame = cap.read()

print("done")
