from pedlar.agent import Agent

from collections import deque

import numpy as np

class OurEchoAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mids = deque(maxlen=10)
        
    def on_tick(self, bid, ask, time=None):
        mid = (bid + ask)/2
        self.mids.append(mid)
        signal = mid - np.mean(self.mids)
        print(mid, signal)
        if signal > 0:
            self.buy()
        else:
            self.sell()
    
    def on_order(self, order):
        """Called on placing a new order."""
        print("New order:", order)
        print("Orders:", self.orders) # Agent orders only
        pass

    def on_order_close(self, order, profit):
        """Called on closing an order with some profit."""
        print("Order closed", order, profit)
        print("Current balance:", self.balance) # Agent balance only
        pass
        
        
if __name__=='__main__':
#     agent_x = OurEchoAgent(username="joe", password="1234",
#                          ticker="tcp://icats.doc.ic.ac.uk:7000",
#                          endpoint="http://icats.doc.ic.ac.uk")

    agent_x = OurEchoAgent(backtest='backtest_GBPUSD.csv')
    agent_x.run()









