import copy
from functools import wraps
from typing import Type, Tuple
import traceback

from radna_accounting.configs.response_codes.mapping import (
    SYS_CODE,
    DETAILS_KEY,
    error_map
)
from radna_accounting.configs.config import (
    logger_types,
    loggerOutput
)

def catchAndLog(*exceptions: Type[BaseException]):
    """
    Decorator factory that catches specified exceptions and logs them.

    Usage:
        @catch_and_log(ValueError, KeyError)
        def my_func(...):
            ...
    """
    exceptions_to_catch: Tuple[Type[BaseException], ...] = exceptions or (Exception,)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except exceptions_to_catch as err:
                error_msg = None
                if len(err.args) == 0 or (len(err.args) > 0 and isinstance(err.args[0], str)):
                    error_msg = copy.deepcopy(
                        error_map.get(f"{SYS_CODE}400")
                    )
                    error_msg[DETAILS_KEY] = repr(err)
                else:
                    error_msg = err.args[0]
                loggerOutput(
                    rrn="ERROR",
                    method=logger_types.ERROR, 
                    message=f"{func.__name__} - {error_msg}"
                )
                traceback.print_exc()
                return error_msg

        return wrapper
    return decorator

