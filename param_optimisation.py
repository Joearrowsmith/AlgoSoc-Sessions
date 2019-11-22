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

    
def print_optimisation_outputs(test_param_balances):
    print("Outputs from optimisation:")
    for idx, test in enumerate(test_param_balances):
        print(f"{idx+1}) {test}")
            

def optimise_with_agent_1(backtest='data/backtest_GBPUSD_12_hours.csv',
                          verbose=False, sort=False, simple=True):
    from agent_1_simple_macd import SimpleMACDAgent
    if verbose:
        print("Testing optimise with agent 1 - Simple MACD")
    if simple:
        test_cases = {'fast_length':[20, 60],
                      'slow_length':[40,120]}
    else:
        test_cases = {'fast_length':[20, 60,100,120,120,250],
                      'slow_length':[40,120,250,250,360,500]}
    test_param_balances = optimise_expected_return(SimpleMACDAgent, test_cases,
                                                   backtest=backtest,
                                                   verbose=verbose,
                                                   sort=sort)
    if verbose:
        print_optimisation_outputs(test_param_balances)
    return test_param_balances


def optimise_with_agent_2(backtest='data/backtest_GBPUSD_12_hours.csv', 
                          verbose=False, sort=False, simple=True):
    from agent_2_simple_risk_managed_macd import SimpleRiskMACDAgent
    if verbose:
        print("Testing optimise with agent 2 - Simple Risk MACD")
    if simple:
        test_cases = {'fast_length':[120]*2,
                      'slow_length':[250]*2,
                      'stop_loss_scaling':[100,100],
                      'take_profit_scaling':[2.5,3.0]}
    else:
        test_cases = {'fast_length':[120]*49,
                      'slow_length':[250]*49,
                      'stop_loss_scaling':  [1.1,1.5,2.0,2.5,3.0,3.5,4.0]*7,
                      'take_profit_scaling':[0.1,1.0,1.5,2.0,2.5,3.0,3.5,
                                             1.0,1.5,2.0,2.5,3.0,3.5,0.1,
                                             1.5,2.0,2.5,3.0,3.5,0.1,1.0,
                                             2.0,2.5,3.0,3.5,0.1,1.0,1.5,
                                             2.5,3.0,3.5,0.1,1.0,1.5,2.0,
                                             3.0,3.5,0.1,1.0,1.5,2.0,2.5,
                                             3.5,0.1,1.0,1.5,2.0,2.5,3.0,]}
    test_param_balances = optimise_expected_return(SimpleRiskMACDAgent, test_cases,
                                                   backtest=backtest,
                                                   verbose=verbose,
                                                   sort=sort)
    if verbose:
        print_optimisation_outputs(test_param_balances)
    return test_param_balances


def optimise_with_agent_3(backtest='data/backtest_GBPUSD_12_hours.csv', 
                               verbose=False, sort=False, simple=True):
    from agent_3_risk_managed_macd import RiskMACDAgent
    if verbose:
        print("Testing optimise with agent 3 - Risk MACD")
    if simple:
        test_cases = {'fast_length':[120]*2,
                      'slow_length':[250]*2,
                      'ret_length':[100,100],
                      'ret_scaling_factor':[2.5,3.0]}
    else:
        test_cases = {'fast_length':[120]*12,
                      'slow_length':[250]*12,
                      'ret_length':[100,200,300,400]*3,
                      'ret_scaling_factor':[2.5,3.0,3.5,4.0,
                                            3.0,3.5,4.0,2.5,
                                            3.5,4.0,2.5,3.0]}
    test_param_balances = optimise_expected_return(RiskMACDAgent, test_cases,
                                                   backtest=backtest,
                                                   verbose=verbose,
                                                   sort=sort)
    if verbose:
        print_optimisation_outputs(test_param_balances)
    return test_param_balances

    
if __name__=='__main__':
    simple=False
    verbose=True
    sort=True
    #optimise_with_agent_1(verbose=verbose, sort=sort, simple=simple)
    optimise_with_agent_2(verbose=verbose, sort=sort, simple=simple)
    #optimise_with_agent_3(verbose=verbose, sort=sort, simple=simple)