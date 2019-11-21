from pedlar.agent import Agent
from collections import deque
import numpy as np

from agent_1_simple_macd import SimpleMACDAgent


### what is being implemented
# take profit (make 2* moving std deviation)
# stop loss (make 2* moving std deviation)
###########################


class RiskMACDAgent(SimpleMACDAgent):
    """An improved MACD trading agent with risk control measures."""
    name = "Risk_MACD"
    
    def __init__(self, ret_length=100, fast_length=120, slow_length=250, verbose=False, 
                 **kwargs):
        assert fast_length < slow_length
        self.rets = deque(maxlen=ret_length)
        self.fast = deque(maxlen=fast_length)
        self.slow = deque(maxlen=slow_length)
        
        self.verbose = verbose
        
        super().__init__(**kwargs)
        
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
            print(f'Tick: {mid: .05f}, {time}')
        
        self.order_macd(bid, ask)
        
        
        
        
    
    
    
#     def check_risk(self, bid, ask):
#         profit = self.get_profit(bid, ask)
        
#         #print(f'profit: {profit}')
        
#         self.check_early_stop(profit)
        
    
#     def get_profit(self, bid, ask):
#         if self.orders:
#             o = self.orders[self.last_order]
#             profit = bid - o.price if o.type == "buy" else o.price - ask
#             return profit

            
#     def check_early_stop(self, profit):
#         if profit is not None:
#             if profit > self.early_stop:
#                 print(f'----------------> take profit: {profit}')
#                 self.close()
#             elif profit < (-2 * self.early_stop):
#                 print(f'----------------> stop loss: {profit}')
#                 self.close()

                
#     def trade(self):
#         ret = self.rets[-1]
#         #print('ret:', ret)
#         self.fast.append(ret)
#         self.slow.append(ret)
#         slow_mean = np.mean(self.slow)
#         fast_mean = np.mean(self.fast)
#         signal = fast_mean - slow_mean
        
#         if signal == 0:
#             pass
#         elif signal > 0:
#             #print("buy")
#             self.buy()
#         else:
#             #print("sell")
#             self.sell()
        

if __name__ == "__main__":
    backtest = True
    if backtest:
        agent = RiskMACDAgent(backtest='data/backtest_GBPUSD_12_hours.csv')
    else:
        agent = RiskMACDAgent(username='agent_3', password='1234',
                              ticker='tcp://icats.doc.ic.ac.uk:7000',
                              endpoint='http://icats.doc.ic.ac.uk')
    agent.run()  