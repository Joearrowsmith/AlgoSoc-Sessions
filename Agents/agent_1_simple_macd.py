'''
 Simple momentum strategy looking at the
 cross over of two moving averages of the returns.
'''

from pedlar.agent import Agent
from Agents.signal import Signal
from collections import deque
import numpy as np


class SimpleMACDAgent(Agent):
    name = "Simple_MACD"

    def __init__(self,
                 fast_length, slow_length,
                 verbose=False, make_order=True, **kwargs):
        super().__init__(**kwargs)
        self.init_tests(fast_length, slow_length)
        self.fast = deque(maxlen=fast_length)
        self.slow = deque(maxlen=slow_length)
        self.verbose = verbose
        self.last_mid = None
        self.make_order = make_order
        self.signal = Signal(False, None, None)

    def init_tests(self, fast_length, slow_length):
        assert fast_length < slow_length, "Fast length must be less than slow length."

    def on_tick(self, bid, ask, time=None):
        '''Called on every tick update.'''
        mid = (bid + ask) / 2
        if self.verbose:
            print(f'Tick: {mid: .05f}, {time}')
        if self.last_mid is None:
            self.last_mid = mid
            return
        self.set_macd_signal(mid)
        self.order()

    def set_macd_signal(self, mid):
        ret = mid-self.last_mid
        self.fast.append(ret)
        self.slow.append(ret)
        slow_mean = np.mean(self.slow)
        fast_mean = np.mean(self.fast)
        signal = fast_mean - slow_mean
        self.signal.set_signal_value(signal)

    def order(self):
        signal = self.signal.value
        if signal > 0:
            self.buy()
        elif signal < 0:
            self.sell()

    def on_order(self, order):
        '''Called on placing a new order.'''
        if self.verbose:
            print('New order:', order)
            print('Orders:', self.orders)  # Agent orders only

    def on_order_close(self, order, profit):
        '''Called on closing an order with some profit.'''
        if self.verbose:
            print('Order closed', order, profit)
            print('Current balance:', self.balance)  # Agent balance only

    def buy(self):
        '''Overloading the Agent.buy function to add our signal update'''
        if self.make_order:
            super().buy()
        self.signal.open("buy")

    def sell(self):
        '''Overloading the Agent.sell function to add our signal update'''
        if self.make_order:
            super().sell()
        self.signal.open("sell")


def main(fast_length=120, slow_length=250, backtest=None, verbose=True):
    if backtest is None:
        agent = SimpleMACDAgent(fast_length=fast_length,
                                slow_length=slow_length,
                                verbose=verbose,
                                username='joe', password='1234',
                                ticker='tcp://icats.doc.ic.ac.uk:7000',
                                endpoint='http://icats.doc.ic.ac.uk')
    else:
        agent = SimpleMACDAgent(fast_length=fast_length,
                                slow_length=slow_length,
                                verbose=verbose,
                                backtest=backtest)
    agent.run()
