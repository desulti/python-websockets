# Importing the relevant libraries
import asyncio

import websockets

# Server data
PORT = 9091
print("Server listening on Port " + str(PORT))
# A set of connected ws clients
connected = set()
dotNetClients = set()
scrapyrtClients = set()
# The main behavior function for this server
async def echo(websocket, path):
    print("A client just connected")
    connected.add(websocket)
    try:
        async for message in websocket:
            print("Received message from client: " + message)
            # Send a response to all connected clients except sender
            for conn in connected:
                if conn != websocket:
                    await conn.send( message)
    # Handle disconnecting clientspython
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")
    finally:
        connected.remove(websocket)
# Start the server
start_server = websockets.serve(echo, "localhost", PORT, ping_interval=None)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()