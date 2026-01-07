from ..configs.config import (
    logger_types,
    loggerOutput
)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ..controller.accounting_periods import AccountingPeriodsController

@csrf_exempt
def create_accounting_period_request(request):
    controller = AccountingPeriodsController() 
    result = {}
    try:
        method = request.method
        if method == "POST":
            json_str = request.body.decode("utf-8")
            data = json.loads(json_str)

            result = controller.create_accounting_period(data)
        else:
            result = {
                "error": f"create_accounting_period_request - Method {request.method} is not supported" 
            }
    except Exception as e:
        loggerOutput(method=logger_types.ERROR, message=f"create_accounting_period_request - Caught something: {type(e).__name__} -> {e}")
        result = {
            "error": str(e)
        }
    finally:
        loggerOutput(message=f"create_accounting_period_request - {result}")
        if 'error' in result:
            return JsonResponse(result, status=400)
        else:
            return JsonResponse(result)
    
@csrf_exempt
def close_accounting_period_request(request):
    controller = AccountingPeriodsController() 
    result = {}
    try:
        method = request.method
        if method == "POST":
            json_str = request.body.decode("utf-8")
            data = json.loads(json_str)
            result = controller.close_accounting_period(data)
        else:
            result = {
                "error": f"close_accounting_period_request - Method {request.method} is not supported" 
            }
            loggerOutput(method=logger_types.ERROR, message=result)
    except Exception as e:
        loggerOutput(method=logger_types.ERROR, message=f"close_accounting_period_request - Caught something: {type(e).__name__} -> {e}")
        result = {
            "error": str(e)
        }
    finally:
        loggerOutput(message=f"close_accounting_period_request - {result}")
        if 'error' in result:
            return JsonResponse(result, status=400)
        else:
            return JsonResponse(result)
