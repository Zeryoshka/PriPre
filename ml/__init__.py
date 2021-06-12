from .it_is_alive import It_is_alive

# Dict of models
# key: name of model
# value: function, for predict results


MODELS = {
    "It is alive": It_is_alive
}


class Models:
    """
    Class for describing all models
    """

    def __init__(self, MODELS):
        """
        Constructor of models object
        param: models - dict
        """
        self._models = MODELS  # Dict of models
        self._names = list(
            MODELS.keys()
        )  # List of models's names (generate automaticly from MODELS)

    @property
    def names(self):
        """
        Property with list of models names
        """
        return self._names

    def __getitem__(self, key):
        """
        Get item magic-method
        """
        if key in self.names:
            return self._models[key]
        return None

    def load(self):
        """
        Method for loading model's parametrs
        """
        print("Loading is start")
        for name, model in self.models.items():
            model.load()
            print(f"Loaded {name}")

    def is_model_exist(self, name):
        """
        Function for checking existing of model with name
        """
        return name in self.names
