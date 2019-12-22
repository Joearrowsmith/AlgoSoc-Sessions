'''
 Simple momentum strategy looking at the
 cross over of two moving averages of the returns.
'''

from Agents.Core import Core
from time import sleep

class LinearAgent(Core):
    name = "Linear_Agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count = 0
        
    def core_on_tick(self, bid, ask, time=None):
        '''Called on every tick update.'''        
        if self.count == 10:
            print("buying")
            print(self.core_buy(bid, ask))

        if self.count == 30:
            print("closing buy")
            print(self.core_close(bid, ask))
        

        if self.count == 40:
            print("selling")
            print(self.core_sell(bid, ask))
        
        if self.count == 70:
            print("closing sell")
            print(self.core_close(bid, ask))
        
        if self.count == 80:
            print("buying")
            print(self.core_buy(bid, ask))
            
        if self.count == 90:
            print("closing buy - selling")
            print(self.core_sell(bid, ask))

        if self.count == 120:
            print("closing sell")
            print(self.core_close(bid, ask))

        if self.count == 135:
            print("closing nothing")
            print(self.core_close(bid, ask))

        if self.count > 140:
            sleep(10)
        self.count += 1

    def core_on_order_close(self, est_profit, est_order_open_price, order_type):
        print("order close -------------------------------")

    def core_order_open(self, est_order_open_price, order_type):
        print("order open -----------------------------")

def main(rets_length, make_orders, verbose=True, backtest=None):
    if backtest is None:
        agent = LinearAgent(rets_length=rets_length,
                            make_orders=make_orders,
                            verbose=verbose,
                            username='joe', password='1234',
                            ticker='tcp://icats.doc.ic.ac.uk:7000',
                            endpoint='http://icats.doc.ic.ac.uk')
    else:
        agent = LinearAgent(rets_length=rets_length,
                            make_orders=make_orders,
                            verbose=verbose,
                            backtest=backtest)
    agent.run()
