backtest_default = 'data/backtest_GBPUSD_12_hours.csv'
n_default = 5
verbose_default = True
sort_default = True


if __name__ == "__main__":
    from Agents.agent_2_simple_risk_managed_macd import main as agent_2_main

    agent_2_main(backtest=backtest_default)
