import pyro

class StatsmakerBase:
    def __init__(self):
        self.models = {}
        
    def define_model(self, name, model_func):
        self.models[name] = model_func
        
    def infer(self, model_name, data, num_samples=1000):
        model = self.models[model_name]
        return pyro.infer.Importance(model, num_samples=num_samples).run(data)
    
    def sample(self, model_name, params, num_samples=1000):
        model = self.models[model_name]
        return pyro.infer.Predictive(model, params, num_samples=num_samples)()






