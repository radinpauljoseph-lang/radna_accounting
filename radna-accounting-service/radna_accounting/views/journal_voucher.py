import copy
import json
from django.http import (
    JsonResponse,
    HttpResponse
)
from xhtml2pdf import pisa
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from radna_accounting.configs.config import (
    logger_types,
    loggerOutput,
    NO_ID
)
from radna_accounting.configs.response_codes.error_model import ErrorModel
from radna_accounting.configs.response_codes.mapping import (
    WEB_CODE,
    SYS_CODE,
    JNE_CODE,
    MESSAGE_KEY,
    DETAILS_KEY,
    STATUS_KEY,
    error_map
)

from radna_accounting.controller.journal_voucher import JournalVoucherController
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
from radna_accounting.validators.data_model import DATA_KEY
from radna_accounting.validators.journal_voucher import JournalVoucherDocumentDataModel

class JournalVoucherRequestMetaData:
    def __init__(self):
        self.DOWNLOAD_JOURNAL_VOUCHER_REQUEST = "downloadJournalVoucherFileRequest"

jv_request_meta = JournalVoucherRequestMetaData()

required_headers = [REQUEST_REFERENCE_NUMBER]

@csrf_exempt
def downloadJournalVoucherFileRequest(request, id: str):
    error_model = ErrorModel().model_dump()
    controller = JournalVoucherController() 
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
            controller = JournalVoucherController(rrn)

            result = controller.downloadJournalVoucherFile(id)
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
        loggerOutput(rrn=rrn, method=logger_types.ERROR, message=f"{jv_request_meta.DOWNLOAD_JOURNAL_VOUCHER_REQUEST} - Caught something: {type(err).__name__} -> {err}")
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
        rrn = NO_ID if rrn is None else rrn
        loggerOutput(rrn=rrn, message=f"{jv_request_meta.DOWNLOAD_JOURNAL_VOUCHER_REQUEST} - DONE: {result}")
        if set(result) == set(error_model):
            return JsonResponse(result, status=result[STATUS_KEY])
        return result
    
