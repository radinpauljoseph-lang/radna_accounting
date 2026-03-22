import copy
from datetime import datetime
from django.http import HttpResponse
from ..utils.decorators.error_handling import catchAndLog
from ..configs.config import (
    logger_types,
    loggerOutput,
    engine
)
from ..models.journal_entry import je_types
from ..configs.response_codes.mapping import (
    COA_CODE,
    JNE_CODE,
    JNV_CODE,
    MESSAGE_KEY,
    DETAILS_KEY,
    error_map
)
from ..models.chart_of_accounts import coa_meta
from ..models.journal_voucher import jv_meta
from ..models.journal_entry import je_meta
from ..core.journal_voucher.journal_voucher import JournalVoucherCore
from ..core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
from ..core.journal_entry.journal_entry import JournalEntryCore
from ..validators.journal_voucher import (
    JournalVoucherModel,
    JournalVoucherDocumentDataMetaData,
    JournalVoucherDocumentDataModel
)
from ..validators.data_model import DATA_KEY

class JournalEntryControllerMetaData:
    def __init__(self):
        self.JOURNAL_VOUCHER_CONTROLLER = "JournalVoucherController"
        self.CREATE_JOURNAL_VOUCHER = "createJournalVoucher"

jv_controller_meta = JournalEntryControllerMetaData()

class JournalVoucherController:
    def __init__(self, rrn = None):
        self.validator_model = JournalVoucherModel
        self.engine = engine
        self.core_model = JournalVoucherCore
        self.coa_core_model = ChartOfAccountsCore
        self.je_core_model = JournalEntryCore
        self.rrn = rrn

    @catchAndLog(Exception)
    def createJournalVoucher(self, transaction_id: str) -> dict:
        loggerOutput(rrn=self.rrn, message=f"{jv_controller_meta.JOURNAL_VOUCHER_CONTROLLER}.{jv_controller_meta.CREATE_JOURNAL_VOUCHER} - Start Creating Journal Voucher")
        return_data = {}
        ACCOUNT_NAME = 'account_name'

        core_model = self.core_model()
        je_core_model = self.je_core_model(rrn=self.rrn)
        coa_core_model = self.coa_core_model(rrn=self.rrn)

        journal_entries = je_core_model.selectRecordByTransactionId(transaction_id)
        
        if len(journal_entries[DATA_KEY]) == 0:
            error = copy.deepcopy(error_map.get(f"{JNV_CODE}{JNE_CODE}0028"))
            del core_model
            del je_core_model
            del coa_core_model
            raise Exception(error)
        
        journal_entries = journal_entries[DATA_KEY]

        for entry in journal_entries:
            account_details = coa_core_model.selectRecordById(entry[je_meta.ACCOUNT_NUMBER])
            if account_details is None:
                error = copy.deepcopy(error_map.get(f"{JNV_CODE}{COA_CODE}0101"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    account_id=entry[je_meta.ACCOUNT_NUMBER]
                )
                del core_model
                del je_core_model
                del coa_core_model
                raise Exception(error)
            account_details = account_details[DATA_KEY]
            entry[ACCOUNT_NAME] = account_details[coa_meta.NAME]
        
        credit_debit_details = je_core_model.getTransactionIdAmount(transaction_id)

        transaction_date = journal_entries[0][je_meta.TRANSACTION_DATE].strftime("%Y-%m-%d")
        currency_code = journal_entries[0][je_meta.CURRENCY_CODE]
        credit_total = credit_debit_details[je_types.CREDIT]
        debit_total = credit_debit_details[je_types.DEBIT]

        content = JournalVoucherDocumentDataModel(
            transactionDate=transaction_date,
            currencyCode=currency_code,
            creditTotal=credit_total,
            debitTotal=debit_total,
            journalEntry=journal_entries
        ).model_dump()

        core_model.insertRecord(transaction_id, content)
        
        record = core_model.selectRecordByTransactionId(transaction_id)
        return_data = record
        loggerOutput(rrn=self.rrn, message=f"{jv_controller_meta.JOURNAL_VOUCHER_CONTROLLER}.{jv_controller_meta.CREATE_JOURNAL_VOUCHER} - Done Creating Journal Voucher")
        return return_data
    
    @catchAndLog(Exception)
    def downloadJournalVoucherFile(self, transaction_id):
        core_model = self.core_model()
        result = core_model.selectRecordByTransactionId(transaction_id)
        result = result[DATA_KEY]
        if len(result) == 0:
            error = copy.deepcopy(error_map.get(f"{JNV_CODE}0101"))
            raise Exception(error)
        
        result = result[0]
        file_name = f"{result[jv_meta.DOCUMENT_NAME]}.{result[jv_meta.DOCUMENT_FILE_TYPE]}"
        target_file = f"{result[jv_meta.DOCUMENT_PATH]}\\{file_name}"
        with open(target_file, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/pdf")
            response["Content-Disposition"] = "attachment; filename=\"{file_name}\""
            return response
        # return FileResponse(
        #     open(target_file, "rb"),
        #     as_attachment=True,
        #     filename=file_name
        # )
        
