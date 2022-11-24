import asyncio
import socket
from asyncio import AbstractEventLoop


async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    while True:

        data = await loop.sock_recv(connection, 1024)
        if data == b'boom':
            raise Exception('Неожиданная ошибка')
        await loop.sock_sendall(connection, data)


async def list_connections(server_socket: socket, loop: AbstractEventLoop) -> None:
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f'Подключен клиент с адресом {address}')
        asyncio.create_task(echo(connection, loop))


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.bind(server_address)
    server_socket.setblocking(False)
    server_socket.listen()

    await list_connections(server_socket, asyncio.get_event_loop())

asyncio.run(main())
