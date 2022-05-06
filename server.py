import os
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
        while True:
            os.system('cls')
            print_ranges(self.server_id, self.successor, self.server_range, self.modified_range, get_ports(self.url)[0])
            message = self.socket_response.recv_multipart()
            if message[0].decode() == 'i_am_responsible':
                if review_responsibility(int(message[1].decode()), self.modified_range):
                    #Es es responsable de guardar ese nodo, debo guardarlo
                    self.socket_response.send_multipart(
                        [pickle.dumps(
                            {
                                'server_id': self.server_id,
                                'modified_range': self.modified_range,
                                'successor': self.successor,
                                'response': f'Es Responsable De Almacenar El Id:{int(message[1].decode())}',
                                'my_connection' : get_ports(self.url)[1],
                                'state': True
                            }
                        )]
                    )
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
            elif message[0].decode() == 'query_id':
                self.successor = message[1].decode()
                self.socket_response.send_multipart(
                    [self.server_id.encode()]
                )
            elif message[0].decode() == 'change_my_ranges':
                information_new_node = pickle.loads(message[1])
                self.reset_variables()
                self.server_range, self.modified_range = adjust_ranges(f"({information_new_node['id_node']}, {self.server_id}]", self.LIMIT_ALGORITHM)

                self.socket_response.send_multipart(
                    ['ok'.encode()]
                )


    def reset_variables(self):
        self.server_range = ''
        self.modified_range = ''

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
                predecessor = connection
                while True:
                    self.socket_request.connect(connection)
                    #Despues debo pregunta si es responsable de guardarme
                    self.socket_request.send_multipart(
                        ['i_am_responsible'.encode(), self.server_id.encode()]
                    )
                    message = pickle.loads(self.socket_request.recv_multipart()[0])
                    #debo desconectarme de la conexion actual
                    self.socket_request.disconnect(connection)
                    if not message['state']:
                        report_response(message)
                        predecessor = connection
                        connection = message['successor']
                        time.sleep(4)
                        continue
                    else:
                        #Es porque ya encontro un Nodo al cual conectarse
                        report_response(message)
                        break
                #Proceso de traer el predecesor y que apunte al nuevo nodo
                self.socket_request.connect(predecessor)
                self.socket_request.send_multipart(
                    ['query_id'.encode(), get_ports(self.url)[1].encode()]
                )
                id_predecessor = self.socket_request.recv_multipart()[0].decode()
                self.socket_request.disconnect(predecessor)

                time.sleep(4)
                report_conection(self.server_id, message['server_id'], id_predecessor)
                time.sleep(4)
                #Proceso de los rangos
                self.server_range, self.modified_range = adjust_ranges(f"({id_predecessor}, {self.server_id}]", self.LIMIT_ALGORITHM)
                self.successor = message['my_connection']


                #Despues de procesar los cambios, debo cambiar los rango del nodo que me respondio que si
                self.socket_request.connect(message['my_connection'])
                self.socket_request.send_multipart(
                    ['change_my_ranges'.encode(), pickle.dumps(
                        {
                            'id_node' : self.server_id
                        }
                    )]
                )
                response = self.socket_request.recv_multipart()[0].decode()
                self.socket_request.disconnect(message['my_connection'])

                print('------ Lanzando el nuevo servidor :D -------')
                time.sleep(10)

                if response == 'ok':
                    self.start()

if __name__ == '__main__':
    server_id = sys.argv[1]
    url = sys.argv[2]
    cmd = sys.argv[3]
    Server(server_id, url, cmd, '8888').turn_on()