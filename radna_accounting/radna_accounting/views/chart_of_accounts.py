import copy
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..configs.config import (
    logger_types,
    loggerOutput
)
from ..configs.response_codes.error_model import ErrorModel
from ..configs.response_codes.mapping import (
    WEB_CODE,
    COA_CODE,
    MESSAGE_KEY,
    STATUS_KEY,
    error_map
)

from ..controller.chart_of_accounts import ChartOfAccountsController
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

class ChartOfAccountsRequestMetaData:
    def __init__(self):
        self.CREATE_ACCOUNT_REQUEST = "createAccountRequest"
        self.GET_UPDATE_ACCOUNT_REQUEST = "getUpdateAccountRequest"

coa_request_meta = ChartOfAccountsRequestMetaData()

required_headers = [REQUEST_REFERENCE_NUMBER]

@csrf_exempt
def createAccountRequest(request):
    error_model = ErrorModel().model_dump()
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
            controller = ChartOfAccountsController(rrn) 

            result = controller.createAccount(data)

            if type(result) is dict:
                if set(result) == set(error_model):
                    raise Exception(result)
        else:
            loggerOutput(rrn=rrn, method=logger_types.ERROR, message=f"{coa_request_meta.CREATE_ACCOUNT_REQUEST} - Unsupported Request Method")
            error = copy.deepcopy(error_map.get(f"{WEB_CODE}0002"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                method=method
            )
            result = error
            raise Exception(error)
        
    except Exception as e:
        loggerOutput(method=logger_types.ERROR, message=f"{coa_request_meta.CREATE_ACCOUNT_REQUEST} - Caught something: {type(e).__name__} -> {e}")
    finally:
        del controller
        loggerOutput(message=f"{coa_request_meta.CREATE_ACCOUNT_REQUEST} - DONE: {result}")
        if set(result) == set(error_model):
            return JsonResponse(result, status=result[STATUS_KEY])
        return JsonResponse(result, status=CREATED_RESPONSE_CODE)
    
@csrf_exempt
def getUpdateAccountRequest(request, id: str = None):
    error_model = ErrorModel().model_dump()
    result = {}
    rrn = None
    controller = None

    try:
        if not checkRequiredValidators(request.headers, required_headers):
            error = copy.deepcopy(error_map.get(f"{WEB_CODE}0001"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                header=', '.join(required_headers)
            )
            result = error
            raise Exception(error)
        
        rrn = request.headers.get(REQUEST_REFERENCE_NUMBER)
        if id is None:
            error = copy.deepcopy(error_map.get(f"{COA_CODE}0107"))
            result = error
            raise Exception(error)
        
        method = request.method
        controller = ChartOfAccountsController(rrn) 
        if method == GET_METHOD:
            result = controller.getAccount(id)
            if type(result) is dict:
                if set(result) == set(error_model):
                    raise Exception(result)
        elif method == PUT_METHOD:
            json_str = request.body.decode(UTF_8)
            data = json.loads(json_str)
            result = controller.updateAccount(id, data)
            if type(result) is dict:
                if set(result) == set(error_model):
                    raise Exception(result)
        else:
            loggerOutput(rrn=rrn, method=logger_types.ERROR, message=f"{coa_request_meta.GET_UPDATE_ACCOUNT_REQUEST} - Unsupported Request Method")
            error = copy.deepcopy(error_map.get(f"{WEB_CODE}0002"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                method=method
            )
            result = error
            raise Exception(error)
        
    except Exception as e:
        loggerOutput(rrn=rrn, method=logger_types.ERROR, message=f"{coa_request_meta.GET_UPDATE_ACCOUNT_REQUEST} - Caught something: {type(e).__name__} -> {e}")
    finally:
        del controller
        loggerOutput(message=f"get_update_account_request - DONE: {result}")
        if set(result) == set(error_model):
            return JsonResponse(result, status=result[STATUS_KEY])
        return JsonResponse(result, status=OK_RESPONSE_CODE)
