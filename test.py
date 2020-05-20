import ccxtpro
import asyncio
import websockets

print('CCXT Pro version', ccxtpro.__version__)
print('Supported exchanges:', ccxtpro.exchanges)

# async def main():
#     exchange = ccxtpro.kraren({'enableRateLimit': True})
#     symbols = 'BTC/USDT'
#     if exchange.has['watchTickers']:
#         while True:
#             try:
#                 tickers = await exchange.watch_tickers(symbols)
#                 print(exchange.iso8601(exchange.milliseconds()), tickers)
#             except Exception as e:
#                 print(e)
#             # stop the loop on exception or leave it commented to retry
#             # rasie e

# asyncio.get_event_loop().run_until_complete(main())

# binance = ccxt.binance()
# binance_ticker = binance.id, binance.fetch_tickers('BTC/USDT')

# print(type(binance_ticker))