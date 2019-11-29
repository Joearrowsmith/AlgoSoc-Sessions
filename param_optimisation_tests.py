from param_optimisation_explicit import explicit_search_max_expected_return, print_optimisation_outputs

from param_optimisation_random import random_search_max_expected_return

def expicit_optimise_with_agent_1(backtest='data/backtest_GBPUSD_12_hours.csv',
                                  verbose=False, sort=False, simple=True):
    from agent_1_simple_macd import SimpleMACDAgent
    if simple:
        test_cases = {'fast_length':[20, 60],
                      'slow_length':[40,120]}
    else:
        test_cases = {'fast_length':[20, 60,100,120,120,250],
                      'slow_length':[40,120,250,250,360,500]}
    test_param_balances = explicit_search_max_expected_return(
        SimpleMACDAgent, test_cases,
        backtest=backtest,
        verbose=verbose,
        sort=sort
    )
    if verbose:
        print_optimisation_outputs(test_param_balances)
    return test_param_balances


def random_optimise_with_agent_1(backtest='data/backtest_GBPUSD_12_hours.csv', 
                                 n=20, verbose=False, sort=True):
    from agent_1_simple_macd import SimpleMACDAgent
    search_dict = {'fast_length':[5, 50, int],
                   'slow_length':[40,250, int]}
    test_param_balances = random_search_max_expected_return(
        SimpleMACDAgent, search_dict, n,
        backtest, verbose, sort
    )
    return test_param_balances
    

def expicit_optimise_with_agent_2(backtest='data/backtest_GBPUSD_12_hours.csv', 
                                  verbose=False, sort=False, simple=True):
    from agent_2_simple_risk_managed_macd import SimpleRiskMACDAgent
    if simple:
        test_cases = {'fast_length':[120]*2,
                      'slow_length':[250]*2,
                      'stop_loss_scaling':[1.1,1.5],
                      'take_profit_scaling':[3.5,5.0]}
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
    test_param_balances = explicit_search_max_expected_return(
        SimpleRiskMACDAgent, test_cases,
        backtest=backtest,
        verbose=verbose,
        sort=sort
    )
    if verbose:
        print_optimisation_outputs(test_param_balances)
    return test_param_balances


def random_optimise_with_agent_2(backtest='data/backtest_GBPUSD_12_hours.csv', 
                                 n=20, verbose=False, sort=True):
    from agent_2_simple_risk_managed_macd import SimpleRiskMACDAgent
    search_dict = {'fast_length':[5, 200, int],
                   'slow_length':[150, 300, int],
                   'stop_loss_scaling':[1.1, 3.0, float],
                   'take_profit_scaling':[0.1, 5.0, float]}
    test_param_balances = random_search_max_expected_return(
        SimpleRiskMACDAgent, search_dict, n, 
        backtest, verbose, sort
    )
    return test_param_balances

def expicit_optimise_with_agent_3(backtest='data/backtest_GBPUSD_12_hours.csv', 
                                  verbose=False, sort=False, simple=True):
    from agent_3_ret_bound_risk_macd import RetBoundRiskMACDAgent
    if simple:
        test_cases = {'fast_length':[120]*2,
                      'slow_length':[250]*2,
                      'ret_length':[100,100],
                      'ret_upper_scaling_factor':[2.5,3.0],
                      'ret_lower_scaling_factor':[2.5,3.0]}
    else:
        test_cases = {'fast_length':[120]*12,
                      'slow_length':[250]*12,
                      'ret_length':[100,200,300,400]*3,
                      'ret_upper_scaling_factor':[2.5,3.0,3.5,4.0,
                                                  3.0,3.5,4.0,2.5,
                                                  3.5,4.0,2.5,3.0],
                      'ret_lower_scaling_factor':[2.5,3.0,3.5,4.0,
                                                  3.0,3.5,4.0,2.5,
                                                  3.5,4.0,2.5,3.0]}
    test_param_balances = explicit_search_max_expected_return(
        RetBoundRiskMACDAgent, test_cases,
        backtest=backtest,
        verbose=verbose,
        sort=sort
    )
    if verbose:
        print_optimisation_outputs(test_param_balances)
    return test_param_balances


def random_optimise_with_agent_3(backtest='data/backtest_GBPUSD_12_hours.csv', 
                                 n=20, verbose=False, sort=True):
    from agent_3_ret_bound_risk_macd import RetBoundRiskMACDAgent
    search_dict = {'fast_length':[5, 200, int],
                   'slow_length':[150, 300, int],
                   'ret_length':[25,500, int],
                   'ret_upper_scaling_factor':[0.1, 5.0, float],
                   'ret_lower_scaling_factor':[0.1, 5.0, float]}
    test_param_balances = random_search_max_expected_return(
        RetBoundRiskMACDAgent, search_dict, n, 
        backtest, verbose, sort
    )
    return test_param_balances


def expicit_optimise_with_agent_4(backtest='data/backtest_GBPUSD_12_hours.csv', 
                          verbose=False, sort=False, simple=True):
    from agent_4_decision_tree import DecisionTreeAgent
    if simple:
        test_cases = {'fast_length':[120]*2,
                      'slow_length':[250]*2,
                      'horizon':[200,250],
                      'max_depth':[3,7]}
    test_param_balances = explicit_search_max_expected_return(
        DecisionTreeAgent, test_cases,
        backtest=backtest,
        verbose=verbose,
        sort=sort
    )
    if verbose:
        print_optimisation_outputs(test_param_balances)
    return test_param_balances

def random_optimise_with_agent_4(backtest='data/backtest_GBPUSD_12_hours.csv', 
                                 n=20, verbose=False, sort=True):
    from agent_4_decision_tree import DecisionTreeAgent
    search_dict = {'fast_length':[5, 200, int],
                   'slow_length':[150, 300, int],
                   'horizon':[20,500,int],
                   'max_depth':[1,10,int]}
    test_param_balances = random_search_max_expected_return(
        DecisionTreeAgent, search_dict, n, 
        backtest, verbose, sort
    )
    return test_param_balances

if __name__=='__main__':
    simple=True
    verbose=True
    sort=True
    expicit_optimise_with_agent_1(verbose=verbose, sort=sort, simple=simple)
    expicit_optimise_with_agent_2(verbose=verbose, sort=sort, simple=simple)
    expicit_optimise_with_agent_3(verbose=verbose, sort=sort, simple=simple)
    expicit_optimise_with_agent_4(verbose=verbose, sort=sort, simple=simple)
    random_optimise_with_agent_1(verbose=verbose, sort=sort, simple=simple)
    random_optimise_with_agent_2(verbose=verbose, sort=sort, simple=simple)
    random_optimise_with_agent_3(verbose=verbose, sort=sort, simple=simple)
    random_optimise_with_agent_4(verbose=verbose, sort=sort, simple=simple)