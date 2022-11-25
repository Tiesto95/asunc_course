import asyncio
import socket



async def connections(loop, server_socket):
    while True:
        connect, address = await loop.sock_accept(server_socket)
        print(f'Подключение клиента с адресом {address}')
        connect.setblocking(False)
        asyncio.create_task(read_write(connect, loop))


async def read_write(socket, loop):
    while True:
        data = await loop.sock_recv(socket, 1024)
        print(f'Получены данные {data}')
        await loop.sock_sendall(socket, data)


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.bind(server_address)
    server_socket.setblocking(False)
    server_socket.listen()

    await connections(asyncio.get_event_loop(), server_socket)

asyncio.run(main())
