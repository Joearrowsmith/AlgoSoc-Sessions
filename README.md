# AlgoSoc-Sessions

Master Branch: ![Master](https://travis-ci.com/Joearrowsmith/AlgoSoc-Sessions.svg?branch=master)

## agent_0_echo.py 
- The simplest possible agent: prints the current bid, ask and time. Works for backtest and real-time data.

## agent_1_simple_macd.py
- A simple momentum strategy looking at the cross over of two moving averages.

## agent_2_risk_managed_macd.py
- A momentum strategy with some risk measures. Inherits the base rules from simple MACD and implements a stop loss and take profit on top.

## build_dataset.py
- A function to collect your own data using the live datastream from the pedlar server.

## param_optimisation.py
- A function to determine the expected return from using an agents different parameters.

## test_agents.py
- A script to test the code builds when uploaded to github.

---

# About us:

### [algo soc](http://www.algosoc.com)

### [algo soc slack](https://algosoc.slack.com)

## Pedlar:

### [pedlar server](http://icats.doc.ic.ac.uk) 

(Requires access to Imperial Wifi Network)

![Pedlar](misc/pedlarweb_screenshot.jpg)

### You can contact us at: <algo.trade@imperial.ac.uk>

<img src="misc/icats_logo.png" alt="icats_logo" width="150"/>