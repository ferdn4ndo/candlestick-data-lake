import asyncio
import json
import websockets


async def hello():
    # uri = 'wss://stream.binance.com:9443/stream?streams=BTCUSDT@kline_1m'
    # uri = 'wss://stream.binance.com:9443/ws/BTCUSDT@kline_1m'
    uri = 'wss://stream.binance.com:9443/ws'

    async with websockets.connect(uri) as websocket:
        await websocket.send(
            json.dumps(
                {
                    'id': 1,
                    'method': 'SUBSCRIBE',
                    'params': ['BTCUSDT@kline_1m']
                }
            )
        )
        print("1")
        resp = await websocket.recv()
        print("2")
        print(resp)

        await websocket.send(
            json.dumps(
                {
                    'id': 1,
                    'method': 'LIST_SUBSCRIPTIONS',
                }
            )
        )
        resp = await websocket.recv()
        print(resp)
        print('brabo')

        async with ts as tscm:
            while True:
                res = await tscm.recv()
                print(res)
        print('bra')


asyncio.get_event_loop().run_until_complete(hello())
