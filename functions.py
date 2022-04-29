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

def get_range(modified_range : str, start_character : str):
    items = {'(' : ')', '[' : ']'}
    start_index = modified_range.find(start_character)
    string = ''
    while True:
        if modified_range[start_index] != items[start_character]:
            string += modified_range[start_index]
        else:
            break
        start_index += 1

    string += items[start_character]
    return string

def review_responsibility(new_node_identifier : int , modified_range : str):
    if 'U' in modified_range:
        # es porque tenemos dos rangos
        pass
    else:
        # es porque solo tenemos un rango
        pass


#get_range(f"(29, 64) U [0, 29]", '[')