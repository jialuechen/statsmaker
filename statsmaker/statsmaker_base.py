# statsmaker/statsmaker_base.py
from .models.price_impact_models import AlmgrenChrissModel, BayesianPriceImpactModel, KyleModel, HubermanStanzlModel, BayesianKyleModel

class StatsmakerBase:
    def __init__(self):
        self.models = {}

    def define_model(self, name, model_class, **kwargs):
        self.models[name] = model_class(**kwargs)

    def calculate_impact(self, name, *args):
        if name in self.models:
            model = self.models[name]
            if hasattr(model, 'calculate_impact'):
                return model.calculate_impact(*args)
            elif hasattr(model, 'calculate_total_impact'):
                return model.calculate_total_impact(*args)
            elif hasattr(model, 'predict'):
                return model.predict(*args)
        else:
            raise ValueError(f"Model {name} is not defined.")

    def fit_model(self, name, *args):
        if name in self.models:
            model = self.models[name]
            if hasattr(model, 'fit'):
                return model.fit(*args)
        else:
            raise ValueError(f"Model {name} is not defined.")