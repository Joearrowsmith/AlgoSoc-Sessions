from pedlar.agent import Agent
from collections import deque
import numpy as np

class BuildDatasetAgent(Agent):
    '''A trading agent.'''
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_tick(self, bid, ask, time=None):
        '''Called on every tick update.'''
        print('Tick:', bid, ask, time)
        with open('GBPUSSD_301019.csv','a') as fd:
            fd.write(f'tick,{bid},{ask},{time}')

if __name__ == '__main__':
    agent = BuildDatasetAgent(username='joe', password='1234',
                              ticker='tcp://icats.doc.ic.ac.uk:7000',
                              endpoint='http://icats.doc.ic.ac.uk')
    agent.run()
