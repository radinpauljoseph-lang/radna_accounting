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
    SYS_CODE,
    JNE_CODE,
    MESSAGE_KEY,
    DETAILS_KEY,
    STATUS_KEY,
    error_map
)

from ..controller.journal_entry import JournalEntryController
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

class JournalEntryRequestMetaData:
    def __init__(self):
        self.CREATE_JOURNAL_ENTRY_REQUEST = "createJournalEntryRequest"
        self.GET_UPDATE_JOURNAL_ENTRY_REQUEST = "getUpdateJournalEntryRequest"

je_request_meta = JournalEntryRequestMetaData()

required_headers = [REQUEST_REFERENCE_NUMBER]

@csrf_exempt
def createJournalEntryRequest(request):
    error_model = ErrorModel().model_dump()
    controller = JournalEntryController() 
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
            controller = JournalEntryController(rrn)

            result = controller.createJournalEntry(data)
            if type(result) is dict:
                if set(result) == set(error_model):
                    raise Exception(result)
        else:
            loggerOutput(rrn=rrn, method=logger_types.ERROR, message=f"{je_request_meta.CREATE_JOURNAL_ENTRY_REQUEST} - Unsupported Request Method")
            error = copy.deepcopy(error_map.get(f"{WEB_CODE}0002"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                method=method
            )
            result = error
            raise Exception(error)
        
    except Exception as err:
        loggerOutput(rrn=rrn, method=logger_types.ERROR, message=f"{je_request_meta.CREATE_JOURNAL_ENTRY_REQUEST} - Caught something: {type(err).__name__} -> {err}")
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
        loggerOutput(rrn=rrn, message=f"{je_request_meta.CREATE_JOURNAL_ENTRY_REQUEST} - DONE: {result}")
        if set(result) == set(error_model):
            return JsonResponse(result, status=result[STATUS_KEY])
        return JsonResponse(result, status=CREATED_RESPONSE_CODE)
        
# @csrf_exempt
# def get_update_journal_entry_request(request, id = None):
#     controller = JournalEntryController() 
#     result = {}
#     try:
#         if id is None:
#             result = {
#                 "error": "get_update_journal_entry_request - Journal Entry ID required"
#             }
#             loggerOutput(method=logger_types.ERROR, message=result)
#         method = request.method
#         if method == "GET":
#             result = controller.get_journal_entry(id)
#         elif method == "PUT":
#             json_str = request.body.decode("utf-8")
#             data = json.loads(json_str)
#             result = controller.update_journal_entry(id, data)
#         else:
#             result = {
#                 "error": f"get_update_journal_entry_request - Method {request.method} is not supported" 
#             }
#             loggerOutput(method=logger_types.ERROR, message=result)
#     except Exception as e:
#         loggerOutput(method=logger_types.ERROR, message=f"get_update_journal_entry_request - Caught something: {type(e).__name__} -> {e}")
#         result = {
#             "error": str(e)
#         }
#     finally:
#         loggerOutput(message=f"get_update_journal_entry_request - {result}")
#         if 'error' in result:
#             return JsonResponse(result, status=400)
#         else:
#             return JsonResponse(result)
        
# @csrf_exempt
# def get_delete_journal_entry_by_transaction_id_request(request, transaction_id = None):
#     controller = JournalEntryController() 
#     result = {}
#     try:
#         if transaction_id is None:
#             result = {
#                 "error": "get_delete_journal_entry_by_transaction_id_request - Journal Entry Transaction ID required"
#             }
#             loggerOutput(method=logger_types.ERROR, message=result)
#         method = request.method
#         if method == "GET":
#             result = controller.get_journal_entry_by_transaction_id(transaction_id)
#         elif method == "DELETE":
#             result = controller.delete_journal_entry_by_transaction_id(transaction_id)
#         else:
#             result = {
#                 "error": f"get_delete_journal_entry_by_transaction_id_request - Method {request.method} is not supported" 
#             }
#             loggerOutput(method=logger_types.ERROR, message=result)
#     except Exception as e:
#         loggerOutput(method=logger_types.ERROR, message=f"get_delete_journal_entry_by_transaction_id_request - Caught something: {type(e).__name__} -> {e}")
#         result = {
#             "error": str(e)
#         }
#     finally:
#         loggerOutput(message=f"get_delete_journal_entry_by_transaction_id_request - {result}")
#         if 'error' in result:
#             return JsonResponse(result, status=400)
#         else:
#             return JsonResponse(result)

    
# @csrf_exempt
# def post_journal_entry_by_month_year_request(request, month, year):
#     controller = JournalEntryController() 
#     result = {}
#     try:
#         if month is None or year is None:
#             result = {
#                 "error": "post_journal_entry_by_month_year_request - Month & Year required"
#             }
#             loggerOutput(method=logger_types.ERROR, message=result)
#         method = request.method
#         if method == "POST":
#             result = controller.post_journal_entry_by_month_year(month, year)
#         else:
#             result = {
#                 "error": f"post_journal_entry_by_month_year_request - Method {request.method} is not supported" 
#             }
#             loggerOutput(method=logger_types.ERROR, message=result)
#     except Exception as e:
#         loggerOutput(method=logger_types.ERROR, message=f"post_journal_entry_by_month_year_request - Caught something: {type(e).__name__} -> {e}")
#         result = {
#             "error": str(e)
#         }
#     finally:
#         loggerOutput(message=f"post_journal_entry_by_month_year_request - {result}")
#         if 'error' in result:
#             return JsonResponse(result, status=400)
#         else:
#             return JsonResponse(result)

    
