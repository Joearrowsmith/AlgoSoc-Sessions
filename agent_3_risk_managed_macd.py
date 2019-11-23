from agent_1_simple_macd import SimpleMACDAgent
from collections import deque
import numpy as np

class RiskMACDAgent(SimpleMACDAgent):
    """An improved MACD trading agent with dynamic risk control measures."""
    name = "Risk_MACD"
    
    def __init__(self, 
                 ret_length=100, ret_scaling_factor=3.5, 
                 fast_length=120, slow_length=250, 
                 verbose=False, **kwargs):
        super().__init__(**kwargs)
        assert fast_length < slow_length
        
        self.ret_length = ret_length
        self.ret_scaling_factor = ret_scaling_factor
        self.fast = deque(maxlen=fast_length)
        self.slow = deque(maxlen=slow_length)
        self.verbose = verbose
        
        self.warm_up = ret_length
        
        self.reset()
        
        
    def on_order(self, order):
        """Called on placing a new order."""
        if self.verbose:
            print("New order:", order)
            print("Orders:", self.orders) # Agent orders only
        
        
    def on_order_close(self, order, profit):
        """Called on closing an order with some profit."""
        if self.verbose:
            print("Order closed", order, profit)
            print("Current balance:", self.balance) # Agent balance only

        
    def on_tick(self, bid, ask, time=None):
        """Called on every tick update."""
        
        mid = (bid  + ask) / 2 
        if self.verbose:
            print('Tick: {: .05f}, {}'.format(mid, time))
        
        signal = self.get_signal(mid)
        
        if self.count > 3:
            prev_mid = self.fast[-2]
            ret = np.log(mid) - np.log(prev_mid)
            self.rets.append(ret)
            
            rets_mean = np.mean(self.rets)
            self.rets_std = np.std(self.rets)
            
            take_profit = self.rets_std * self.ret_scaling_factor + rets_mean
            stop_loss = -1 * self.rets_std * self.ret_scaling_factor + rets_mean
            if (ret > take_profit) or (ret < stop_loss):
                self.close()
                self.reset()
        if self.warm_up < self.count: 
            self.order_macd(signal)
        self.count += 1
        
    def reset(self):
        self.count = 0
        self.rets_std = 0
        self.rets = deque(maxlen=self.ret_length)

        
def test_agent_3(backtest='data/backtest_GBPUSD_12_hours.csv', verbose=False):
    agent = RiskMACDAgent(backtest=backtest, verbose=verbose)
    agent.run()

    
if __name__ == "__main__":
    backtest = False
    if backtest:
        agent = RiskMACDAgent(backtest='data/backtest_GBPUSD_12_hours.csv')
    else:
        agent = RiskMACDAgent(verbose=True, 
                              username='joe', password='1234',
                              ticker='tcp://icats.doc.ic.ac.uk:7000',
                              endpoint='http://icats.doc.ic.ac.uk')
    agent.run()
