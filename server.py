"""
The car will callt he server to get readings. So the purpose of this is
to receive a connection and serve readings.

Base script from:
http://ilab.cs.byu.edu/python/socket/echoserver.html
"""

import socket
from sensing import Sensors

host = ''
port = 8888
backlog = 5
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(backlog)

sensors = Sensors()

while 1:
    client, address = s.accept()
    data = str(sensors.get_readings())
    try:
        print("Sending: ")
        print(data)
        client.send(data.encode(encoding='utf_8'))
    except:
        print("Couldn't send data.")
    client.close()

sensors.cleanup_gpio()
