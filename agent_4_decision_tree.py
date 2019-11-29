## Code adapted from https://github.com/nuric

from pedlar.agent import Agent
from collections import deque
from sklearn import tree


class DecisionTreeAgent(Agent):
    """Trades based on decision tree."""
    name = "Decision_Tree_Agent"
    def __init__(self, horizon=200, max_depth=5,
                 fast_length=120, slow_length=250, 
                 verbose=False, **kwargs):
        super().__init__(**kwargs)
        self.init_tests(fast_length, slow_length, horizon, max_depth)
        
        self.X_train = list() # stores input data
        self.y_train = list() # stores targets - i.e. buy - sell
        
        self.tree = tree.DecisionTreeClassifier(max_depth=max_depth)
        
        self.slow = deque(maxlen=slow_length)
        self.fast = deque(maxlen=fast_length)
        self.verbose = verbose
        
        self.horizon = horizon
        self.order_length = 0
        self.last_mid = None

        
    def init_tests(self, fast_length, slow_length, horizon, max_depth):
        assert fast_length < slow_length, "Fast length must be less than slow length."
        assert horizon > 2, "Horizon must be greater than 2."
        assert max_depth > 0, "Must have positive max depth"
        
        
    def on_tick(self, bid, ask, time=None):
        """Called on every tick update. """
        mid = (bid  + ask) / 2 
        if self.verbose:
            print(f"Tick: {mid: .05f}, {time}")
        
        if self.last_mid is None:
            self.last_mid = mid
            return
        
        # We take the differences to avoid
        # fixing to a specific price value
        ret = mid-self.last_mid
        self.slow.append(ret)
        self.fast.append(ret)
        self.last_mid = mid
        
        # Fill the buffer
        if (len(self.slow) != self.slow.maxlen or
            len(self.fast) != self.fast.maxlen):
            return
        
        # Predict
        try:
            out = self.tree.predict([[fast_avg, slow_avg]])[0]
            if out == 1:
                self.buy()
            else:
                self.sell()
        except: # The tree is not fitted yet
            if not self.orders:
                self.buy() # We just buy as a starting point
        # Wait for the horizon, at some fixed point in the future
        # we will close the order and see how we did.
        self.order_length += 1
        if self.order_length >= self.horizon and self.orders:
            self.order_length = 0
            self.close()

            
    def on_order(self, order):
        """Called on placing a new order."""
        if self.verbose:
            print("New order:", order)
            print("Orders:", self.orders) # Agent orders only
        fast_avg = sum(self.fast)/len(self.fast)
        slow_avg = sum(self.slow)/len(self.slow)
        self.X_train.append([fast_avg, slow_avg]) # Store the information made for this order

        
    def on_order_close(self, order, profit):
        """On order close handler."""
        if self.verbose:
            print("Order closed", order, profit)
            print("Current balance:", self.balance) # Agent balance only
        # Based on the profit decide what to do
        if profit >= 0:
            if order.type == "buy":
                self.y_train.append(1)
            else:
                self.y_train.append(-1)
        else:
            if order.type == "sell":
                self.y_train.append(1)
            else:
                self.y_train.append(-1)
        # Re-learn strategy, i.e. avoid same mistakes
        # repeat successful trade
        self.tree.fit(self.X_train, self.y_train)
        
    
if __name__ == "__main__":
    backtest = True
    verbose = True
    if backtest:
        agent = DecisionTreeAgent(verbose=verbose, backtest="data/backtest_GBPUSD_12_hours.csv")
    else:
        agent = DecisionTreeAgent(verbose=verbose, username="joe", password="1234",
                                  ticker="tcp://icats.doc.ic.ac.uk:7000",
                                  endpoint="http://icats.doc.ic.ac.uk")
    agent.run()