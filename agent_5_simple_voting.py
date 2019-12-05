from pedlar.agent import Agent
from collections import deque
import numpy as np

class SimpleVotingAgent(Agent):
    name = "Mean_voting_agent"
    
    def __init__(self, agents_list, agents_params, rets_length, verbose=False, **kwargs):
        super().__init__(**kwargs)
        
        self.agents_inst = []
        for a, p in zip(agents_list, agents_params):
            combined_dict = {**kwargs,**p}
            print(combined_dict)
            self.agents_inst.append(a(**combined_dict))
        
        self.verbose = verbose
        self.last_mid = None
        self.rets = deque(maxlen=rets_length)
        
    def on_tick(self, bid, ask, time=None):
        mid = (bid  + ask) / 2 
        if self.verbose:
            print(f'Tick: {mid: .05f}, {time}')
        if self.last_mid is None:
            self.last_mid = mid
            return
        
        ret = np.log(mid) - np.log(self.last_mid)
        
        self.rets.append(ret)
        
        if len(self.rets) < self.rets.maxlen:
            return
        
        current_std = np.std(self.rets)
        
        simple_macd = self.agents_inst[0]
        dt = self.agents_inst[1]
        
        macd_signal = simple_macd.on_tick(bid, ask, time)
        dt_signal = dt.on_tick(bid, ask, time)
        
        
        if macd_signal is None or dt_signal is None:
            return
        
        simple_macd_norm = macd_signal/current_std
        simple_macd_posfunc = np.tanh(simple_macd_norm)
        dt_posfunc = dt_signal
        
        
        
        voting = np.mean([simple_macd_posfunc, dt_posfunc])
        print(voting)
        pass

    
    
if __name__=='__main__':
    from agent_1_simple_macd import SimpleMACDAgent
    from agent_4_decision_tree import DecisionTreeAgent
    agents_list = [SimpleMACDAgent, DecisionTreeAgent]
    agents_params = [{'fast_length':120,
                      'slow_length':250,
                     'make_order':False},
                     {'horizon':100, 'max_depth':3,
                      'fast_length':120, 'slow_length':250,
                      'make_order':False}
    ]
    backtest = True
    if backtest:
        agent = SimpleVotingAgent(agents_list,  agents_params, 100, backtest='data/backtest_GBPUSD_12_hours.csv')
    else:
        agent = SimpleVotingAgent(agents_list, agents_params, 100, username='joe', password='1234',
                          ticker='tcp://icats.doc.ic.ac.uk:7000',
                          endpoint='http://icats.doc.ic.ac.uk')
    agent.run()

    








