from ..configs.config import logger
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
        logger.error(f"create_account_request - Caught something: {type(e).__name__} -> {e}")
        result = {
            "error": str(e)
        }
    finally:
        logger.info(f"create_account_request - {result}")
        if 'error' in result:
            return JsonResponse(result, status=400)
        else:
            return JsonResponse(result)
    
@csrf_exempt
def get_update_account_request(request, id = None):
    controller = ChartOfAccountsController() 
    result = {}
    try:
        if id is None:
            result = {
                "error": "get_update_account_request - Account ID required"
            }
            logger.error(result)
        method = request.method
        if method == "GET":
            result = controller.get_account(id)
        elif method == "PUT":
            json_str = request.body.decode("utf-8")
            data = json.loads(json_str)
            result = controller.update_account(id, data)
        else:
            result = {
                "error": f"get_update_account_request - Method {request.method} is not supported" 
            }
            logger.error(result)
    except Exception as e:
        logger.error(f"get_update_account_request - Caught something: {type(e).__name__} -> {e}")
        result = {
            "error": str(e)
        }
    finally:
        logger.info(f"get_update_account_request - {result}")
        if 'error' in result:
            return JsonResponse(result, status=400)
        else:
            return JsonResponse(result)
