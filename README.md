<div align=center>
<img src="assets/LLMBroker.jpeg" width="220" height="180" loc>
</div>

# StatsMaker
Pyro-based Market Microstructure Python Library

StatsMaker builds a Numpy-based backtesting engine and employs walk forward optimization to backtest trading strategies. It comes with a factor analysis engine accelerated by GPU and a market prediction module utilizing LLM “YOLO” framework from Hugging Face to build and cache trading indicators to facilitate strategy development. The built-in LLM can automate the detection of patterns in real stock market data and provides insights for informed decision-making in self-defined strategies.


## Dependency
* ultralytics
* ultralyticsplus
* CuPy

## Installation

```
pip install --upgrade statsmaker
```

## License
statsmaker is distributed under Apache-2.0 license.
