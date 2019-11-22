## Setup Helper Functions

def setup_agent_1(backtest, verbose):
    from agent_1_simple_macd import SimpleMACDAgent
    agent = SimpleMACDAgent(backtest=backtest, verbose=verbose)
    agent.run()
    
def setup_agent_2(backtest, verbose):
    from agent_2_simple_risk_managed_macd import SimpleRiskMACDAgent
    agent = SimpleRiskMACDAgent(backtest=backtest, verbose=verbose)
    agent.run()

def setup_agent_3(backtest, verbose):
    from agent_3_risk_managed_macd import RiskMACDAgent
    agent = RiskMACDAgent(backtest=backtest, verbose=verbose)
    agent.run()

def setup_agent_0(backtest='data/backtest_GBPUSD_tiny.csv'):
    from agent_0_echo import EchoAgent
    agent = EchoAgent(backtest=backtest)
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
    setup_agent_2(backtest=backtest, verbose=False)
    setup_agent_2(backtest=backtest, verbose=True)

def test_param_optimisation_agent_1(backtest='data/backtest_GBPUSD_tiny.csv'):
    from param_optimisation import optimise_with_agent_1
    optimise_with_agent_1(backtest=backtest, simple=True)
    
def test_param_optimisation_agent_2(backtest='data/backtest_GBPUSD_tiny.csv'):
    from param_optimisation import optimise_with_agent_2
    optimise_with_agent_2(backtest=backtest, simple=True)
    
def test_param_optimisation_agent_3(backtest='data/backtest_GBPUSD_tiny.csv'):
    from param_optimisation import optimise_with_agent_3
    optimise_with_agent_3(backtest=backtest, simple=True)
    
def test_param_optimisation_verbose_sort(backtest='data/backtest_GBPUSD_tiny.csv'):
    from param_optimisation import optimise_with_agent_1
    optimise_with_agent_1(backtest=backtest, simple=True, sort=True, verbose=False)
    optimise_with_agent_1(backtest=backtest, simple=True, sort=False, verbose=True)