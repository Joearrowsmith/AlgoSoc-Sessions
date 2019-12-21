'''
An MACD trading agent with bounded movements of the ret from the mean.
- This agent tries to detect if underlying asset suddenly moves away from
  the mean with a larger than expected move.
'''

from pedlar.agent import Agent
from Agents.signal import Signal
from collections import deque
import numpy as np


class RetBoundRiskMACDAgent(Agent):
    name = "Ret_Bounds_Risk_MACD"

    def __init__(self,
                 ret_length,
                 ret_upper_scaling_factor,
                 ret_lower_scaling_factor,
                 fast_length, slow_length,
                 verbose=False, make_order=True, **kwargs):
        super().__init__(**kwargs)
        self.init_tests(fast_length, slow_length, ret_length,
                        ret_upper_scaling_factor, ret_lower_scaling_factor)

        self.rets_std = 0

        self.ret_length = ret_length
        self.ret_scaling_factor = {'upper': ret_upper_scaling_factor,
                                   'lower': ret_lower_scaling_factor}
        self.ret_bound = {'upper': 0,
                          'lower': 0}
        self.rets = deque(maxlen=self.ret_length)

        self.fast = deque(maxlen=fast_length)
        self.slow = deque(maxlen=slow_length)
        self.verbose = verbose
        self.make_order = make_order
        self.signal = Signal(False, None, None)

        self.last_mid = None
        self.last_signal = 0

    def init_tests(self, fast_length, slow_length, ret_length,
                   ret_upper_scaling_factor, ret_lower_scaling_factor):
        assert fast_length < slow_length, "Fast length must be less than slow length."
        assert ret_length > 3, "Ret length must be at least 3 otherwise array is too small."
        assert ret_upper_scaling_factor > 0, "Ret upper scaling factor must be a positive decimal."
        assert ret_lower_scaling_factor > 0, "Ret lower scaling factor must be a positive decimal."

    def on_tick(self, bid, ask, time=None):
        """Called on every tick update."""
        mid = (bid + ask) / 2
        if self.verbose:
            print(f"Tick: {mid: .05f}, {time}")
        if self.last_mid is None:
            self.last_mid = mid
            return

        ret = np.log(mid) - np.log(self.last_mid)
        signal = self.get_signal(ret)

        self.rets.append(ret)
        rets_mean = np.mean(self.rets)
        rets_std = np.std(self.rets)

        if (ret > self.ret_bound['upper']) or (ret < self.ret_bound['lower']):
            self._close()

        is_new_signal = np.sign(signal) != np.sign(self.last_signal)
        if is_new_signal:
            if self.verbose:
                print(f"New signal: {signal}, {self.last_signal}")
            self.order_macd(signal)
            self.ret_bound['upper'] = rets_std * self.ret_scaling_factor['upper'] + rets_mean
            self.ret_bound['lower'] = -1 * rets_std * self.ret_scaling_factor['lower'] + rets_mean

        self.last_mid = mid
        self.last_signal = signal

    def get_signal(self, mid):
        ret = mid-self.last_mid
        self.fast.append(ret)
        self.slow.append(ret)
        slow_mean = np.mean(self.slow)
        fast_mean = np.mean(self.fast)
        signal = fast_mean - slow_mean
        return signal

    def order_macd(self, signal):
        if signal > 0:
            self._buy()
        elif signal < 1:
            self._sell()

    def on_order(self, order):
        """Called on placing a new order."""
        if self.verbose:
            print("New order:", order)
            print("Orders:", self.orders)  # Agent orders only

    def on_order_close(self, order, profit):
        """Called on closing an order with some profit."""
        if self.verbose:
            print("Order closed", order, profit)
            print("Current balance:", self.balance)  # Agent balance only

    def _buy(self):
        '''Overloading the Agent.buy function to add our signal update'''
        if self.make_order:
            self.buy()
        self.signal.open("buy")

    def _sell(self):
        '''Overloading the Agent.sell function to add our signal update'''
        if self.make_order:
            self.sell()
        self.signal.open("sell")

    def _close(self):
        '''Overloading the Agent.close function to add our signal update'''
        if self.make_order:
            self.close()
        self.signal.close()


def main(ret_length=100,
         ret_upper_scaling_factor=1.2,
         ret_lower_scaling_factor=3.0,
         fast_length=100,
         slow_length=250,
         verbose=True, backtest=None):
    if backtest is None:
        agent = RetBoundRiskMACDAgent(ret_length=ret_length,
                                      ret_upper_scaling_factor=ret_upper_scaling_factor,
                                      ret_lower_scaling_factor=ret_lower_scaling_factor,
                                      fast_length=fast_length,
                                      slow_length=slow_length,
                                      verbose=verbose,
                                      username='joe', password='1234',
                                      ticker='tcp://icats.doc.ic.ac.uk:7000',
                                      endpoint='http://icats.doc.ic.ac.uk')

    else:
        agent = RetBoundRiskMACDAgent(ret_length=ret_length,
                                      ret_upper_scaling_factor=ret_upper_scaling_factor,
                                      ret_lower_scaling_factor=ret_lower_scaling_factor,
                                      fast_length=fast_length,
                                      slow_length=slow_length,
                                      verbose=verbose,
                                      backtest=backtest)
    agent.run()
