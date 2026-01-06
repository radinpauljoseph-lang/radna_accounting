from ..configs.config import (
    logger_types,
    loggerOutput
)
from ..utils.decorators.error_handling import catchAndLog
from ..configs.response_codes.error_model import ErrorModel
from ..configs.response_codes.mapping import STATUS_KEY
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ..controller.chart_of_accounts import ChartOfAccountsController

@csrf_exempt
def create_account_request(request):
    controller = ChartOfAccountsController() 
    result = {}
    try:
        method = request.method
        if method == "POST":
            json_str = request.body.decode("utf-8")
            data = json.loads(json_str)

            result = controller.create_account(data)
            
        else:
            result = {
                "error": f"create_account_request - Method {request.method} is not supported" 
            }
    except Exception as e:
        loggerOutput(method=logger_types.ERROR, message=f"create_account_request - Caught something: {type(e).__name__} -> {e}")
        result = {
            "error": str(e)
        }
    finally:
        loggerOutput(message=f"create_account_request - {result}")
        if 'error' in result:
            return JsonResponse(result, status=400)
        else:
            return JsonResponse(result)
    
@csrf_exempt
def get_update_account_request(request, id = None):
    error_model = ErrorModel().model_dump()
    result = {}
    try:
        rrn = request.headers.get("Request-Reference-Number")
        if id is None:
            result = {
                "error": "get_update_account_request - Account ID required"
            }
            loggerOutput(rrn=rrn, method=logger_types.ERROR, message=result)
        method = request.method
        controller = ChartOfAccountsController(rrn) 
        if method == "GET":
            result = controller.get_account(id)
        elif method == "PUT":
            json_str = request.body.decode("utf-8")
            data = json.loads(json_str)
            result = controller.update_account(id, data)
            if type(result) is dict:
                if set(result) == set(error_model):
                    raise Exception(result)
        else:
            result = {
                "error": f"get_update_account_request - Method {request.method} is not supported" 
            }
            loggerOutput(rrn=rrn, method=logger_types.ERROR, message=result)
    except Exception as e:
        loggerOutput(rrn=rrn, method=logger_types.ERROR, message=f"get_update_account_request - Caught something: {type(e).__name__} -> {e}")
    finally:
        loggerOutput(message=f"get_update_account_request - DONE: {result}")
        if set(result) == set(error_model):
            return JsonResponse(result, status=result[STATUS_KEY])
        elif 'error' in result:
            return JsonResponse(result, status=400)
        return JsonResponse(result)
