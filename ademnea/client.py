import os
import socket
from . import config


class Client():
    def connect(self):
        SERVER = config.HOST
        PORT = config.PORT
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))
        self.client.sendall(bytes("This is from Client", 'UTF-8'))

        while True:
            in_data = self.client.recv(1024)
            print("From Server :", in_data.decode())
            out_data = input()
            self.client.sendall(bytes(out_data, 'UTF-8'))
            if out_data == 'bye':
                break
            if out_data == 'file':
                self.send_file(os.path.dirname(os.path.realpath(__file__)) + "./threads.py")
        self.client.close()

    def send_file(self, file_path):
        in_data = self.client.recv(1024)
        print("From Server :", in_data.decode())
        out_data = input()
        self.client.sendall(bytes(out_data, 'UTF-8'))

        f = open(file_path, "rb")
        l = os.path.getsize(file_path)
        m = f.read(l)
        self.client.sendall(m)
        f.close()
        print("Done sending...")
