import pyro
import torch
import pyro.distributions as dist

class HighFrequencyModel:
    def __init__(self):
        self.model = self.high_frequency_model

    def high_frequency_model(self, data):
        alpha = pyro.sample("alpha", dist.Normal(0, 1))
        beta = pyro.sample("beta", dist.Normal(0, 1))
        sigma = pyro.sample("sigma", dist.HalfNormal(1))

        with pyro.plate("data", len(data)):
            returns = pyro.sample("returns", dist.Normal(alpha + beta * data["market_returns"], sigma))
        
        return returns

    def fit(self, data, num_samples=1000):
        return pyro.infer.NUTS(self.model).run(data, num_samples=num_samples)

    def predict(self, data, params):
        predictive = pyro.infer.Predictive(self.model, params, num_samples=100)
        return predictive(data)