import json
import os

import requests

class Trader():
    base_url = 'https://api.stockfighter.io/ob/api'

    def __init__(self, api_key, venue, account):
        self.account = account
        self.venue = venue
        self.api_key = api_key
        self.auth_headers = {'X-Starfighter-Authorization': api_key}

    def request_data(self, *, data=None, headers=None):
        request_data = {'account': self.account, 'venue': self.venue}
        if data is not None:
            request_data.update(data)

        request_data = json.dumps(request_data)

        request_headers = {'X-Starfighter-Authorization': api_key}
        if headers is not None:
            request_headers.update(headers)

        return {'data': request_data, 'headers': request_headers}

    def buy(self, stock, price, quantity):
        order = {
            'symbol': stock,
            'price': price,
            'qty': quantity,
            'direction': 'buy',
            'orderType': 'limit'
        }

        buy_url = '{base_url}/venues/{venue}/stocks/{stock}/orders'.format(
            base_url=self.base_url,
            venue=self.venue,
            stock=stock,
        )

        response = requests.post(buy_url, **self.request_data(data=order))
        return response.json()


def main(api_key):
    account = 'CRS82425746'
    venue = 'UYSJEX'
    stock = 'OMD'

    trader = Trader(api_key, venue, account)
    print(trader.buy(stock, 8000, 100))

if __name__ == '__main__':
    try:
        api_key = os.environ['SF_API_KEY']
    except:
        print('No API key found. Did you forget to set SF_API_KEY?\n\n')
        raise
    main(api_key)
