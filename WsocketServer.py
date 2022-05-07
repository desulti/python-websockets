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
        print("Just join but is removed")
        connected.remove(websocket)
# Start the server
start_server = websockets.serve(echo, "0.0.0.0", PORT, ping_interval=None)
asyncio.get_event_loop().run_until_complete(start_server)
async def heartbeat():
        '''
        Sending heartbeat to server every 5 seconds
        Ping - pong messages to verify connection is alive
        '''
        try:
            print(connected)
            for conn in connected:
                print("Save client")
                await conn.send('ping')
            await asyncio.sleep(10)
        except websockets.exceptions.ConnectionClosed:
            print('Connection with server closed')
async def main():
    task1 = asyncio.create_task(heartbeat())
    await asyncio.sleep(10)
    await task1
async def forever():
    while True:
        await main()
asyncio.get_event_loop().run_until_complete(forever())
asyncio.get_event_loop().run_forever()