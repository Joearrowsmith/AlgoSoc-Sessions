"""Decision Tree agent."""
from collections import deque
# Install using pip3 install sklearn
from sklearn import tree

from pedlar.agent import Agent


class DecisionTreeAgent(Agent):
  """Trades based on decision tree."""
  name = "Decision_Tree_Agent"
  def __init__(self, **kwargs):
    self.X_train = list() # stores input data
    self.y_train = list() # stores targets - i.e. buy - sell
    self.tree = tree.DecisionTreeClassifier()
    self.slow = deque(maxlen=32)
    self.fast = deque(maxlen=8)
    self.last_bid = None
    self.horizon = 0
    super().__init__(**kwargs) # Must call this

  def on_order(self, order):
    """On order handler."""
    print("ORDER:", order)
    fast_avg = sum(self.fast)/len(self.fast)
    slow_avg = sum(self.slow)/len(self.slow)
    # Store the information made for this order
    self.X_train.append([fast_avg, slow_avg])

  def on_order_close(self, order, profit):
    """On order close handler."""
    print("PROFIT:", profit)
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

  def on_tick(self, bid, ask, time=None):
    """On tick handler."""
    if self.last_bid is None:
      self.last_bid = bid
      return
    # We take the differences to avoid
    # fixing to a specific price value
    self.slow.append(bid-self.last_bid)
    self.fast.append(bid-self.last_bid)
    self.last_bid = bid
    # Fill the buffer
    if (len(self.slow) != self.slow.maxlen or
        len(self.fast) != self.fast.maxlen):
      print("Tick:", bid, ask)
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
    self.horizon += 1
    if self.horizon >= 200 and self.orders:
      self.horizon = 0
      self.close()

if __name__ == "__main__":
  # agent = DecisionTreeAgent(username="memes", password="memes",
                            # ticker="tcp://icats.doc.ic.ac.uk:7000",
                            # endpoint="http://icats.doc.ic.ac.uk")
  agent = DecisionTreeAgent(backtest="data/backtest_GBPUSD_12_hours.csv")
  # agent = DecisionTreeAgent.from_args() # python3 decisiontree.py -b backtest_GBPUSD.csv
  agent.run()