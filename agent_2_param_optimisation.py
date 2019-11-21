def optimise_expected_return(Agent, test_cases, verbose=False, sort=False, **kwargs):
    test_balances = []
    test_params = []
    keys, values = test_cases.keys(), list(test_cases.values())
    check_sublists_same_size(values)
    for current_test_params in zip(*values):
        current_test_dict = dict(zip(keys, current_test_params))
        test_params.append(current_test_dict)
        if verbose:
            print(f'Testing with: {current_test_dict}')
        agent_params = {**current_test_dict, **kwargs}
        agent = Agent(**agent_params)
        agent.run()
        bal = agent.balance
        test_balances.append(bal)
    test_param_balances = list(zip(test_params, test_balances))
    if sort:
        test_param_balances = reversed(sorted(test_param_balances, key = lambda i: i[1]))
    return test_param_balances
    

def check_sublists_same_size(test_list):
    if type(test_list) is not list:
        raise TypeError(f'Not a list: {type(test_list)}')
    len_first = len(test_list[0])
    assert all(len(i) == len_first for i in test_list), 'Sublists not of same size'


def test_optimise_with_agent_1(backtest='data/backtest_GBPUSD_12_hours.csv', verbose=False, sort=False):
    from agent_1_simple_macd import SimpleMACDAgent
    if verbose:
        print("Testing optimise with agent 1 - Simple MACD")
    test_cases = {'fast_length':[ 60,120,250],
                  'slow_length':[120,250,500]}
    test_param_balances = optimise_expected_return(SimpleMACDAgent, test_cases,
                                                   backtest=backtest,
                                                   verbose=verbose,
                                                   sort=sort)
    if verbose:
        print("Outputs from optimisation:")
        for idx, test in enumerate(test_param_balances):
            print(f"{idx+1}) {test}")
    return test_param_balances


def test_optimise_with_agent_3(backtest='data/backtest_GBPUSD_12_hours.csv', verbose=False, sort=False):
    from agent_3_risk_managed_macd import RiskMACDAgent
    if verbose:
        print("Testing optimise with agent 3 - Risk MACD")
    test_cases = {'fast_length':[120]*12,
                  'slow_length':[250]*12,
                  'ret_length':[100,200,300,400]*3,
                  'risk_scaling_factor':[2.5,3.0,3.5,4.0,
                                         3.0,3.5,4.0,2.5,
                                         3.5,4.0,2.5,3.0]}
    test_param_balances = optimise_expected_return(RiskMACDAgent, test_cases,
                                                   backtest=backtest,
                                                   verbose=verbose,
                                                   sort=sort)
    if verbose:
        print("Outputs from optimisation:")
        for idx, test in enumerate(test_param_balances):
            print(f"{idx+1}) {test}")
    return test_param_balances

    
if __name__=='__main__':
    test_optimise_with_agent_1(verbose=True, sort=True)
    test_optimise_with_agent_3(verbose=True, sort=True)