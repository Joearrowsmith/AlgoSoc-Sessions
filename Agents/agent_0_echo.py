'''
The simplest possible agent: prints the current bid, ask and time.
Works for backtest and real-time data.
'''

from pedlar.agent import Agent


class EchoAgent(Agent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_tick(self, bid, ask, time=None):
        print(f'Tick: {bid: .05f}, {ask: .05f}, {time}')


def main(backtest=None):
    if backtest is None:
        agent = EchoAgent(username='joe', password='1234',
                          ticker='tcp://icats.doc.ic.ac.uk:7000',
                          endpoint='http://icats.doc.ic.ac.uk')
    else:
        agent = EchoAgent(backtest=backtest)
    agent.run()
