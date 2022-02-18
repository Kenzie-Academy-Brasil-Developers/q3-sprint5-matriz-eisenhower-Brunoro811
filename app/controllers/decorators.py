
from functools import wraps
from flask import request
from http import HTTPStatus as httpstatus

def verify_types(correct_types: dict,opitional_keys: bool=False):
    def received_function(function):
        @wraps(function)
        def wrapper(id: int = None):
            data: dict = request.get_json()
            try:
                key_error = []
                if not (opitional_keys):
                    for key, value in correct_types.items():
                        if type(data[key]) != value:
                            key_error.append(data[key])
                else:
                    for key, value in correct_types.items():
                        if not (data.get(key,None) == None):
                            if type(data[key]) != value:
                                key_error.append(data[key])

                if key_error:
                    raise TypeError
                if not id:
                    return function()
                return function(id)
            except TypeError:
                return {
                    "error": "value with type incorrect!",
                    "received wrong": key_error,
                }, httpstatus.UNPROCESSABLE_ENTITY
            except Exception as e:
                raise e

        return wrapper

    return received_function