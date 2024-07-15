<div align=center>
<img src="assets/StatsMaker.png" width="250" height="220" loc>
</div>

# statsmaker

![GitHub](https://img.shields.io/github/license/jialuechen/statsmaker)
![PyPI](https://img.shields.io/pypi/v/statsmaker)
![Python](https://img.shields.io/pypi/pyversions/statsmaker)

statsmaker is a powerful Python library designed for market microstructure modeling, statistical analysis, and trading strategy development. It combines probabilistic programming, machine learning, and financial market microstructure theory to provide a comprehensive toolkit for researchers and traders.

## Features

- Probabilistic programming models based on Uber Pyro
- Market microstructure models (order flow, limit order book, market making, etc.)
- High-frequency trading and dark pool trading models
- Liquidity, volatility, and execution quality metrics
- Portfolio optimization and execution strategy optimization
- Machine learning and reinforcement learning integration
- Data simulation and market replay functionality

## Installation

Install statsmaker using pip:

```sh
pip install statsmaker
```

## Quick Start

Here's a simple example of using statsmaker for order flow model inference:

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

## Documentation

Detailed documentation can be found at [docs.statsmaker.io](https://docs.statsmaker.io).

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get started.

## License

statsmaker is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for more details.

## Citation

If you use statsmaker in your research, please cite:

```
@software{statsmaker2024,
  author = {Your Name},
  title = {statsmaker: A Python Library for Market Microstructure Modeling and Analysis},
  year = {2024},
  url = {https://github.com/yourusername/statsmaker},
  version = {0.1.0}
}
```

## Contact

If you have any questions or suggestions, please open an issue or contact us directly at contact@statsmaker.io.

## Acknowledgments

We would like to thank the Pyro team at Uber for their excellent probabilistic programming framework, which forms the foundation of many models in statsmaker.
