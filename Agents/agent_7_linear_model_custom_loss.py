'''
Agent that uses a linear model to make decisions.
'''

from Agents.core import Core
from collections import deque

import tensorflow as tf

def linear_model(num_rets, loss_func):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(1, activation="tanh",  # we are predicting a position that needs to be between 1 and -1
                              input_shape=(num_rets,))
    ])
    model.compile(optimizer='rmsprop',
                  loss=loss_func)
    return model

def loss_expected_return(predicted_pos, next_return):
    return - tf.reduce_mean(predicted_pos * next_return)

class LinearAgent(Core):
    name = "Linear_Agent_Custom_Loss"

    def __init__(self, train_data_length, predict_ahead, **kwargs):
        super().__init__(**kwargs)
        assert self.rets_length > (1 + predict_ahead), f"Rets length ({self.rets_length}) must be greater than 1+{predict_ahead}."
        assert predict_ahead >= 0, "Must be positive predict ahead."
        self.predict_ahead = int(predict_ahead)
        self.train_data = deque(maxlen=train_data_length)
        self.train_y_data = deque(maxlen=train_data_length)

        self.warmup = int(train_data_length / 2)
        self.x_input_size = self.rets_length - 1 - predict_ahead
        self.lin_model = linear_model(self.x_input_size, loss_expected_return)

        self.counter = 0

    def core_on_tick(self, bid, ask, time=None):
        '''Called on every tick update.'''
        self.counter += 1
        if len(self.rets) < self.rets.maxlen:
            return
        train = list(self.rets)[:-(1 + self.predict_ahead)]
        target = sum(list(self.rets)[-(1 + self.predict_ahead):])

        self.train_data.append(train)
        self.train_y_data.append([target])

        if len(self.train_y_data) > self.warmup:
            if self.counter % 100 == 0:
                # Training period
                self.lin_model.fit(list(self.train_data), list(self.train_y_data),
                                   epochs=10, verbose=0)
            pred_y = self.lin_model.predict([list(self.rets)[(1 + self.predict_ahead):]])
            self.set_signal(pred_y)
            self.order(bid, ask)

    def order(self, bid, ask):
        pos = self.signal_value
        if pos > 0.25:
            self.core_buy(bid, ask)
        elif pos < -0.25:
            self.core_sell(bid, ask)

    def core_order_open(self, est_order_open_price, order_type, bid, ask):
        pass

    def core_on_order_close(self, est_profit, est_order_open_price, order_type):
        pass


def main(train_data_length=1000, predict_ahead=20,
         rets_length=30, signal_mean_length=3, make_orders=True,
         verbose=True, backtest=None):
    if backtest is None:
        agent = LinearAgent(train_data_length, predict_ahead,
                            rets_length=rets_length,
                            signal_mean_length=signal_mean_length,
                            make_orders=make_orders,
                            verbose=verbose,
                            username='joe', password='1234',
                            ticker='tcp://icats.doc.ic.ac.uk:7000',
                            endpoint='http://icats.doc.ic.ac.uk')
    else:
        agent = LinearAgent(train_data_length, predict_ahead,
                            rets_length=rets_length,
                            signal_mean_length=signal_mean_length,
                            make_orders=make_orders,
                            verbose=verbose,
                            backtest=backtest)
    agent.run()
    print(f"Final session balance accurate est: {agent.est_balance[0]:.03f}")
    print(f"Final session balance est: {agent.est_balance[1]:.03f}")
    print("--------------")
