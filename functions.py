import hashlib
import string
import random

def assign_range(server_id : str, limit_algorithm: int):
    server_range = f"({server_id}, {limit_algorithm}]"
    modified_range = f"({server_id}, {limit_algorithm}) U [0, {server_id}]"
    return server_range, modified_range

def print_ranges(server_id : str, successor : str, server_range : str, modified_range : str, listen : str):
    msg = f"""
    Identificador del servidor : {server_id}
    Donde escucha el servidor: {listen}
    sucesor : {successor}
    Rango establecido : {server_range}
    Rango modificado : {modified_range}
    """
    print(msg)

def get_ports(url: str):
    return f"tcp://*:{url}", f"tcp://localhost:{url}"

def get_range(modified_range : str, start_character : str, only : bool = False, left : bool = True):
    items_1 = {'(': ')', '[': ']'}
    items_2 = {'(': ']'}
    start_index = modified_range.find(start_character)
    item_option = items_2 if only else items_1
    string = ''
    while True:
        if modified_range[start_index] != item_option[start_character]:
            string += modified_range[start_index]
        else:
            break
        start_index += 1
    string += item_option[start_character]

    string = string.replace('[', '(')
    string = string.replace(']', ')')

    # agregarle las modificaciones para que los rangos queden bien
    if only:
        result = []
        for c in string:
            if c == ',':
                result.append(
                    '+1'
                )
            if c == ')':
                result.append(
                    '+1'
                )
            result.append(c)
    else:
        #izquierda
        result = []
        if left:
            for c in string:
                if c == ',':
                    result.append('+1')
                result.append(c)
        #derecha
        else:
            for c in string:
                if c == ')':
                    result.append('+1')
                result.append(c)

    return ''.join(result)

def review_responsibility(new_node_identifier : int , modified_range : str):
    if 'U' in modified_range:
        # es porque tenemos dos rangos, comprobamos el primer rango y despues comprobamos el segundo
        range_1 = get_range(modified_range, '(')
        judgment = f"True if {new_node_identifier} in range{range_1} else False"

        if eval(judgment):
            #print(range_1)
            return True

        range_2 = get_range(modified_range, '[', left=False)
        judgment = f"True if {new_node_identifier} in range{range_2} else False"

        if eval(judgment):
            #print(range_2)
            return True

        return False

    else:
        # es porque solo tenemos un rango
        range_1 = get_range(modified_range, '(', only=True)
        judgment = f"True if {new_node_identifier} in range{range_1} else False"

        if eval(judgment):
            #print(range_1)
            return True

        return False

def adjust_ranges(range_1 : str, LIMIT_ALGORITHM : int):
    numbers = ''
    for c in range_1:
        if c != ',':
            if c.isdigit():
                numbers += c
        else:
            numbers += ' '

    x = numbers.split(sep=' ')

    if int(x[0]) > int(x[1]):
        server_range = range_1
        modified_range = f"({int(x[0])}, {LIMIT_ALGORITHM}) U [0, {int(x[1])}]"
        return server_range, modified_range
    else:
        return range_1, range_1

def report_response(response : dict):
    msg = f"""
    --- Respuesta de un Nodo del anillo---
    Id del Servidor:{response['server_id']}
    El Rango Del Servidor es:{response['modified_range']}
    conexion Al Succesor es: {response['successor']}
    Respuesta Del Servidor : {response['response']}
    """
    print(msg)

def report_conection(id_new_node : str, server_id : str, predeccessor : str):
    msg = f"""
    ----- Información de conexión----
    El nuevo nodo que se va ingresar al anillo es:{id_new_node}
    Ese nuevo nodo, va a puntar al nodo:{server_id}
    El predecesor del nodo:{server_id}, era el nodo:{predeccessor}
    """
    print(msg)


def generate_server_id(n):
    sha1 = hashlib.sha1()
    cadena =  ''.join([random.choice(string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(n)])
    sha1.update(cadena.encode())

    return int(sha1.hexdigest(), 16)


#print(review_responsibility(815214802406361232556826505624409233887463191431, '(662403047594505137831771753655161236886256407857, 1178064936386267465930441796275973080866459643147]'))
#print(adjust_ranges('(50, 29]', 64))