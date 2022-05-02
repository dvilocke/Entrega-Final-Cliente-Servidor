def assign_range(server_id : str, limit_algorithm: int):
    server_range = f"({server_id}, {limit_algorithm}]"
    modified_range = f"({server_id}, {limit_algorithm}) U [0, {server_id}]"
    return server_range, modified_range

def print_ranges(server_id : str, successor : str, server_range : str, modified_range : str):
    msg = f"""
    Identificador del servidor : {server_id}
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

def adjust_ranges(range_1 : str):
    numbers = ''
    for c in range_1:
        if c != ',':
            if c.isdigit():
                numbers += c
        else:
            numbers += ' '

    x = numbers.split(sep=' ')

    if int(x[0]) < int(x[1]):
        server_range = range_1
        modified_range = f"({int(x[0])}, {int(x[1])}) U [0, {int(x[0])}]"
        return server_range, modified_range
    else:
        return range_1, range_1

def report_response(response : dict):
    msg = f"""
    Id del Servidor:{response['server_id']}
    El Rango Del Servidor es:{response['modified_range']}
    El Succesor es: {response['successor']}
    Respuesta Del Servidor : {response['response']}
    """
    print(msg)

#print(review_responsibility(77, '(29, 64]'))
print(adjust_ranges('(29, 15]'))