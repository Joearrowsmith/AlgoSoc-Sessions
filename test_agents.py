## Setup Helper Functions

def setup_agent_0(backtest='data/backtest_GBPUSD_tiny.csv'):
    from agent_0_echo import EchoAgent
    agent = EchoAgent(backtest=backtest)
    agent.run()

def setup_agent_1(backtest, verbose):
    from agent_1_simple_macd import SimpleMACDAgent
    agent = SimpleMACDAgent(backtest=backtest, verbose=verbose)
    agent.run()
    
def setup_agent_2(backtest, verbose):
    from agent_2_simple_risk_managed_macd import SimpleRiskMACDAgent
    agent = SimpleRiskMACDAgent(backtest=backtest, verbose=verbose)
    agent.run()

def setup_agent_3(backtest, verbose):
    from agent_3_ret_bound_risk_macd import RetBoundRiskMACDAgent
    agent = RetBoundRiskMACDAgent(backtest=backtest, verbose=verbose)
    agent.run()

def setup_agent_4(backtest, verbose):
    from agent_4_decision_tree import DecisionTreeAgent
    agent = DecisionTreeAgent(backtest=backtest, verbose=verbose)
    agent.run()
    
## Test Functions
    
def test_agent_0(backtest='data/backtest_GBPUSD_tiny.csv'):
    setup_agent_0(backtest=backtest)
    
def test_agent_1(backtest='data/backtest_GBPUSD_tiny.csv'):
    setup_agent_1(backtest=backtest, verbose=False)
    setup_agent_1(backtest=backtest, verbose=True)
    
def test_agent_2(backtest='data/backtest_GBPUSD_tiny.csv'):
    setup_agent_2(backtest=backtest, verbose=False)
    setup_agent_2(backtest=backtest, verbose=True)
    
def test_agent_3(backtest='data/backtest_GBPUSD_tiny.csv'):
    setup_agent_3(backtest=backtest, verbose=False)
    setup_agent_3(backtest=backtest, verbose=True)
    
def test_agent_4(backtest='data/backtest_GBPUSD_tiny.csv'):
    setup_agent_4(backtest=backtest, verbose=False)
    setup_agent_4(backtest=backtest, verbose=True)

def test_param_optimisation_agent_1(backtest='data/backtest_GBPUSD_tiny.csv'):
    from param_optimisation_tests import expicit_optimise_with_agent_1
    expicit_optimise_with_agent_1(backtest=backtest, simple=True)
    
def test_param_optimisation_agent_2(backtest='data/backtest_GBPUSD_tiny.csv'):
    from param_optimisation_tests import expicit_optimise_with_agent_2
    expicit_optimise_with_agent_2(backtest=backtest, simple=True)
    
def test_param_optimisation_agent_3(backtest='data/backtest_GBPUSD_tiny.csv'):
    from param_optimisation_tests import expicit_optimise_with_agent_3
    expicit_optimise_with_agent_3(backtest=backtest, simple=True)
    
def test_param_optimisation_agent_4(backtest='data/backtest_GBPUSD_tiny.csv'):
    from param_optimisation_tests import expicit_optimise_with_agent_4
    expicit_optimise_with_agent_4(backtest=backtest, simple=True)
    
def test_param_optimisation_verbose_sort(backtest='data/backtest_GBPUSD_tiny.csv'):
    from param_optimisation_tests import expicit_optimise_with_agent_1
    expicit_optimise_with_agent_1(backtest=backtest, simple=True, sort=True, verbose=False)
    expicit_optimise_with_agent_1(backtest=backtest, simple=True, sort=False, verbose=True)