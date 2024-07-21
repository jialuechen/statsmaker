# statsmaker/models/price_impact_models.py
import pyro
import pyro.distributions as dist
import torch

class AlmgrenChrissModel:
    def __init__(self, sigma, gamma, eta):
        self.sigma = sigma  # Volatility
        self.gamma = gamma  # Permanent impact factor
        self.eta = eta  # Temporary impact factor

    def calculate_permanent_impact(self, order_size):
        return self.gamma * order_size

    def calculate_temporary_impact(self, order_size, market_volume):
        return self.eta * (order_size / market_volume)

    def calculate_total_impact(self, order_size, market_volume):
        permanent_impact = self.calculate_permanent_impact(order_size)
        temporary_impact = self.calculate_temporary_impact(order_size, market_volume)
        return permanent_impact + temporary_impact


class KyleModel:
    def __init__(self, lambda_kyle):
        self.lambda_kyle = lambda_kyle  # Kyle's lambda, the price impact parameter

    def calculate_impact(self, order_size):
        return self.lambda_kyle * order_size


class HubermanStanzlModel:
    def __init__(self, kappa, psi):
        self.kappa = kappa  # Permanent impact factor
        self.psi = psi  # Temporary impact factor

    def calculate_impact(self, order_size, market_depth):
        permanent_impact = self.kappa * order_size
        temporary_impact = self.psi * (order_size / market_depth)
        return permanent_impact + temporary_impact


class BayesianPriceImpactModel:
    def __init__(self, alpha_prior, beta_prior):
        self.alpha_prior = alpha_prior
        self.beta_prior = beta_prior

    def model(self, order_size, market_volume, price_impact=None):
        alpha = pyro.sample("alpha", self.alpha_prior)
        beta = pyro.sample("beta", self.beta_prior)
        price_impact_mean = alpha * order_size + beta * (order_size / market_volume)
        with pyro.plate("data", len(order_size)):
            pyro.sample("obs", dist.Normal(price_impact_mean, 1.0), obs=price_impact)
        
    def guide(self, order_size, market_volume, price_impact=None):
        alpha_loc = pyro.param("alpha_loc", torch.tensor(0.0))
        alpha_scale = pyro.param("alpha_scale", torch.tensor(1.0), constraint=torch.distributions.constraints.positive)
        beta_loc = pyro.param("beta_loc", torch.tensor(0.0))
        beta_scale = pyro.param("beta_scale", torch.tensor(1.0), constraint=torch.distributions.constraints.positive)

        pyro.sample("alpha", dist.Normal(alpha_loc, alpha_scale))
        pyro.sample("beta", dist.Normal(beta_loc, beta_scale))

    def fit(self, order_size, market_volume, price_impact, num_steps=1000):
        pyro.clear_param_store()
        svi = pyro.infer.SVI(model=self.model,
                             guide=self.guide,
                             optim=pyro.optim.Adam({"lr": 0.01}),
                             loss=pyro.infer.Trace_ELBO())
        
        order_size = torch.tensor(order_size)
        market_volume = torch.tensor(market_volume)
        price_impact = torch.tensor(price_impact)
        
        for step in range(num_steps):
            loss = svi.step(order_size, market_volume, price_impact)
            if step % 100 == 0:
                print(f"Step {step} : Loss = {loss}")
                
        return {
            "alpha": pyro.param("alpha_loc").item(),
            "beta": pyro.param("beta_loc").item()
        }

    def predict(self, order_size, market_volume):
        alpha = pyro.param("alpha_loc").item()
        beta = pyro.param("beta_loc").item()
        price_impact_mean = alpha * order_size + beta * (order_size / market_volume)
        return price_impact_mean


class BayesianKyleModel:
    def __init__(self, lambda_prior):
        self.lambda_prior = lambda_prior

    def model(self, order_size, price_impact=None):
        lambda_kyle = pyro.sample("lambda_kyle", self.lambda_prior)
        price_impact_mean = lambda_kyle * order_size
        with pyro.plate("data", len(order_size)):
            pyro.sample("obs", dist.Normal(price_impact_mean, 1.0), obs=price_impact)
        
    def guide(self, order_size, price_impact=None):
        lambda_loc = pyro.param("lambda_loc", torch.tensor(0.0))
        lambda_scale = pyro.param("lambda_scale", torch.tensor(1.0), constraint=torch.distributions.constraints.positive)

        pyro.sample("lambda_kyle", dist.Normal(lambda_loc, lambda_scale))

    def fit(self, order_size, price_impact, num_steps=1000):
        pyro.clear_param_store()
        svi = pyro.infer.SVI(model=self.model,
                             guide=self.guide,
                             optim=pyro.optim.Adam({"lr": 0.01}),
                             loss=pyro.infer.Trace_ELBO())
        
        order_size = torch.tensor(order_size)
        price_impact = torch.tensor(price_impact)
        
        for step in range(num_steps):
            loss = svi.step(order_size, price_impact)
            if step % 100 == 0:
                print(f"Step {step} : Loss = {loss}")
                
        return pyro.param("lambda_loc").item()

    def predict(self, order_size):
        lambda_kyle = pyro.param("lambda_loc").item()
        return lambda_kyle * order_size