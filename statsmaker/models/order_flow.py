import pyro
import torch
import pyro.distributions as dist

class OrderFlowModel:
    def __init__(self):
        self.model = self.order_flow_model

    def order_flow_model(self, data):
        lambda_buy = pyro.sample("lambda_buy", dist.Gamma(1.0, 1.0))
        lambda_sell = pyro.sample("lambda_sell", dist.Gamma(1.0, 1.0))
        
        with pyro.plate("data", len(data)):
            order_type = pyro.sample("order_type", dist.Bernoulli(lambda_buy / (lambda_buy + lambda_sell)))
        
        return order_type

    def fit(self, data, num_samples=1000):
        return pyro.infer.MCMC(pyro.infer.NUTS(self.model), num_samples=num_samples).run(data)

    def predict(self, params, num_samples=100):
        predictive = pyro.infer.Predictive(self.model, params, num_samples=num_samples)
        return predictive(torch.tensor([]))