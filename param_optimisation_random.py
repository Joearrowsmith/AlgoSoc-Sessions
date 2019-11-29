import random

def random_search_max_expected_return(Agent, 
                                      search_dictionary, n_steps, 
                                      backtest, 
                                      verbose=False, sort=True):
    keys, values = search_dictionary.keys(), list(search_dictionary.values())
    failed_runs = 0
    test_param_balances = []
    for n in range(n_steps):
        agent_inputs = {}
        for idx, k in enumerate(keys):
            k_value = random.randrange(values[idx][0], values[idx][1])
            agent_inputs[k] = k_value
        if verbose:
            print(f"{n}) Using {agent_inputs}")
        try:
            agent = Agent(backtest=backtest, verbose=False, **agent_inputs)
            agent.run()
            test_balance = agent.balance
            test_param_balances.append([agent_inputs, test_balance])
        except Exception as E:
            failed_runs += 1
            print(f"Run failed: {E}, fail number: {failed_runs}")
    if sort:
        test_param_balances = list(reversed(sorted(test_param_balances, key=lambda i : i[1])))
    if verbose:
        for i in test_param_balances:
            print(f"{i[1]: .3f} | {i[0]}")
        print(f"Failed runs: {failed_runs}/{n_steps}")
    return test_param_balances


if __name__=='__main__':
    from agent_4_decision_tree import DecisionTreeAgent
    search_dict = {'horizon' : [5, 500],
                   'max_depth' : [3, 12],
                   'fast_length' : [15, 149],
                   'slow_length' : [20, 500]}
    verbose = True
    #backtest='data/backtest_GBPUSD_12_hours.csv'
    backtest='data/backtest_GBPUSD.csv'
    test_param_balances = random_search_max_expected_return(DecisionTreeAgent, search_dict, 
                                                            10, backtest=backtest, verbose=verbose)
    optimum_params = test_param_balances[0]
    agent = DecisionTreeAgent(verbose=verbose,
                              username='Joe', password='1234',
                              ticker='tcp://icats.doc.ic.ac.uk:7000',
                              endpoint='http://icats.doc.ic.ac.uk', **optimum_params[0])