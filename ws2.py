from datetime import datetime
import asyncio
import json
from binance import BinanceSocketManager
from binance.client import Client
from binance import AsyncClient, BinanceSocketManager


async def x():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)

    # start any sockets here, i.e a trade socket
    ts = bm.kline_socket('BTCUSDT')

    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            # print(res)

            timestamp = datetime.fromtimestamp(res['E']/1000)
            start = datetime.fromtimestamp(res['k']['t']/1000)
            end = datetime.fromtimestamp(res['k']['T']/1000)
            open = res['k']['o']
            close = res['k']['c']
            high = res['k']['h']
            low = res['k']['l']
            closed = res['k']['x']

            print('timestamp: {} | start: {} | end: {} | open: {} | close: {} | high: {} | low: {} | closed: {}'.format(timestamp, start, end, open, close, high, low, closed))

asyncio.get_event_loop().run_until_complete(x())

"""
{
    "e": "kline",					# event type
    "E": 1499404907056,				# event time
    "s": "ETHBTC",					# symbol
    "k": {
        "t": 1499404860000, 		# start time of this bar
        "T": 1499404919999, 		# end time of this bar
        "s": "ETHBTC",				# symbol
        "i": "1m",					# interval
        "f": 77462,					# first trade id
        "L": 77465,					# last trade id
        "o": "0.10278577",			# open
        "c": "0.10278645",			# close
        "h": "0.10278712",			# high
        "l": "0.10278518",			# low
        "v": "17.47929838",			# volume
        "n": 4,						# number of trades
        "x": false,					# whether this bar is final
        "q": "1.79662878",			# quote volume
        "V": "2.34879839",			# volume of active buy
        "Q": "0.24142166",			# quote volume of active buy
        "B": "13279784.01349473"	# can be ignored
        }
}
"""
