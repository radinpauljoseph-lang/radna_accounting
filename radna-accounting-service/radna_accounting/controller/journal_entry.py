import copy
from datetime import datetime
from radna_accounting.utils.decorators.error_handling import catchAndLog
from radna_accounting.configs.config import (
    logger_types,
    loggerOutput,
    engine,
    CONFIGS
)
from radna_accounting.configs.response_codes.mapping import (
    COA_CODE,
    TIS_CODE,
    ACP_CODE,
    JNE_CODE,
    MESSAGE_KEY,
    DETAILS_KEY,
    error_map
)
from radna_accounting.core.journal_entry.journal_entry import JournalEntryCore
from radna_accounting.core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
from radna_accounting.core.transaction_ids.transaction_ids import TransactionIdsCore
from radna_accounting.core.accounting_periods.accounting_periods import AccountingPeriodsCore
from radna_accounting.validators.journal_entry import JournalEntryModel
from radna_accounting.validators.data_model import DATA_KEY
from radna_accounting.models.transaction_ids import ti_meta
from radna_accounting.models.accounting_periods import (
    acp_meta,
    acp_status
)
from radna_accounting.models.journal_entry import (
    je_meta,
    je_status,
    je_types
)

class JournalEntryControllerMetaData:
    def __init__(self):
        self.JOURNAL_ENTRY_CONTROLLER = "JournalEntryController"
        self.CREATE_JOURNAL_ENTRY = "createJournalEntry"
        self.UPDATE_JOURNAL_ENTRY = "updateJournalEntry"
        self.DELETE_JOURNAL_ENTRY = "deleteJournalEntry"
        self.GET_JOURNAL_ENTRY = "getJournalEntry"
        self.GET_JOURNAL_ENTRY_BY_TRANSACTION_ID = "getJournalEntryByTransactionId"
        self.SET_TRANSACTION_ID_FOR_REVIEW = "setTransactionIdForReview"
        self.APPROVE_JOURNAL_ENTRY_BY_TRANSACTION_ID = "approveJournalEntryByTransactionId"
        self.REJECT_JOURNAL_ENTRY_BY_TRANSACTION_ID = "rejectJournalEntryByTransactionId"
        self.POST_JOURNAL_ENTRY_BY_TRANSACTION_ID = "postJournalEntryByTransactionId"
    
