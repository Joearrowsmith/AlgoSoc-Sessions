# Intro Agents

Here you can find 3 basic agents showing the basic structure of a pedlar agent.

- agent_0_echo.py: 
  - An agent that recieves ticks and prints them out.
- agent_1_simple_macd.py: 
  - An agent that uses a macd to generate a signal and make orders based on this signal. https://www.investopedia.com/terms/m/macd.asp
- agent_2_simple_risk_managed_macd.py:
  - An agent that built on top of the simple_macd adds a stop-loss and take-profit. https://www.investopedia.com/terms/s/stop-lossorder.asp
  

## The key prinicples:
- Your agent is a class that inherits from the class 'Agent' and contains some of the key functionality to enable your agent to recieve ticks from the server.

- When your agent recieves a tick, the function 'on_tick' is activated with the parameters 'bid', 'ask' and 'time' (the current properties of the security)

- You can add logic inside the 'on_tick' function to make and close orders. 
  - You can make a buy order by calling 'self.buy()'
  - You can make a sell order by calling 'self.sell()'
  - You can close any open orders by calling 'self.close()'


# Setup
- Starting in the 'AlgoSoc-Sessions' folder inside the terminal.
- Create a virtual environment call 'env' and activate the environment. (More info: https://docs.python.org/3/tutorial/venv.html)
    - Create the enviroment: 
        - <code>python -m venv env</code>
    - Activate the environment:
        - Windows: <code>env/Script/activate</code>
        - Unix (Mac / Linux): <code>env/bin/activate</code>
- Install the requirements from the reqs.txt:
    - <code>python -m pip install -r reqs.txt</code>
- Navigate into this folder.
    - <code>cd Intro_agents</code>
- Run code:
    - Agent 0 : <code>python -m agent_0_echo.py</code>
    - Agent 1 : <code>python -m agent_1_simple_macd.py</code>
    - Agent 2 : <code>python -m agent_2_simple_risk_managed_macd.py</code>
