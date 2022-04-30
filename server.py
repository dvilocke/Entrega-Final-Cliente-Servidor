
from functions import *
import pickle
import time
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
        self.home_url = home_url

        #Atributos para las  peticiones

        self.socket_response = self.CONTEXT.socket(zmq.REP)
        self.socket_request = self.CONTEXT.socket(zmq.REQ)

        #Atributos para el anillo

        self.successor = None
        self.server_range = None
        self.modified_range  = None

    def start(self):
        self.socket_response.bind(get_ports(self.url)[0])
        print_ranges(self.server_id, self.successor, self.server_range, self.modified_range)
        while True:
            message = self.socket_response.recv_multipart()
            if message[0].decode() == 'i_am_responsible':
                if review_responsibility(int(message[1].decode()), self.modified_range):
                    #Es es responsable de guardar ese nodo, debo guardarlo
                    pass
                else:
                    #No es el responsable de guardar ese nodo, debo enviarle mi sucesor
                    self.socket_response.send_multipart(
                        [pickle.dumps(
                            {
                                'server_id': self.server_id,
                                'modified_range' : self.modified_range,
                                'successor': self.successor,
                                'response' : f'No Es Responsable De Almacenar El Id:{int(message[1].decode())}',
                                'state' : False
                            }
                        ) ]
                    )

    def turn_on(self):
        if self.cmd == '--first':
            # significa que es el primer servidor
            self.server_range, self.modified_range = assign_range(self.server_id, self.LIMIT_ALGORITHM)
            self.successor = get_ports(self.url)[1]
            self.start()

        elif self.cmd == '--conect':
            if self.home_url is not None:
                #Me conecto al servidor que yo dije que quiero entrar a traves de la variable self.home_url
                connection  = get_ports(self.home_url)[1]
                while True:
                    self.socket_request.connect(connection)
                    #Despues debo pregunta si es responsable de guardarme
                    self.socket_request.send_multipart(
                        ['i_am_responsible'.encode(), self.server_id.encode()]
                    )
                    message = pickle.loads(self.socket_request.recv_multipart()[0])
                    if not message['state']:
                        report_response(message)
                        connection = message['successor']
                        time.sleep(4)
                        continue
                    else:
                        #Es porque ya encontro un Nodo al cual conectarse
                        break
                print('funciona')

if __name__ == '__main__':
    server_id = sys.argv[1]
    url = sys.argv[2]
    cmd = sys.argv[3]
    Server(server_id, url, cmd, '5555').turn_on()