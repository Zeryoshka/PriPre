from .const_model import Const

# Dict of models
# key: name of model
# value: function, for predict results
MODELS = {
    'const': Const
}


class _Models:
    '''
    Class for describing all models
    '''
    def __init__(self, MODELS):
        '''
        Constructor of models object
        param: models - dict
        '''
        self._models = MODELS # Dict of models
        self.names = list(MODELS.keys()) # List of models's names (generate automaticly from MODELS)

    def __getitem__(self, key):
        '''
        Get item magic-method
        '''
        if key in self.names:
            return self._models[key]
        return None

    def load(self):
        '''
        Method for loading model's parametrs
        '''
        print('Loading is start')
        for name, model in self.models.items():
            model.load()
            print(f'Loaded {name}')

    def is_model_exist(self, name):
        '''
        Function for checking existing of model with name
        '''
        return name in self.names


models = _Models(MODELS)