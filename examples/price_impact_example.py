# examples/price_impact_models_example.py
from statsmaker import StatsmakerBase
from statsmaker.models.price_impact_models import AlmgrenChrissModel, BayesianPriceImpactModel, KyleModel, HubermanStanzlModel, BayesianKyleModel
import pyro.distributions as dist

# Create a Statsmaker instance
sm = StatsmakerBase()

# Define the Almgren-Chriss model
sm.define_model("almgren_chriss", AlmgrenChrissModel, sigma=0.02, gamma=0.1, eta=0.01)
impact = sm.calculate_impact("almgren_chriss", 1000, 100000)
print("Almgren-Chriss Price Impact:", impact)

# Define the Kyle model
sm.define_model("kyle", KyleModel, lambda_kyle=0.05)
impact = sm.calculate_impact("kyle", 1000)
print("Kyle Model Price Impact:", impact)

# Define the Huberman and Stanzl model
sm.define_model("huberman_stanzl", HubermanStanzlModel, kappa=0.02, psi=0.1)
impact = sm.calculate_impact("huberman_stanzl", 1000, 100000)
print("Huberman-Stanzl Price Impact:", impact)

# Define the Bayesian Price Impact model
alpha_prior = dist.Normal(0.0, 1.0)
beta_prior = dist.Normal(0.0, 1.0)
sm.define_model("bayesian_price_impact", BayesianPriceImpactModel, alpha_prior=alpha_prior, beta_prior=beta_prior)

# Prepare data
order_sizes = [1000, 2000, 1500, 1200, 1800]
market_volumes = [100000, 150000, 120000, 110000, 130000]
price_impacts = [10, 20, 15, 12, 18]

# Fit the model
params = sm.fit_model("bayesian_price_impact", order_sizes, market_volumes, price_impacts, num_steps=1000)
print("Fitted parameters (Bayesian Price Impact):", params)

# Make predictions
predictions = sm.calculate_impact("bayesian_price_impact", order_sizes, market_volumes)
print("Predicted price impacts (Bayesian Price Impact):", predictions)

# Define the Bayesian Kyle model
lambda_prior = dist.Normal(0.0, 1.0)
sm.define_model("bayesian_kyle", BayesianKyleModel, lambda_prior=lambda_prior)

# Prepare data
order_sizes_kyle = [1000, 2000, 1500, 1200, 1800]
price_impacts_kyle = [50, 100, 75, 60, 90]

# Fit the model
lambda_kyle = sm.fit_model("bayesian_kyle", order_sizes_kyle, price_impacts_kyle, num_steps=1000)
print("Fitted lambda (Bayesian Kyle):", lambda_kyle)

# Make predictions
predictions_kyle = sm.calculate_impact("bayesian_kyle", order_sizes_kyle)
print("Predicted price impacts (Bayesian Kyle):", predictions_kyle)