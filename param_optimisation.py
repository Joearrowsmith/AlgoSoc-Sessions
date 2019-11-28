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