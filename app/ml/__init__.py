
def const(x_old, y_old, x_pred):
    return 1

# Dict of models
# key: name of model
# value: function, for predict results
MODELS = {
    'const': const
}

# List of models's names (generate automaticly from MODELS)
MODELS_NAMES = list(MODELS.keys())

def is_model_exist(name):
    '''
    Function for checking existing of model with name
    '''
    return name in MODELS_NAMES
