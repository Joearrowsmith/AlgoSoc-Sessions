from pedlar.agent import Agent
from collections import deque
import numpy as np

class Core(Agent):

    def __init__(self, rets_length, make_orders, verbose, **kwargs):
        super().__init__(**kwargs)
        self.rets = deque(maxlen=rets_length)
        self.make_orders = make_orders
        self.verbose = verbose

        self.is_order_open = None
        self.is_new_order = None
        self.order_type = "close"
        self.est_order_open_price = None
        self.signal_value = None
        self.prev_tick = None
        
    def set_signal(self, signal_value):
        self.signal_value = signal_value
    
    def on_tick(self, bid, ask, time):
        '''Called on every tick update.'''
        mid = (bid + ask) / 2
        if self.prev_tick is None:
            self.prev_tick = (bid, ask, time)
            return
        prev_mid = (self.prev_tick[0] + self.prev_tick[1])/2
        log_ret = np.log(mid) - np.log(prev_mid)
        if self.verbose:
            print(f'Tick: {mid: .05f}, {log_ret: .06f}, {time}')
        self.rets.append(log_ret)
        self.core_on_tick(bid, ask, time)
        self.prev_tick = (bid, ask, time)
        
    def on_order_close(self, order, profit):
        if self.verbose:
            print(f"Order closed: {order}")
            print(f"Profit: {profit}") 
        
    def on_order(self, order):
        if self.verbose:
            print(f"Order open: {order}")

    def core_close(self, bid, ask):
        self.check_is_new_order("close")
        est_profit = None
        if self.is_new_order:
            est_profit = self.get_est_profit(bid, ask, self.order_type)
            self.est_order_open_price = None
            if self.make_orders:
                self.close()
            self.is_order_open = False
            self.order_type = "close"
        return est_profit

    def core_buy(self, bid, ask):
        print("core buy")
        open_price = ask
        self.check_is_new_order("buy")
        closing_opp_order = self.check_closing_opposite_order("buy")
        est_profit = None
        if self.is_new_order:
            if closing_opp_order:
                est_profit = self.get_est_profit(bid, ask, self.order_type)
            self.est_order_open_price = open_price
            if self.make_orders:
                self.buy()
            if self.verbose:
                print(f"Buy open at ask: {ask}")
            self.is_order_open = True
            self.order_type = "buy"
        return est_profit

    def core_sell(self, bid, ask):
        print("core sell")
        open_price = bid
        self.check_is_new_order("sell")
        closing_opp_order = self.check_closing_opposite_order("sell")
        est_profit = None
        if self.is_new_order:
            if closing_opp_order:
                est_profit = self.get_est_profit(bid, ask, self.order_type)
            self.est_order_open_price = open_price
            if self.make_orders:
                self.sell()
            if self.verbose:
                print(f"Sell open at bid: {bid}")
            self.is_order_open = True
            self.order_type = "sell"
        return est_profit

    def check_is_new_order(self, new_order_type):
        self.is_new_order = (self.order_type != new_order_type)
        if self.is_new_order & self.verbose:
            print(f"New order detected of type: {new_order_type}")
    
    def check_closing_opposite_order(self, new_order_type):
        """ Checks if a previous order open is opposite to the new order 
        and therefore closes that order."""
        if (self.order_type == "buy") & (new_order_type == "sell"):
            if self.verbose:
                print("Closing previous buy order.")
            return True
        elif (self.order_type == "sell") & (new_order_type == "buy"):
            if self.verbose:
                print("Closing previous sell order.")
            return True
        return False

    def get_est_profit(self, bid, ask, order_type):
        est_profit = None
        if order_type == "buy":
            est_profit = bid - self.est_order_open_price
        elif order_type == "sell":
            est_profit = self.est_order_open_price - ask
        else:
            raise TypeError("order_type can only be 'buy' or 'sell'")
        return est_profit

    def core_on_tick(self, bid, ask, time):
        pass
