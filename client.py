import os
import pickle
import hashlib
import time
import  json
import zmq


class Client:

    CONTEXT = zmq.Context()
    SIZE = 50 # son 65 Kilobyte

    def __init__(self, file_name : str, server_to_connect : str):

        #Atributos De Clase
        self.file_name = file_name
        self.servet_to_connect = server_to_connect

        #Atributos para las peticiones
        self.socket_request = self.CONTEXT.socket(zmq.REQ)

    def partition(self):
        part_numbers = 0
        with open(self.file_name, 'rb') as f:
            content = f.read(self.SIZE)
            if content:
                while content:
                    part_numbers += 1
                    content = f.read(self.SIZE)
        return part_numbers

    def get_ports(self):
        return f"tcp://*:{self.servet_to_connect}", f"tcp://localhost:{self.servet_to_connect}"

    def server_response(self, response, counter):
        msg = f"""
                    --- Respuesta Del Servidor ----
        El servidor {response['server_id']} respondio
        Su rango es: {response['modified_range']}
        Su sucesor es: {response['successor']}
        Es responsable de almacenar la parte {counter} : {'Si' if response['state'] else 'No'}
        """
        print(msg)
        time.sleep(4)

    def additional_information(self, count, extension, sha1, number):
        msg = f"""
                    --- Información Adicional ---
        Guardando la parte:{count}
        Su extension es:{extension}
        Su sha1 asignado es: {sha1}
        Su int(sha1, 16) es: {number}"""
        print(msg)
        time.sleep(4)

    def get_the_extension(self):
        start_index = self.file_name.index('.')
        extension = ''
        while start_index != len(self.file_name):
            extension += self.file_name[start_index]
            start_index += 1

        return extension

    def generate_json(self, counter, sha1, number, bd_server):
        base = {
            'parte': counter,
            'sha1': sha1,
            'rango': number,
            'servidor': bd_server
        }
        with open('information.json', 'r+') as  f:
            content = json.loads(f.read())
            content.append(base)
            f.seek(0)
            f.write(json.dumps(content))

    def send_to_servers(self):
        if os.path.exists(self.file_name):
            conection = self.get_ports()[1]
            counter = 1
            keep_reading = False
            file_extension = self.get_the_extension()
            with open(self.file_name, 'rb') as f:
                data = f.read(self.SIZE)
                while counter <= self.partition():
                    self.socket_request.connect(conection)

                    if keep_reading:
                        data = f.read(self.SIZE)

                    keep_reading = False
                    sha1 = hashlib.sha1()
                    sha1.update(data)
                    self.socket_request.send_multipart(
                        ['i_am_responsible'.encode(), str(int(sha1.hexdigest(), 16)).encode()]
                    )
                    #--- respuesta del servidor ---#
                    response = pickle.loads(self.socket_request.recv_multipart()[0])
                    self.server_response(response, counter)
                    # --- logica importante --- #
                    if response['state']:
                        # es responsable de almacenar esa parte
                        self.additional_information(counter, file_extension, sha1.hexdigest(), int(sha1.hexdigest(), 16))
                        self.socket_request.send_multipart(
                            ['save'.encode(), pickle.dumps(
                                {
                                    'extension' : file_extension,
                                    'sha1': sha1.hexdigest(),
                                    'content' : data
                                }
                            )]
                        )
                        bd_server = self.socket_request.recv_multipart()[0].decode()
                        self.generate_json(counter, sha1.hexdigest(), int(sha1.hexdigest(), 16), bd_server)
                        time.sleep(4)
                        keep_reading = True
                        counter += 1
                        self.socket_request.disconnect(conection)
                        continue

                    self.socket_request.disconnect(conection)
                    conection = response['successor']


if __name__ == '__main__':
    Client('prueba.txt', '6666').send_to_servers()