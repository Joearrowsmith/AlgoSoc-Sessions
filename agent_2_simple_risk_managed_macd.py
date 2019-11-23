from agent_1_simple_macd import SimpleMACDAgent
from collections import deque
import numpy as np

class SimpleRiskMACDAgent(SimpleMACDAgent):
    """An improved MACD trading agent with static risk control measures."""
    name = "Simple_Risk_MACD"
    
    def __init__(self, 
                 stop_loss_scaling=1.5,
                 take_profit_scaling=2.0,
                 fast_length=120, slow_length=250, 
                 verbose=False, **kwargs):
        super().__init__(**kwargs)
        assert fast_length < slow_length
        assert stop_loss_scaling > 1.0
        assert take_profit_scaling > 0.0
        
        self.take_profit_scaling = take_profit_scaling
        self.stop_loss_scaling = stop_loss_scaling
        self.fast = deque(maxlen=fast_length)
        self.slow = deque(maxlen=slow_length)
        self.verbose = verbose
        
        self.tick = {'bid':None, 
                     'ask':None, 
                     'mid':None,
                     'spread':None}
        
        self.last_order = -1
        self.last_signal = 0
        
        
    def on_order(self, order):
        """Called on placing a new order."""
        self.last_order = order.id
        self.last_signal = 1 if order.type == "buy" else -1
        last_spread = self.tick['spread']
        self.stop_loss = -last_spread * self.stop_loss_scaling
        self.take_profit = last_spread*self.take_profit_scaling
        
        if self.verbose:
            print("New order:", order)
            print("Orders:", self.orders) # Agent orders only
            print(f"Order detected; take profit: {self.take_profit: .05f}, stop loss: {self.stop_loss: .05f}")
        
        
    def on_order_close(self, order, profit):
        """Called on closing an order with some profit."""
        if self.verbose:
            print("Order closed", order, profit)
            print("Current balance:", self.balance) # Agent balance only

        
    def on_tick(self, bid, ask, time=None):
        """Called on every tick update."""
        mid = (bid  + ask) / 2 
        spread = ask - bid 
        if self.verbose:
            print(f"Tick: {mid: .05f}, {time}")
        
        signal = self.get_signal(mid)
        
        new_signal = check_if_signal_different_to_last_order_signal(signal, self.last_signal)
        
        if new_signal:
            if self.verbose:
                print(f"New signal: {signal}, {self.last_signal}")
            self.order_macd(signal)
        
        self.tick = {'bid':bid, 'ask':ask,
                     'mid':mid, 'spread':spread}
        
        self.check_take_profit_stop_loss()
    
    
    def check_take_profit_stop_loss(self):
        if self.orders:
            o = self.orders[self.last_order]
            diff = self.tick['bid'] - o.price if o.type == "buy" else o.price - self.tick['ask']
            
            if self.verbose:
                print(f"Gross profit: {diff: .05f}")
            
            if diff > (self.take_profit):
                if self.verbose:
                    print(f"Take profit: {diff: .05f} > {self.take_profit: .05f}")
                self.close()
            if diff < (self.stop_loss):
                if self.verbose:
                    print(f"Stop loss: {diff: .05f} < {self.stop_loss: .05f}")
                self.close()
    
def check_if_signal_different_to_last_order_signal(signal, last_order_signal):
    return np.sign(signal) != np.sign(last_order_signal)
    
        
def test_agent_2(backtest='data/backtest_GBPUSD_12_hours.csv', verbose=False):
    agent = SimpleRiskMACDAgent(backtest=backtest, verbose=verbose)
    agent.run()

    
if __name__ == "__main__":
    backtest = False
    if backtest:
        agent = SimpleRiskMACDAgent(backtest='data/backtest_GBPUSD_12_hours.csv')
    else:
        agent = SimpleRiskMACDAgent(verbose=True, 
                                    username='joe', password='1234',
                                    ticker='tcp://icats.doc.ic.ac.uk:7000',
                                    endpoint='http://icats.doc.ic.ac.uk')
    agent.run()
