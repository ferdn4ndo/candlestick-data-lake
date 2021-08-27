"""
AQUI:
    carga inicial database: exchanges e currencies - Por hora binance
    iniciar websocket binance
    deixar loop eterno para manter conexao

apos isso, sera possivel 'inicializar' um currency-pair, onde:
    - insere linha na currency_pair
    - abre/registra par no websocket
    - executa um 'load-historic'
"""
from app.services.consumer_service import ConsumerService

client = BinanceClient()
service = BinanceExchangeService(self.session)

consumer = ConsumerService(client, service)
consumer.populate_exchange_data()

# pair_symbol = 'BTCUSDT'
# consumer.populate_candlesticks(pair_symbol)

asyncio.get_event_loop().run_until_complete()
