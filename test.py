import ccxt
import time
import pprint as pp

exchange = ccxt.kraken()
exchange.load_products()
pp.pprint(exchange.fetch_ticker("BTC/ETH"))
