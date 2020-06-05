from kraken_wsclient_py import kraken_wsclient_py as client

def my_handler(message):
    # Here you can do stuff with the messages
    print(message)

my_client = client.WssClient()
my_client.start()

my_client.subscribe_public(
    subscription = {
        'name': 'ohlc'
    },
    pair = ['BTC/USD'],
    callback = my_handler
)
