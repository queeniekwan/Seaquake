import ccxt

exchange = ccxt.coinbasepro()
# binance_ticker = binance.id, binance.fetch_tickers('BTC/USDT')

print(exchange.symbols)