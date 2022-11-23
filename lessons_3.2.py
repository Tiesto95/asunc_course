import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)
server_socket.listen()

try:
    conection, client_address = server_socket.accept()
    print(f'Подключен клиент с адресом: {client_address}')

    buffer = b''

    while buffer[-2:] != b'\r\n':
        data = conection.recv(2)
        if not data:
            break
        else:
            buffer += data
    print('Все полученные данные', buffer)
    conection.sendall(buffer)
finally:
    server_socket.close()
