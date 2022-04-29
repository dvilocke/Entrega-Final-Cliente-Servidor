from functions import *
import sys
import zmq


class Server:

    CONTEXT = zmq.Context()
    LIMIT_ALGORITHM = 64

    def __init__(self, server_id : str, url : str , cmd : str, home_url: str = None):

        #Atributos de clase

        self.server_id = server_id
        self.url = url
        self.cmd = cmd

        #Atributos para las  peticiones

        self.socket_response = self.CONTEXT.socket(zmq.REP)
        self.socket_request = self.CONTEXT.socket(zmq.REQ)

        #Atributos para el anillo

        self.successor = None
        self.server_range = None
        self.modified_range  = None

    def start(self):
        self.socket_response.bind(get_ports(self.url)[0])
        while True:
            print_ranges(self.server_id, self.server_range, self.modified_range)
            message = self.socket_response.recv_multipart()


    def turn_on(self):
        if self.cmd == '--first':
            # significa que es el primer servidor
            self.server_range, self.modified_range = assign_range(self.server_id, self.LIMIT_ALGORITHM)
            self.start()
        else:
            # signfica que ya existe un servidor primero
            pass

if __name__ == '__main__':
    server_id = sys.argv[1]
    url = sys.argv[2]
    cmd = sys.argv[3]
    Server(server_id, url, cmd).turn_on()