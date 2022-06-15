import threading
import json


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.clientAddress = clientAddress
        print("New connection added: ", clientAddress)

    def run(self):
        print("Connection from : ", self.clientAddress)

        self.csocket.send(bytes("Hi, This is from Server..", 'utf-8'))
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg == 'bye':
                break
            if msg == 'json':
                self.process_json()
            if msg == 'file':
                self.save_file()
            print("from client", msg)
            self.csocket.send(bytes(msg, 'UTF-8'))
        print("Client at ", self.clientAddress, " disconnected...")

    def save_file(self):
        # Get data about the file
        self.csocket.send(bytes("file_info", "UTF-8"))
        print("Waiting for file information....")
        data = self.process_json(self.csocket.recv(1024).decode("UTF-8"))
        file_name = data[0]
        self.csocket.send(bytes("file", "UTF-8"))
        f = open(f"./{file_name}", "wb")
        data = None
        while True:
            m = self.csocket.recv(1024)
            data = m
            if m:
                while m:
                    m = self.csocket.recv(1024)
                    data += m
            else:
                break
        f.write(data)
        f.close()
        print("Done receiving")

    def process_json(self, data):
        try:
            data = data.decode('UTF-8')
            print(data, "first case")
            json_data = json.loads(data)
            print("Data after")
            return json_data
        except Exception as e:
            return ["hello.php"]
            # self.csocket.send(bytes(f"500{e}", "UTF-8"))
