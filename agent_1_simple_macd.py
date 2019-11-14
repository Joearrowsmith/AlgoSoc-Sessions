from pedlar.agent import Agent
from collections import deque
import numpy as np

class MyAgent(Agent):
    """A trading agent."""
    
    def __init__(self, fast_length, slow_length, **kwargs):
        assert fast_length < slow_length
        self.fast = deque(maxlen=fast_length)
        self.slow = deque(maxlen=slow_length)
        print("running")
        super().__init__(**kwargs)

    def on_order(self, order):
        """Called on placing a new order."""
        #print("New order:", order)
        #print("Orders:", self.orders) # Agent orders only
        pass

    def on_order_close(self, order, profit):
        """Called on closing an order with some profit."""
        #print("Order closed", order, profit)
        #print("Current balance:", self.balance) # Agent balance only
        pass

    def on_tick(self, bid, ask, time=None):
        """Called on every tick update."""
        #print("Tick:", bid, ask, time)
        
        mid = (bid  + ask) / 2 
        
        self.fast.append(mid)
        self.slow.append(mid)
        
        slow_mean = np.mean(self.slow)
        fast_mean = np.mean(self.fast)
        
        signal = slow_mean - fast_mean
        
        if signal == 0:
            pass
        elif signal > 0:
            self.buy()
        else:
            self.sell()

if __name__ == "__main__":
#     agent = MyAgent(username="joe", password="1234",
#                     ticker="tcp://icats.doc.ic.ac.uk:7000",
#                     endpoint="http://icats.doc.ic.ac.uk")
    test_cases = [[5, 10],[10, 20],[20, 40], [5, 40]]
    test_balances = []
    for test in test_cases:
        print(f"new agent with {test[0]} & {test[1]}")
        agent = MyAgent(fast_length=test[0], 
                        slow_length=test[1], 
                        backtest='backtest_GBPUSD.csv')
        agent.run()
        bal = agent.balance
        test_balances.append(bal)
    
    for outcome in zip(test_cases, test_balances):
        print(outcome)
        