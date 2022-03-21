# Importing the relevant libraries
import websockets
import pathlib
import ssl
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
if on_heroku:
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(
        pathlib.Path(__file__).with_name('localhost.pem'))

    start_server = websockets.serve(
        echo, "0.0.0.0", PORT)
else:
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(
        pathlib.Path(__file__).with_name('localhost.pem'))
    start_server = websockets.serve(echo, "0.0.0.0", PORT, ssl=ssl_context)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()