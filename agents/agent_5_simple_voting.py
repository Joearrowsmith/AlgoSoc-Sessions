from pedlar.agent import Agent
from collections import deque
import numpy as np


class SimpleVotingAgent(Agent):
    name = "Mean_voting_agent"

    def __init__(self, agents_list, agents_params, agents_require_pos_func,
                 rets_length, verbose=False, **kwargs):
        super().__init__(**kwargs)
        self.init_tests(agents_list, agents_params, agents_require_pos_func)

        self.agents_inst = []
        for a, p in zip(agents_list, agents_params):
            combined_dict = {**kwargs, **p}
            print(combined_dict)
            self.agents_inst.append(a(**combined_dict))
        self.agents_req_pos_func = agents_require_pos_func

        self.verbose = verbose
        self.last_mid = None
        self.rets = deque(maxlen=rets_length)

    def init_tests(self, agents_list, agents_params, agents_require_pos_func):
        num_agents = len(agents_list)
        num_params = len(agents_params)
        num_pos_func_bool = len(agents_require_pos_func)
        assert (num_agents == num_params == num_pos_func_bool), f'{num_agents}!={num_params}!={num_pos_func_bool}'

    def on_tick(self, bid, ask, time=None):
        mid = (bid + ask) / 2
        if self.verbose:
            print(f'Tick: {mid: .05f}, {time}')
        if self.last_mid is None:
            self.last_mid = mid
            return
        ret = np.log(mid) - np.log(self.last_mid)
        self.rets.append(ret)
        if len(self.rets) < self.rets.maxlen:
            return
        rolling_std = np.std(self.rets)

        pos_funcs = []
        for a, req_pf in zip(self.agents_inst, self.agents_req_pos_func):
            signal = a.on_tick(bid, ask, time)
            if signal is None:
                continue
            if req_pf:
                signal_vol_norm = signal/rolling_std
                pos_func = np.tanh(signal_vol_norm)
            else:
                pos_func = signal
            pos_funcs.append(pos_func)

        voting = np.mean(pos_funcs)
        print(pos_funcs, voting)
        pass


if __name__ == '__main__':
    from agent_1_simple_macd import SimpleMACDAgent
    from agent_4_decision_tree import DecisionTreeAgent
    verbose = False
    agents_list = [SimpleMACDAgent, DecisionTreeAgent]
    agents_params = [{'fast_length': 120,
                      'slow_length': 250,
                      'make_order': False,
                      'verbose': verbose},
                     {'horizon': 100,
                      'max_depth': 3,
                      'fast_length': 120,
                      'slow_length': 250,
                      'make_order': False,
                      'verbose': verbose}]
    agents_require_pos_func = [True, False]
    backtest = True
    if backtest:
        agent = SimpleVotingAgent(agents_list,  agents_params,
                                  agents_require_pos_func, 100,
                                  backtest='../data/backtest_GBPUSD_12_hours.csv')
    else:
        agent = SimpleVotingAgent(agents_list, agents_params,
                                  agents_require_pos_func, 100,
                                  username='joe', password='1234',
                                  ticker='tcp://icats.doc.ic.ac.uk:7000',
                                  endpoint='http://icats.doc.ic.ac.uk')
    agent.run()
