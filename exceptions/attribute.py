from enum import Enum

class PropertyExceptionCode (Enum):
    PROPERTY_NOT_RECOGNIZED = "PRORPERTY_NOT_RECOGNIZED",
    PROPERTY_VALUE_ERROR = "PRORPERTY_VALUE_ERROR",
    PROPERTY_NOT_FOUND = "PRORPERTY_NOT_FOUND",

class PropertyException(Exception):
    code=None 
    def __init__(self, code):
        self.code = code
        super().__init__(self)



