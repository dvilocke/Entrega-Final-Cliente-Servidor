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
        print(range_1)
        range_2 = get_range(modified_range, '[', left=False)
        print(range_2)
    else:
        # es porque solo tenemos un rango
        range_1 = get_range(modified_range, '(', only=True)
        print(range_1)


review_responsibility(25, '(29, 50]')