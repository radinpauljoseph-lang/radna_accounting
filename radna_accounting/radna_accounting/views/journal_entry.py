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
    
