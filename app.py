import asyncio
import websockets
import json

clients = {}

async def handler(websocket):
    try:
        while True:
            message = await websocket.recv()
            data = json.loads(message)

            # Обробка підключення гравця
            if data['type'] == 'join':
                room = data['room']
                if room not in clients:
                    clients[room] = []
                clients[room].append(websocket)

                # Якщо у кімнаті вже 2 гравці, сповістити про початок гри
                if len(clients[room]) == 2:
                    for client in clients[room]:
                        await client.send(json.dumps({"type": "start", "player": "white" if clients[room][0] == client else "black"}))

            # Обробка ходу гравця
            elif data['type'] == 'move':
                room = data['room']
                for client in clients[room]:
                    if client != websocket:
                        await client.send(json.dumps({"type": "move", "move": data['move']}))

    except websockets.exceptions.ConnectionClosed:
        for room, client_list in clients.items():
            if websocket in client_list:
                client_list.remove(websocket)
                break

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # Зупинка сервера

asyncio.run(main())
