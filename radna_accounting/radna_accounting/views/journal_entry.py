from ..configs.config import logger
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from ..controller.journal_entry import JournalEntryController

from django import forms

@csrf_exempt
def create_journal_entry_request(request):
    controller = JournalEntryController() 
    result = {}
    try:
        method = request.method
        if method == "POST":
            json_str = request.body.decode("utf-8")
            data = json.loads(json_str)

            result = controller.create_journal_entry(data)
        else:
            result = {
                "error": f"create_journal_entry_request - Method {request.method} is not supported" 
            }
    except Exception as e:
        logger.error(f"create_journal_entry_request - Caught something: {type(e).__name__} -> {e}")
        result = {
            "error": str(e)
        }
    finally:
        logger.info(f"create_journal_entry_request - {result}")
        if 'error' in result:
            return JsonResponse(result, status=400)
        else:
            return JsonResponse(result)
        
@csrf_exempt
def get_update_journal_entry_request(request, id = None):
    controller = JournalEntryController() 
    result = {}
    try:
        if id is None:
            result = {
                "error": "get_update_journal_entry_request - Journal Entry ID required"
            }
            logger.error(result)
        method = request.method
        if method == "GET":
            result = controller.get_journal_entry(id)
        elif method == "PUT":
            json_str = request.body.decode("utf-8")
            data = json.loads(json_str)
            result = controller.update_journal_entry(id, data)
        else:
            result = {
                "error": f"get_update_journal_entry_request - Method {request.method} is not supported" 
            }
            logger.error(result)
    except Exception as e:
        logger.error(f"get_update_journal_entry_request - Caught something: {type(e).__name__} -> {e}")
        result = {
            "error": str(e)
        }
    finally:
        logger.info(f"get_update_journal_entry_request - {result}")
        if 'error' in result:
            return JsonResponse(result, status=400)
        else:
            return JsonResponse(result)
        
@csrf_exempt
def get_delete_journal_entry_by_transaction_id_request(request, transaction_id = None):
    controller = JournalEntryController() 
    result = {}
    try:
        if transaction_id is None:
            result = {
                "error": "get_delete_journal_entry_by_transaction_id_request - Journal Entry Transaction ID required"
            }
            logger.error(result)
        method = request.method
        if method == "GET":
            result = controller.get_journal_entry_by_transaction_id(transaction_id)
        elif method == "DELETE":
            result = controller.delete_journal_entry_by_transaction_id(transaction_id)
        else:
            result = {
                "error": f"get_delete_journal_entry_by_transaction_id_request - Method {request.method} is not supported" 
            }
            logger.error(result)
    except Exception as e:
        logger.error(f"get_delete_journal_entry_by_transaction_id_request - Caught something: {type(e).__name__} -> {e}")
        result = {
            "error": str(e)
        }
    finally:
        logger.info(f"get_delete_journal_entry_by_transaction_id_request - {result}")
        if 'error' in result:
            return JsonResponse(result, status=400)
        else:
            return JsonResponse(result)

    
@csrf_exempt
def post_journal_entry_by_month_year_request(request, month, year):
    controller = JournalEntryController() 
    result = {}
    try:
        if month is None or year is None:
            result = {
                "error": "post_journal_entry_by_month_year_request - Month & Year required"
            }
            logger.error(result)
        method = request.method
        if method == "POST":
            result = controller.post_journal_entry_by_month_year(month, year)
        else:
            result = {
                "error": f"post_journal_entry_by_month_year_request - Method {request.method} is not supported" 
            }
            logger.error(result)
    except Exception as e:
        logger.error(f"post_journal_entry_by_month_year_request - Caught something: {type(e).__name__} -> {e}")
        result = {
            "error": str(e)
        }
    finally:
        logger.info(f"post_journal_entry_by_month_year_request - {result}")
        if 'error' in result:
            return JsonResponse(result, status=400)
        else:
            return JsonResponse(result)

    
