import json
import os
import time

import requests

class Trader():
    api_endpoint = 'https://api.stockfighter.io/ob/api'

    def __init__(self, api_key, venue, account):
        self.account = account
        self.venue = venue
        self.api_key = api_key
        self.auth_headers = {'X-Starfighter-Authorization': api_key}

    def url(self, path):
        # Path should contain leading /
        return '{api}/venues/{venue}{path}'.format(
            api=self.api_endpoint,
            venue=self.venue,
            path=path,
        )

    def request(self, method, url, *, data=None):
        request_data = {'account': self.account, 'venue': self.venue}
        if data is not None:
            request_data.update(data)
        request_data = json.dumps(request_data)

        auth_header = {'X-Starfighter-Authorization': self.api_key}
        return requests.request(
            method,
            url,
            data=request_data,
            headers=auth_header,
        ).json()

    def quote(self, stock):
        quote_url = self.url('/stocks/{stock}/quote').format(stock=stock)
        return self.request('get', quote_url)

    def order_status(self, stock, order_id):
        status_url = self.url('/stocks/{stock}/orders/{order_id}').format(
            stock=stock,
            order_id=order_id,
        )
        return self.request('get', status_url)

    def buy(self, stock, price, quantity, *, type='limit'):
        order = {
            'symbol': stock,
            'price': price,
            'qty': quantity,
            'direction': 'buy',
            'orderType': type,
        }

        buy_url = self.url('/stocks/{stock}/orders').format(stock=stock)
        return self.request('post', buy_url, data=order)


def buy_in_blocks(trader, stock, total_to_buy, block_size):
    bought = 0
    while bought < total_to_buy:
        quote = trader.quote(stock)
        try:
            price = int(quote['ask'] * 1.01)
        except:
            print(quote)
        buy_status = trader.buy(stock, price, block_size, type='immediate-or-cancel')
        print(buy_status)
        bought += buy_status['totalFilled']
        time.sleep(1)

def main(api_key):
    account = 'MAA52701793'
    venue = 'NDYPEX'
    stock = 'ITBE'

    trader = Trader(api_key, venue, account)
    buy_in_blocks(trader, stock, 40000, 100)

if __name__ == '__main__':
    try:
        api_key = os.environ['SF_API_KEY']
    except:
        print('No API key found. Did you forget to set SF_API_KEY?\n\n')
        raise
    main(api_key)
