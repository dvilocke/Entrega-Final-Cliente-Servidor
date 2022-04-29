def assign_range(server_id : str, limit_algorithm: int):
    server_range = f"({server_id}, {limit_algorithm}]"
    modified_range = f"({server_id}, {limit_algorithm}) U [0, {server_id}]"
    return server_range, modified_range

def print_ranges(server_id : str, server_range : str, modified_range : str):
    msg = f"""
    Identificador del servidor : {server_id}
    Rango establecido : {server_range}
    Rango modificado : {modified_range}
    """
    print(msg)

def get_ports(url: str):
    return f"tcp://*:{url}", f"tcp://localhost:{url}"
