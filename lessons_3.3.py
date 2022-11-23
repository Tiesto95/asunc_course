import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)
server_socket.listen()
server_socket.setblocking(False)

connections = []

try:
    while True:
        try:
            connection, client_address = server_socket.accept()
            connection.setblocking(False)
            print(f'Получен запрос на подключение от {client_address}')
            connections.append(connection)
        except BlockingIOError:
            pass
        for con_client in connections:
            try:
                buffer = b''

                while buffer[-2:] != b'\r\n':
                    data = con_client.recv(2)
                    if not data:
                        break
                    else:
                        print(f'Получены данные {data}')
                        buffer += data
                print(f'Все данные: {buffer}')
                if buffer == b'test\r\n':
                    print('Тревога!!!')
                con_client.send(buffer)
            except BlockingIOError:
                pass
finally:
    server_socket.close()

