from agent_0_echo import EchoAgent
from agent_1_simple_macd import SimpleMACDAgent
from agent_3_risk_managed_macd import RiskMACDAgent

from agent_2_param_optimisation import test_optimise_with_agent_1, test_optimise_with_agent_3

def test_agent_0(backtest='data/backtest_GBPUSD_12_hours.csv'):
    agent = EchoAgent(backtest=backtest)
    agent.run()

def test_agent_1(backtest='data/backtest_GBPUSD_12_hours.csv', verbose=False):
    agent = SimpleMACDAgent(backtest=backtest, verbose=verbose)
    agent.run()
    
def test_agent_3(backtest='data/backtest_GBPUSD_12_hours.csv', verbose=False):
    agent = RiskMACDAgent(backtest=backtest, verbose=verbose)
    agent.run()
    
