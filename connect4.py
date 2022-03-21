# Importing the relevant libraries
import websockets
import asyncio
import os
on_heroku = False
if 'ON_HEROKU' in os.environ:
  on_heroku = True
print(on_heroku)
if on_heroku:
    # get the heroku port
    port = int(os.environ.get('PORT', 17995))  # as per OP comments default is 17995
else:
    port = 8080
# Server data
PORT = port
print("Server listening on Port " + str(PORT))
# A set of connected ws clients
connected = set()
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
                    await conn.send(message)
    # Handle disconnecting clients
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")
    finally:
        connected.remove(websocket)

# Start the server
start_server = websockets.serve(echo, "localhost", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()