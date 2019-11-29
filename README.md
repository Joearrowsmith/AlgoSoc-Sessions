# :chart_with_upwards_trend: AlgoSoc-Sessions

<p align="center">
	<img src="https://travis-ci.com/Joearrowsmith/AlgoSoc-Sessions.svg?branch=master"
     		alt="Build Status">
	<img src="https://img.shields.io/badge/Python_3.6.3+-orange"
     		alt="Java Version">
	<img src="https://img.shields.io/github/repo-size/joearrowsmith/AlgoSoc-Sessions"
     		alt="Github Repo Size">
</p>

## Content

1. agent_0_echo.py 
   - The simplest possible agent: prints the current bid, ask and time. Works for backtest and real-time data.
2. agent_1_simple_macd.py
   - A simple momentum strategy looking at the cross over of two moving averages of the returns.
3. agent_2_simple_risk_managed_macd.py
   - A momentum strategy with some risk measures. Uses the logic from the simple MACD and implements a static stop loss and take profit on top.
4. agent_3_ret_bound_risk_macd.py
   - An MACD trading agent with bounded movements of the ret from the mean. This agent tries to detect if underlying asset suddenly moves away from the mean with a larger than expected move.
5. agent_4_decision_tree.py
   - An agent that trains a decision tree as it is running to determine how it should trade.
6. build_dataset.py
   - Collect your own data using the live datastream from the pedlar server.
7. param_optimisation_explicit.py
   - Determine the expected return from using an explicitly defined set of parameters for an agent.
8. param_optimisation_random.py
   - Determine the expected return from using a random search from an upper and lower bound for each parameter for an agent.
9. param_optimisation_tests.py
   - Example tests using the functionality from param_optimisation_tests.py and param_optimisation_random.py.
10. test_agents.py
    - A script to test the code builds when uploaded to github.

---

## Best Agent Backtest Performance through Versions:

1. Simple MACD \[fast length (fl): 20, slow length (sl): 40\] 
   - returns = -2.98...
2. Simple MACD with "optimal" lengths \[fl: 120, sl: 250\]
   - returns = 0.099...
3. MACD with "optimal" length and dynamic risk control \[fl: 120, sl: 250, ret length (rl): 100, risk scaling factor (rsf): 3.5\]
   - returns = 0.899...
4. MACD with "optimal" length and dynamic risk control \[fl : 120, sl : 250, stop loss scaling (sls)} : 1.1, take profit scaling (tps) : 3.5]
   - returns = 1.609...

---

## Next Steps:

### For agents:
- [x] Decision tree based agent
- [ ] Linear model based agent
- [ ] NN based agent
- [ ] RNN based agent
- [ ] RL based agent

### For finding parameters:
- [x] Explicit search
- [x] Random search
- [ ] Grid search
- [ ] Gradient-based search
- [ ] Evolution-based search
- [ ] Sharpe Optimisation

### Combining multiple signals & agents:
- [ ] Ensemble of agents
- [ ] K-Armed bandits

### Risk Control:
- [ ] Time dependent behaviour (e.g. varying behaviour around market open/close)
- [ ] Real time statistics
- [ ] Add post-analysis of trades made.

---

<img src="misc/icats_logo.png" alt="icats_logo" width="150"/>

# About us:

### [Algo soc website](http://www.algosoc.com)

### [Algo soc slack](https://algosoc.slack.com)

## Our trading platform Pedlar:

[Imperial pedlar server](http://icats.doc.ic.ac.uk) &rightarrow; (requires access to Imperial Wifi Network)

![Pedlar](misc/pedlarweb_screenshot.jpg)

#### You can contact us at: <algo.trade@imperial.ac.uk>

<img src="misc/icats_logo.png" alt="icats_logo" width="150"/>