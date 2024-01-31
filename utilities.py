class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setattr__
    __delattr__ = dict.__delattr__

def str_to_boolean (value):
    if value == 'true' or value == 'True' or value == True:
        return True
    if value == 'false' or value == 'False' or value == False:
        return False
    return value


