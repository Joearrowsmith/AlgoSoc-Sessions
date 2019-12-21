'''
Code adapted from https://github.com/nuric
An agent that trains a decision tree
as it is running to determine how it should trade.
'''

from pedlar.agent import Agent
from collections import deque
from sklearn import tree


class DecisionTreeAgent(Agent):
    name = "Decision_Tree_Agent"

    def __init__(self, horizon, max_depth,
                 fast_length, slow_length,
                 verbose=False, make_order=True, **kwargs):
        super().__init__(**kwargs)
        self.init_tests(fast_length, slow_length, horizon, max_depth)

        self.X_train = list()  # stores input data
        self.y_train = list()  # stores targets - i.e. buy - sell

        self.tree = tree.DecisionTreeClassifier(max_depth=max_depth)

        self.slow = deque(maxlen=slow_length)
        self.fast = deque(maxlen=fast_length)
        self.verbose = verbose
        self.make_order = make_order

        self.horizon = horizon
        self.order_length = 0
        self.last_mid = None
        self.fast_avg, self.slow_avg = None, None

    def init_tests(self, fast_length, slow_length, horizon, max_depth):
        assert fast_length < slow_length, "Fast length must be less than slow length."
        assert horizon > 0, "Horizon must be greater than zero."
        assert max_depth > 0, "Must have positive max depth"

    def on_tick(self, bid, ask, time=None):
        """Called on every tick update. """
        mid = (bid + ask) / 2
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

        signal = self.get_signal(self.fast_avg, self.slow_avg)
        if self.make_order:
            self.order(signal)
        return signal

    def get_signal(self, fast_avg, slow_avg):
        signal = 0
        # Predict
        try:
            signal = self.tree.predict([[fast_avg, slow_avg]])[0]
        except Exception as E:  # The tree is not fitted yet
            if self.verbose:
                print(E)
            if not self.orders:
                signal = 1  # We just buy as a starting point
        # Wait for the horizon, at some fixed point in the future
        # we will close the order and see how we did.
        self.order_length += 1
        if self.order_length >= self.horizon and self.orders:
            self.order_length = 0
            signal = 0
        return signal

    def order(self, signal):
        if signal == 1:
            self.buy()
        else:
            self.sell()

    def on_order(self, order):
        """Called on placing a new order."""
        if self.verbose:
            print("New order:", order)
            print("Orders:", self.orders)  # Agent orders only
        self.fast_avg = sum(self.fast)/len(self.fast)
        self.slow_avg = sum(self.slow)/len(self.slow)
        self.X_train.append([self.fast_avg, self.slow_avg])  # Store the information made for this order

    def on_order_close(self, order, profit):
        """On order close handler."""
        if self.verbose:
            print("Order closed", order, profit)
            print("Current balance:", self.balance)  # Agent balance only
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


def main(horizon=3, max_depth=1,
         fast_length=141, slow_length=311,
         verbose=True, backtest=None):
    if backtest is None:
        agent = DecisionTreeAgent(horizon=horizon,
                                  max_depth=max_depth,
                                  fast_length=fast_length,
                                  slow_length=slow_length,
                                  verbose=verbose,
                                  username="joe", password="1234",
                                  ticker="tcp://icats.doc.ic.ac.uk:7000",
                                  endpoint="http://icats.doc.ic.ac.uk")
    else:
        agent = DecisionTreeAgent(horizon=horizon,
                                  max_depth=max_depth,
                                  fast_length=fast_length,
                                  slow_length=slow_length,
                                  verbose=verbose,
                                  backtest=backtest)
    agent.run()
