"""
Just used to test our server.
http://ilab.cs.byu.edu/python/socket/echoclient.html
"""

import socket
import numpy as np

HOST = '192.168.2.12'
PORT = 8889
SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
readings = s.recv(SIZE)
s.close()
readings = readings.split(',')
print(np.array([readings]))
