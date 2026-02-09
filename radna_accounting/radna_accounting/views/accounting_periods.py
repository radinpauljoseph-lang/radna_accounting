import copy
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..configs.config import (
    logger_types,
    loggerOutput,
    NO_ID
)
from ..configs.response_codes.error_model import ErrorModel
from ..configs.response_codes.mapping import (
    WEB_CODE,
    SYS_CODE,
    ACP_CODE,
    MESSAGE_KEY,
    DETAILS_KEY,
    STATUS_KEY,
    error_map
)

from ..controller.accounting_periods import AccountingPeriodsController
from .request_details.constants import (
    UTF_8,
    REQUEST_REFERENCE_NUMBER,
    POST_METHOD,
    GET_METHOD,
    PUT_METHOD,
    DELETE_METHOD,
    OK_RESPONSE_CODE,
    CREATED_RESPONSE_CODE
)
from .request_details.request_validators import checkRequiredValidators

class AccountingPeriodsRequestMetaData:
    def __init__(self):
        self.CREATING_ACCOUNTING_PERIOD_REQUEST = "createAccountingPeriodRequest"

je_request_meta = AccountingPeriodsRequestMetaData()

required_headers = [REQUEST_REFERENCE_NUMBER]

@csrf_exempt
def createAccountingPeriodRequest(request):
    error_model = ErrorModel().model_dump()
    controller = AccountingPeriodsController() 
    result = {}
    rrn = None
    controller = None
    
    try:
        method = request.method
        if method == POST_METHOD:
            if not checkRequiredValidators(request.headers, required_headers):
                error = copy.deepcopy(error_map.get(f"{WEB_CODE}0001"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    header=', '.join(required_headers)
                )
                result = error
                raise Exception(error)
            
            rrn = request.headers.get(REQUEST_REFERENCE_NUMBER)

            json_str = request.body.decode(UTF_8)
            data = json.loads(json_str)
            controller = AccountingPeriodsController(rrn)

            result = controller.createAccountingPeriod(data)
            if type(result) is dict:
                if set(result) == set(error_model):
                    raise Exception(result)
        else:
            rrn = NO_ID if rrn is None else rrn
            error = copy.deepcopy(error_map.get(f"{WEB_CODE}0002"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                method=method
            )
            result = error
            raise Exception(error)
        
    except Exception as err:
        rrn = NO_ID if rrn is None else rrn
        loggerOutput(rrn=rrn, method=logger_types.ERROR, message=f"{je_request_meta.CREATING_ACCOUNTING_PERIOD_REQUEST} - Caught something: {type(err).__name__} -> {err}")
        error_msg = None
        if len(err.args) == 0 or (len(err.args) > 0 and isinstance(err.args[0], str)):
            error_msg = copy.deepcopy(
                error_map.get(f"{SYS_CODE}400")
            )
            error_msg[DETAILS_KEY] = repr(err)
        else:
            error_msg = err.args[0]
        result = error_msg
    finally:
        del controller
        rrn = NO_ID if rrn is None else rrn
        loggerOutput(rrn=rrn, message=f"{je_request_meta.CREATING_ACCOUNTING_PERIOD_REQUEST} - DONE: {result}")
        if set(result) == set(error_model):
            return JsonResponse(result, status=result[STATUS_KEY])
        return JsonResponse(result, status=CREATED_RESPONSE_CODE)

    

# from ..configs.config import (
#     logger_types,
#     loggerOutput
# )
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from ..controller.accounting_periods import AccountingPeriodsController

# @csrf_exempt
# def create_accounting_period_request(request):
#     controller = AccountingPeriodsController() 
#     result = {}
#     try:
#         method = request.method
#         if method == "POST":
#             json_str = request.body.decode("utf-8")
#             data = json.loads(json_str)

#             result = controller.create_accounting_period(data)
#         else:
#             result = {
#                 "error": f"create_accounting_period_request - Method {request.method} is not supported" 
#             }
#     except Exception as e:
#         loggerOutput(method=logger_types.ERROR, message=f"create_accounting_period_request - Caught something: {type(e).__name__} -> {e}")
#         result = {
#             "error": str(e)
#         }
#     finally:
#         loggerOutput(message=f"create_accounting_period_request - {result}")
#         if 'error' in result:
#             return JsonResponse(result, status=400)
#         else:
#             return JsonResponse(result)
    
# @csrf_exempt
# def close_accounting_period_request(request):
#     controller = AccountingPeriodsController() 
#     result = {}
#     try:
#         method = request.method
#         if method == "POST":
#             json_str = request.body.decode("utf-8")
#             data = json.loads(json_str)
#             result = controller.close_accounting_period(data)
#         else:
#             result = {
#                 "error": f"close_accounting_period_request - Method {request.method} is not supported" 
#             }
#             loggerOutput(method=logger_types.ERROR, message=result)
#     except Exception as e:
#         loggerOutput(method=logger_types.ERROR, message=f"close_accounting_period_request - Caught something: {type(e).__name__} -> {e}")
#         result = {
#             "error": str(e)
#         }
#     finally:
#         loggerOutput(message=f"close_accounting_period_request - {result}")
#         if 'error' in result:
#             return JsonResponse(result, status=400)
#         else:
#             return JsonResponse(result)
