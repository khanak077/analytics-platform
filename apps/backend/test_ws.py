import asyncio
import websockets


async def main():
    uri = "ws://127.0.0.1:8000/ws/events"

    async with websockets.connect(uri) as websocket:
        print("Connected to websocket")

        while True:
            message = await websocket.recv()

            print("Received:", message)


asyncio.run(main())