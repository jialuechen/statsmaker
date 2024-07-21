<div align=center>


<img src="assets/img/StatsMaker.png" width="200" height="180" loc>

# Statsmaker: Probabilistic Programming Language for Market Microstructure Modeling

![GitHub license](https://img.shields.io/github/license/jialuechen/statsmaker)
![PyPI version](https://img.shields.io/pypi/v/statsmaker)
![PyPI downloads](https://img.shields.io/pypi/dm/statsmaker)
![Python versions](https://img.shields.io/badge/python-3.6%2B-green)
![Code coverage](https://img.shields.io/codecov/c/github/jialuechen/statsmaker)
![Documentation](https://img.shields.io/readthedocs/statsmaker)

</div>

Statsmaker is a powerful Python library designed for market microstructure modeling, statistical analysis, and trading strategy development. It combines probabilistic programming, machine learning, and financial market microstructure theory to provide a comprehensive toolkit for researchers and traders.

## Features

- Probabilistic programming models based on Uber Pyro
- Market microstructure models (order flow, limit order book, market making, etc.)
- High-frequency trading and dark pool trading models
- Liquidity, volatility, and execution quality metrics
- Portfolio optimization and execution strategy optimization
- Machine learning and reinforcement learning integration
- Data simulation and market replay functionality
- Price impact models including Almgren-Chriss, Kyle, Huberman-Stanzl, Bayesian Price Impact, and Bayesian Kyle models

## Installation

Install statsmaker using pip:

```bash
pip install --upgrade statsmaker
```

## Quick Start

Here are some examples demonstrating various features of statsmaker:

### 1. Order Flow Model

```python
from statsmaker import StatsmakerBase, OrderFlowModel
import torch

# Create a Statsmaker instance
sm = StatsmakerBase()

# Define the order flow model
order_flow_model = OrderFlowModel()
sm.define_model("order_flow", order_flow_model.model)

# Prepare data
data = torch.randint(0, 2, (100,))

# Perform inference
inference_result = sm.infer("order_flow", data)

# Sample from the posterior distribution
posterior_samples = sm.sample("order_flow", inference_result.get_samples())

print(posterior_samples)
```

### 2. High-Frequency Trading Model

```python
from statsmaker import HighFrequencyModel
import pandas as pd

# Prepare your market data
market_data = pd.DataFrame({
    'market_returns': [0.001, -0.002, 0.003, -0.001, 0.002],
    'volume': [1000, 1200, 800, 1100, 900]
})

# Create and fit the high-frequency model
hft_model = HighFrequencyModel()
fit_result = hft_model.fit(market_data)

# Make predictions
predictions = hft_model.predict(market_data, fit_result.get_samples())
print(predictions)
```

### 3. Portfolio Optimization

```python
from statsmaker import MicrostructurePortfolioOptimizer
import numpy as np

# Prepare return data and microstructure data
returns = np.array([0.05, 0.03, 0.02, 0.04, 0.01])
microstructure_data = {
    'spread': [0.01, 0.015, 0.02, 0.01, 0.025],
    'volume': [10000, 8000, 12000, 9000, 11000]
}

# Create and use the portfolio optimizer
optimizer = MicrostructurePortfolioOptimizer(returns, microstructure_data)
optimal_weights = optimizer.optimize(risk_aversion=2)

print("Optimal portfolio weights:", optimal_weights)
```

### 4. Reinforcement Learning Trading Agent

```python
from statsmaker import RLTrader
import pandas as pd

# Prepare your market data
market_data = pd.DataFrame({
    'price': [100, 101, 99, 102, 98, 103],
    'volume': [1000, 1200, 800, 1100, 900, 1300]
})

# Create and train the RL trader
rl_trader = RLTrader(market_data)
rl_trader.train(num_episodes=100)

# Make trading decisions
actions = rl_trader.act(market_data)
print("Actions:", actions)
```

### 5. Price Impact Models

#### Almgren-Chriss Model

```python
from statsmaker import StatsmakerBase, AlmgrenChrissModel
sm = StatsmakerBase()
sm.define_model("almgren_chriss", AlmgrenChrissModel, sigma=0.02, gamma=0.1, eta=0.01)
impact = sm.calculate_impact("almgren_chriss", 1000, 100000)
print("Almgren-Chriss Price Impact:", impact)
```

#### Kyle Model

```python
from statsmaker import StatsmakerBase, KyleModel
sm = StatsmakerBase()
sm.define_model("kyle", KyleModel, lambda_kyle=0.05)
impact = sm.calculate_impact("kyle", 1000)
print("Kyle Model Price Impact:", impact)
```

#### Huberman and Stanzl Model

```python
from statsmaker import StatsmakerBase, HubermanStanzlModel
sm = StatsmakerBase()
sm.define_model("huberman_stanzl", HubermanStanzlModel, kappa=0.02, psi=0.1)
impact = sm.calculate_impact("huberman_stanzl", 1000, 100000)
print("Huberman-Stanzl Price Impact:", impact)
```

#### Bayesian Price Impact Model

```python
from statsmaker import StatsmakerBase, BayesianPriceImpactModel
import pyro.distributions as dist
sm = StatsmakerBase()
alpha_prior = dist.Normal(0.0, 1.0)
beta_prior = dist.Normal(0.0, 1.0)
sm.define_model("bayesian_price_impact", BayesianPriceImpactModel, alpha_prior=alpha_prior, beta_prior=beta_prior)
order_sizes = [1000, 2000, 1500, 1200, 1800]
market_volumes = [100000, 150000, 120000, 110000, 130000]
price_impacts = [10, 20, 15, 12, 18]
params = sm.fit_model("bayesian_price_impact", order_sizes, market_volumes, price_impacts, num_steps=1000)
print("Fitted parameters (Bayesian Price Impact):", params)
predictions = sm.calculate_impact("bayesian_price_impact", order_sizes, market_volumes)
print("Predicted price impacts (Bayesian Price Impact):", predictions)
```

#### Bayesian Kyle Model

```python
from statsmaker import StatsmakerBase, BayesianKyleModel
import pyro.distributions as dist
sm = StatsmakerBase()
lambda_prior = dist.Normal(0.0, 1.0)
sm.define_model("bayesian_kyle", BayesianKyleModel, lambda_prior=lambda_prior)
order_sizes_kyle = [1000, 2000, 1500, 1200, 1800]
price_impacts_kyle = [50, 100, 75, 60, 90]
lambda_kyle = sm.fit_model("bayesian_kyle", order_sizes_kyle, price_impacts_kyle, num_steps=1000)
print("Fitted lambda (Bayesian Kyle):", lambda_kyle)
predictions_kyle = sm.calculate_impact("bayesian_kyle", order_sizes_kyle)
print("Predicted price impacts (Bayesian Kyle):", predictions_kyle)
```

## Contributing

We welcome contributions to `statsmaker`. If you have an idea for a new feature, a bug fix, or an improvement, please fork the repository and submit a pull request.

## License

`statsmaker` is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

This project is built on the shoulders of giants. We want to acknowledge the contributions of the open-source community, particularly the developers of Pyro and other libraries that make probabilistic programming and financial modeling accessible.


