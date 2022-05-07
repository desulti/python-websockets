# Importing the relevant libraries
import asyncio
import websockets
import os
# Set port
on_heroku = False
if 'ON_HEROKU' in os.environ:
  on_heroku = True
print(on_heroku)
if on_heroku:
    # get the heroku port
    port = int(os.environ.get('PORT', 17995))  # as per OP comments default is 17995
else:
    port = 9091
# Server data
PORT = port
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
start_server = websockets.serve(echo, "0.0.0.0", PORT, ping_interval=None)
asyncio.get_event_loop().run_until_complete(start_server)
async def heartbeat(self, connection):
        '''
        Sending heartbeat to server every 5 seconds
        Ping - pong messages to verify connection is alive
        '''
        while True:
            try:
            	for conn in connected:
                	if conn != websocket:
                		await connection.send('ping')
                		await asyncio.sleep(10)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break
tasks = [
        asyncio.ensure_future(client.heartbeat(connection))
    ]
asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
asyncio.get_event_loop().run_forever()