je_controller_meta = JournalEntryControllerMetaData()
class JournalEntryController:
    def __init__(self, rrn = None):
        self.__validator_model = JournalEntryModel
        self.__core_model = JournalEntryCore
        self.__coa_core_model = ChartOfAccountsCore
        self.__ti_core_model = TransactionIdsCore
        self.__acp_core_model = AccountingPeriodsCore
        self.__rrn = rrn

    @catchAndLog(Exception)
    def createJournalEntry(self, obj) -> dict:
        loggerOutput(rrn=self.__rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.CREATE_JOURNAL_ENTRY} - Start Creating Journal Entry")
        return_data = {}
        je_obj = copy.deepcopy(obj)
        je_obj[je_meta.STATUS] = je_status.NEW
        je_obj[je_meta.POSTING_DATE] = None

        je_obj = self.__validator_model(**je_obj)
        je_obj = je_obj.model_dump()

        core_model = self.__core_model(self.__rrn)
        coa_core_model = self.__coa_core_model(self.__rrn)
        ti_core_model = self.__ti_core_model(self.__rrn)
        acp_core_model = self.__acp_core_model(self.__rrn)
        
        account_number_exists = coa_core_model.selectRecordById(
            je_obj[je_meta.ACCOUNT_NUMBER]
        )

        if not account_number_exists:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}{COA_CODE}0101"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                account_id=je_obj[je_meta.ACCOUNT_NUMBER]
            )
            raise Exception(error)
            
        journal_entry_exists = core_model.selectRecordById(
            je_obj[je_meta.ID]
        )
        if not journal_entry_exists:
            record = copy.deepcopy(je_obj)

            # Add checking for Transaction ID here
            transaction_id_parts = ti_core_model.parseTransactionId(record[je_meta.TRANSACTION_ID])
            transaction_id_exists = ti_core_model.selectRecord(
                month=transaction_id_parts[ti_meta.MONTH],
                year=transaction_id_parts[ti_meta.YEAR],
                id=transaction_id_parts[ti_meta.ID]
            )
            if not transaction_id_exists:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0010"))
                raise Exception(error)
            
            journal_entries_filtered = core_model.selectRecordByTransactionId(record[je_meta.TRANSACTION_ID])
            if journal_entries_filtered is not None:
                journal_entries_filtered = journal_entries_filtered[DATA_KEY]
                valid_statuses = [je_status.NEW, je_status.REJECTED]
                
                for entry in journal_entries_filtered:
                    if entry[je_meta.STATUS] not in valid_statuses:
                        error = copy.deepcopy(error_map.get(f"{JNE_CODE}0010"))
                        raise Exception(error)
                
            # Add checking for Transaction Date here
            transaction_date = record[je_meta.TRANSACTION_DATE]
            
            if transaction_id_parts[ti_meta.MONTH] != transaction_date.month or transaction_id_parts[ti_meta.YEAR] != transaction_date.year:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0103"))
                raise Exception(error)
            
            accounting_period_data = acp_core_model.selectRecord(
                month=transaction_date.month,
                year=transaction_date.year
            )
            if not accounting_period_data:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}{ACP_CODE}0101"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    transaction_date=f"{transaction_date.year}-{transaction_date.month}-{transaction_date.day}"
                )
                raise Exception(error)
            
            accounting_period_data = accounting_period_data[DATA_KEY]
            if accounting_period_data[acp_meta.STATUS] == acp_status.CLOSED:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}{ACP_CODE}0102"))
                raise Exception(error)

            core_model.insertRecord(record)

            record = core_model.selectRecordById(record[je_meta.ID])

            current_transaction_id = ti_core_model.selectCurrentId(
                month=transaction_id_parts[ti_meta.MONTH],
                year=transaction_id_parts[ti_meta.YEAR]
            )[DATA_KEY]

            if transaction_id_parts[ti_meta.ID] == current_transaction_id[ti_meta.ID]:
                transaction_id_parts[ti_meta.ID] = str(int(transaction_id_parts[ti_meta.ID]) + 1).zfill(5)
                ti_core_model.insertRecord(transaction_id_parts)
            return_data = record
        else:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0102"))
            raise Exception(error)
        loggerOutput(rrn=self.__rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.CREATE_JOURNAL_ENTRY} - Done Creating Journal Entry")
        return return_data
    
    @catchAndLog(Exception)
    def getJournalEntry(self, id: str) -> dict:
        return_data = {}
        core_model = self.__core_model(self.__rrn)
        loggerOutput(rrn=self.__rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.GET_JOURNAL_ENTRY} - Start Get Journal Entry Record")  
        record = core_model.selectRecordById(id)
        if record is not None:
            return_data = record
        else:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0026"))
            raise Exception(error)
        loggerOutput(rrn=self.__rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.GET_JOURNAL_ENTRY} - Done Get Journal Entry Record")  
        return return_data

    @catchAndLog(Exception)
    def getJournalEntryByTransactionId(self, transaction_id: str) -> dict:
        return_data = {}
        core_model = self.__core_model(self.__rrn)
        loggerOutput(rrn=self.__rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.GET_JOURNAL_ENTRY_BY_TRANSACTION_ID} - Start Get Journal Entry Record By Transaction ID")  
        record = core_model.selectRecordByTransactionId(transaction_id)
        if record is not None:
            return_data = record
        else:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0028"))
            raise Exception(error)
        loggerOutput(rrn=self.__rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.GET_JOURNAL_ENTRY_BY_TRANSACTION_ID} - Done Get Journal Entry Record By Transaction ID")  
        return return_data
    
    @catchAndLog(Exception)
    def getTransactionIdCreditDebitAmount(self, transaction_id: str) -> dict:
        return_data = {}
        core_model = self.__core_model(self.__rrn)
        loggerOutput(rrn=self.__rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.GET_JOURNAL_ENTRY} - Start Get Transaction ID Credit & Debit Amount: {transaction_id}")  
        return_data = core_model.getTransactionIdAmount(transaction_id)
        loggerOutput(rrn=self.__rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.GET_JOURNAL_ENTRY} - Done Get Transaction ID Credit & Debit Amount: {transaction_id}")  
        return return_data
    
    @catchAndLog(Exception)
    def setTransactionIdForReview(self, transaction_id: str) -> dict:
        return_data = {}
        valid_statuses = [je_status.NEW, je_status.REJECTED]
        core_model = self.__core_model(self.__rrn)
        error_details = []
        counter = core_model.getTransactionIdAmount(transaction_id)

        if counter[je_types.CREDIT] == counter[je_types.DEBIT]:
            query_result = core_model.selectRecordByTransactionId(transaction_id)
            result = query_result[DATA_KEY]
            
            # Add checking for transaction date (all JE records with same transaction IDs must have the same transaction dates)
            first_value = result[0].get(je_meta.TRANSACTION_DATE)
            transaction_dates_equal =  all(item.get(je_meta.TRANSACTION_DATE) == first_value for item in result)

            if not transaction_dates_equal:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0108"))
                error_details.append(error)
                
            for data in result:
                if data[je_meta.STATUS] == je_status.FOR_REVIEW:
                    error = copy.deepcopy(error_map.get(f"{JNE_CODE}0107"))
                    error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                        id=data[je_meta.ID]
                    )
                    error_details.append(error[MESSAGE_KEY])

                elif data[je_meta.STATUS] not in valid_statuses:
                    error = copy.deepcopy(error_map.get(f"{JNE_CODE}0105"))
                    error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                        id=data[je_meta.ID],
                        status=data[je_meta.STATUS]
                    )
                    error_details.append(error[MESSAGE_KEY])
                else:
                    loggerOutput(
                        rrn=self.__rrn,
                        message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.SET_TRANSACTION_ID_FOR_REVIEW} No issue with Journal Entries"
                    )

            if len(error_details) == 0:
                core_model.updateRecordStatusByTransactionId(
                    transaction_id=transaction_id,
                    status=je_status.FOR_REVIEW
                )
                query_result = core_model.selectRecordByTransactionId(transaction_id)
                return_data = query_result
            else:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0104"))
                loggerOutput(
                    rrn=self.__rrn,
                    message=f"{error}"
                )
                error[DETAILS_KEY] = error_details
                raise Exception(error)
        else:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0106"))
            raise Exception(error)
        
        return return_data

    @catchAndLog(Exception)
    def updateJournalEntry(self, id: str, obj: dict) -> dict:
        loggerOutput(rrn=self.__rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.UPDATE_JOURNAL_ENTRY} - Start Updating Journal Entry")
        return_data = {}
        allowed_fields = [
            je_meta.CURRENCY_CODE,
            je_meta.ACCOUNT_NUMBER,
            je_meta.ENTRY_TYPE,
            je_meta.DESCRIPTION,
            je_meta.AMOUNT
        ]
        valid_statuses = [je_status.NEW, je_status.REJECTED]
        core_model = self.__core_model(self.__rrn)
        coa_core_model = self.__coa_core_model(self.__rrn)

        je_id_exists = core_model.selectRecordById(id)

        for key in obj.keys():
            if key not in allowed_fields:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0109"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    key=key
                )
                raise Exception(error)
                
        if not je_id_exists:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0026"))
            raise Exception(error)
        
        data = je_id_exists[DATA_KEY]

        if data[je_meta.STATUS] not in valid_statuses:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0110"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                id=data[je_meta.ID],
                status=data[je_meta.STATUS]
            )
            raise Exception(error)
        
        temp_obj = copy.deepcopy(obj)
        temp_obj[je_meta.ID] = id
        temp_obj[je_meta.STATUS] = data[je_meta.STATUS]
        temp_obj[je_meta.TRANSACTION_ID] = data[je_meta.TRANSACTION_ID]
        temp_obj[je_meta.TRANSACTION_DATE] = data[je_meta.TRANSACTION_DATE]
        je_obj = self.__validator_model(**temp_obj)
        je_obj = je_obj.model_dump()

        account_number_exists = coa_core_model.selectRecordById(
            je_obj[je_meta.ACCOUNT_NUMBER]
        )
        
        if not account_number_exists:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}{COA_CODE}0101"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                account_id=je_obj[je_meta.ACCOUNT_NUMBER]
            )
            raise Exception(error)
        
        core_model.updateRecordById(id, je_obj)
        record = core_model.selectRecordById(id)
        return_data = record

        loggerOutput(rrn=self.__rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.UPDATE_JOURNAL_ENTRY} - Done Updating Journal Entry")

        return return_data
    
    @catchAndLog(Exception)
    def deleteJournalEntry(self, id: str):
        loggerOutput(rrn=self.__rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.DELETE_JOURNAL_ENTRY} - Start Delete Journal Entry")
        return_data = {}
        valid_statuses = [je_status.NEW, je_status.REJECTED]
        core_model = self.__core_model(self.__rrn)

        je_id_exists = core_model.selectRecordById(id)
                
        if not je_id_exists:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0026"))
            raise Exception(error)
        
        data = je_id_exists[DATA_KEY]
        if data[je_meta.STATUS] not in valid_statuses:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0110"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                id=data[je_meta.ID],
                status=data[je_meta.STATUS]
            )
            raise Exception(error)
        
        data[je_meta.STATUS] = je_status.DELETED
        core_model.deleteRecordById(id)
        return_data = data

        loggerOutput(rrn=self.__rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.DELETE_JOURNAL_ENTRY} - Done Delete Journal Entry")

        return return_data
    
    @catchAndLog(Exception)
    def approveJournalEntryByTransactionId(self, transaction_id: str) -> dict:
        loggerOutput(rrn=self.__rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.APPROVE_JOURNAL_ENTRY_BY_TRANSACTION_ID} - Start Approving Journal Entry By Transaction ID")
        return_data = {}
        core_model = self.__core_model(rrn=self.__rrn)
        valid_statuses = [je_status.FOR_REVIEW]
        error_details = []
        query_result = core_model.selectRecordByTransactionId(transaction_id)

        if len(query_result[DATA_KEY]) == 0:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0010"))
            raise Exception(error)
        
        result = query_result[DATA_KEY]
        for data in result:
            if data[je_meta.STATUS] == je_status.APPROVED:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0111"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    id=data[je_meta.ID]
                )
                error_details.append(error[MESSAGE_KEY])

            elif data[je_meta.STATUS] not in valid_statuses:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0112"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    id=data[je_meta.ID],
                    status=data[je_meta.STATUS]
                )
                error_details.append(error[MESSAGE_KEY])
            else:
                loggerOutput(
                    rrn=self.__rrn,
                    message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.APPROVE_JOURNAL_ENTRY_BY_TRANSACTION_ID} No issue with Journal Entries"
                )

        if len(error_details) == 0:
            core_model.updateRecordStatusByTransactionId(
                transaction_id=transaction_id,
                status=je_status.APPROVED
            )
            query_result = core_model.selectRecordByTransactionId(transaction_id)
            return_data = query_result
        else:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0113"))
            loggerOutput(
                rrn=self.__rrn,
                message=f"{error}"
            )
            error[DETAILS_KEY] = error_details
            raise Exception(error)
        
        return return_data

    @catchAndLog(Exception)
    def rejectJournalEntryByTransactionId(self, transaction_id: str) -> dict:
        loggerOutput(rrn=self.__rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.REJECT_JOURNAL_ENTRY_BY_TRANSACTION_ID} - Start Rejecting Journal Entry By Transaction ID")
        return_data = {}
        core_model = self.__core_model(rrn=self.__rrn)
        valid_statuses = [je_status.FOR_REVIEW]
        error_details = []
        query_result = core_model.selectRecordByTransactionId(transaction_id)

        if len(query_result[DATA_KEY]) == 0:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0010"))
            raise Exception(error)
        
        result = query_result[DATA_KEY]
        for data in result:
            if data[je_meta.STATUS] == je_status.REJECTED:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0114"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    id=data[je_meta.ID]
                )
                error_details.append(error[MESSAGE_KEY])

            elif data[je_meta.STATUS] not in valid_statuses:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0115"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    id=data[je_meta.ID],
                    status=data[je_meta.STATUS]
                )
                error_details.append(error[MESSAGE_KEY])
            else:
                loggerOutput(
                    rrn=self.__rrn,
                    message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.REJECT_JOURNAL_ENTRY_BY_TRANSACTION_ID} No issue with Journal Entries"
                )

        if len(error_details) == 0:
            core_model.updateRecordStatusByTransactionId(
                transaction_id=transaction_id,
                status=je_status.REJECTED
            )
            query_result = core_model.selectRecordByTransactionId(transaction_id)
            return_data = query_result
        else:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0116"))
            loggerOutput(
                rrn=self.__rrn,
                message=f"{error}"
            )
            error[DETAILS_KEY] = error_details
            raise Exception(error)
        
        return return_data
    
    @catchAndLog(Exception)
    def postJournalEntryByTransactionId(self, transaction_id: str) -> dict:
        loggerOutput(rrn=self.__rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.POST_JOURNAL_ENTRY_BY_TRANSACTION_ID} - Start Posting Journal Entry By Transaction ID")
        return_data = {}
        core_model = self.__core_model(rrn=self.__rrn)
        valid_statuses = [je_status.APPROVED]
        error_details = []
        query_result = core_model.selectRecordByTransactionId(transaction_id)

        if len(query_result[DATA_KEY]) == 0:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0010"))
            raise Exception(error)
        
        result = query_result[DATA_KEY]
        for data in result:
            if data[je_meta.STATUS] == je_status.REJECTED:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0117"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    id=data[je_meta.ID]
                )
                error_details.append(error[MESSAGE_KEY])

            elif data[je_meta.STATUS] not in valid_statuses:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0118"))
                error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                    id=data[je_meta.ID],
                    status=data[je_meta.STATUS]
                )
                error_details.append(error[MESSAGE_KEY])
            else:
                loggerOutput(
                    rrn=self.__rrn,
                    message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.POST_JOURNAL_ENTRY_BY_TRANSACTION_ID} No issue with Journal Entries"
                )

        if len(error_details) == 0:
            core_model.postRecordsByTransactionId(transaction_id)
            query_result = core_model.selectRecordByTransactionId(transaction_id)
            return_data = query_result
        else:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0119"))
            loggerOutput(
                rrn=self.__rrn,
                message=f"{error}"
            )
            error[DETAILS_KEY] = error_details
            raise Exception(error)
        
        return return_data

