from ...configs.config import (
    logger_types,
    loggerOutput
)

def checkRequiredValidators(input_header: dict, required_headers: list):
    for index in range(len(required_headers)):
        if input_header.get(required_headers[index]) is None:
            return False
    return True