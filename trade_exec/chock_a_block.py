import os
import time

from trader import Trader


def buy_without_impact(trader, stock, total_to_buy):
    ''' Buy without impacting the price too much. '''
    num_bought = 0
    total_cost = 0

    quote = None
    while quote is None:
        try:
            quote = trader.quote(stock)
        except:
            print('No quotes yet.')
            time.sleep(1)
            pass
    # Guess the target price...
    target_price = int(((quote['bid'] + quote['ask']) / 2) * 0.95)

    print('Our target price is something around {}'.format(target_price))

    while num_bought < total_to_buy:
        time.sleep(2)
        try:
            quote = trader.quote(stock)
        except ValueError as e:
            print('Error when getting quote: {}'.format(e))
            continue

        if quote['askSize'] == 0:
            print('No asks')
            continue

        # Give 1% leeway
        ask_price = int(quote['ask'] * 1.01)
        if num_bought == 0:
            quantity = 100
        elif ask_price * 1.05 < target_price:
            # Current price is quite low
            print('Low price')
            quantity = quote['askSize']
        elif ask_price > target_price * 1.02:
            # Current price is a bit too high
            target_to_cost = (target_price * num_bought) / total_cost
            if num_bought >= 100 and target_to_cost < 0.99:
                print('Way too high: {}'.format(target_to_cost))
                # We have spent more than we should: Do not buy
                continue
            else:
                print('Buy a few: {}'.format(target_to_cost))
                # We have spent less than we can, so far
                quantity = 100
        else:
            print('Price is fine')
            # Current price is fine
            quantity = 150

        if num_bought + quantity > total_to_buy:
            quantity = total_to_buy - num_bought

        try:
            buy_status = trader.buy(stock, ask_price, quantity, type='immediate-or-cancel')
        except ValueError as e:
            print('Error when buying stock: {}'.format(e))
            continue

        for fill in buy_status['fills']:
            print('Bought {} at {}'.format(fill['qty'], fill['price']))
            num_bought += fill['qty']
            total_cost += fill['qty'] * fill['price']
        avg_price = 0 if num_bought == 0 else int(total_cost / num_bought)
        print('\tTotal: {} at average price of ${}.{}\n\n'.format(
            num_bought,
            avg_price // 100,
            avg_price % 100,
        ))

def main(api_key):
    account = 'DB63088088'
    venue = 'DUEKEX'
    stock = 'OBOU'

    trader = Trader(api_key, venue, account)
    buy_without_impact(trader, stock, 100000)

if __name__ == '__main__':
    try:
        api_key = os.environ['SF_API_KEY']
    except:
        print('No API key found. Did you forget to set SF_API_KEY?\n\n')
        raise
    main(api_key)
