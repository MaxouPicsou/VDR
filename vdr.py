# https://www.sciencedirect.com/science/article/pii/S1742287613000510
# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjViPqBjrDxAhUGjhQKHe0SCN0QFjAAegQIAxAD&url=https%3A%2F%2Fwww.iacs.org.uk%2Fdownload%2F1871&usg=AOvVaw2AFrLs9fUAaCMTTwdPvqJq
import errno
import os
import socket
from pathlib import Path
import configparser
import tools


class Vdr:

    config = configparser.ConfigParser()
    config.read('config.ini')

    def __init__(self, path="."):
        self.path = path + "/data"
        self.filename = "000000"
        self.connections = {}

        # Create tree structure of VDR if it is not already exists
        if not os.path.exists(path + "/data"):
            os.makedirs(path + "/data")
        if not os.path.exists(path + "/data/frame"):
            os.makedirs(path + "/data/frame")
        if not os.path.exists(path + "/data/nmea"):
            os.makedirs(path + "/data/nmea")
        if not os.path.exists(path + "/data/voice"):
            os.makedirs(path + "/data/voice")

    def add_connection(self, ip, port, key):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((ip, port))
        self.connections[key] = sock

    def receiving_frame(self, key):
        while True:
            data = self.connections[key].recvfrom(1024)
            if data[0] == b'start':
                f = open(self.path + "/frame/" + self.filename + ".bmp", 'wb')
                data = self.connections[key].recvfrom(8192)
                while data:
                    if data[0] == b'stop':
                        f.close()
                        break
                    else:
                        f.write(data[0])
                        data = self.connections[key].recvfrom(8192)

    def receiving_nmea(self, key):
        data = self.connections[key].recvfrom(1024)
        print(key, ":", data)
        path = self.path + "/nmea/" + self.filename
        file = open(path, "a")
        file_size = Path(path).stat().st_size
        if file_size > int(self.config['nmea']['size']):
            self.filename = tools.update(self.filename)
            file.close()
            file = open(path, "a")

        split_data = bytes.decode(data[0]).split(',')

        try:
            if split_data[1] == "safety_management_system":
                tools.safety(split_data, file)
        except IndexError:
            print(errno)

    def start_record(self):
        for i in self.connections:
            self.receiving(i)


VDR = Vdr()
VDR.add_connection("localhost", 12345, "test")
VDR.add_connection("localhost", 12346, "test2")

while True:
    VDR.receiving_frame("test")


