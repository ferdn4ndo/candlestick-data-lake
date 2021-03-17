# Project Structure


## Framework
	
[Tornado](https://www.tornadoweb.org/en/stable/) has native async i/o support and [is faster than Flask and Django according to this benchmark](https://blog.xoxzo.com/2019/04/03/django-vs-flask/)

## Models

### Candlestick

Attributes: 

* id
* open
* high
* low
* close
* volume
* timestamp
* currency_pair_id
* created_at

### CurrencyPair

Attributes:

* id
* exchange_id
* currency_a_id
* currency_b_id
* symbol

### Exchange

Attributes:

* id
* code (must be somehow identified inside the implementations of 'ExchangeService')
* name

### Currency

* id
* symbol
* name
* precision

## Services

### ApiService

to serve regular queries and manage the orm objects (REST) using JWT

### WebRequestService

to be used on syncronous calls to the exchange APIs

### WebSocketService

to be used on asyncronous events triggered by both the data lake (to broadcast recorded candles) and the exchanges that supports event listening (to record candles)

### ExchangeService

to be used as an interface for multiple exchanges implementations
(should have a periodicity of 1m)

### CacheService

computing candlesticks based on latest records for:
3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 1w, 1M
