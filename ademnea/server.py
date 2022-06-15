import socket
from . import config
from .threads import ClientThread


class Server():
    def __init__(self) -> None:
        pass

    def serve_forever(self):
        """
        Starts a multithreaded server and waits for any incoming requests.
        It uses the configurations in the config file.
        Once a request is received, a client thread is created and the server resumes with listening for 
        the incoming requests.
        """
        LOCALHOST = config.HOST
        PORT = config.PORT
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((LOCALHOST, PORT))
        print("Server started")
        print("Waiting for client request..")
        while True:
            server.listen(1)
            clientsock, clientAddress = server.accept()
            data = clientsock.recv(2048)
            newthread = ClientThread(clientAddress, clientsock)
            newthread.start()
