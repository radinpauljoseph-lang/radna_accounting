import copy
from datetime import datetime
from ..utils.decorators.error_handling import catchAndLog
from ..configs.config import (
    logger_types,
    loggerOutput,
    engine
)
from ..configs.response_codes.mapping import (
    COA_CODE,
    TIS_CODE,
    ACP_CODE,
    JNE_CODE,
    MESSAGE_KEY,
    DETAILS_KEY,
    error_map
)
from ..core.journal_entry.journal_entry import JournalEntryCore
from ..core.chart_of_accounts.chart_of_accounts import ChartOfAccountsCore
from ..core.transaction_ids.transaction_ids import TransactionIdsCore
from ..core.accounting_periods.accounting_periods import AccountingPeriodsCore
from ..validators.journal_entry import JournalEntryModel
from ..validators.data_model import DATA_KEY
from ..models.transaction_ids import ti_meta
from ..models.accounting_periods import (
    acp_meta,
    acp_status
)
from ..models.journal_entry import (
    je_meta,
    je_status,
    je_types
)

class JournalEntryControllerMetaData:
    def __init__(self):
        self.JOURNAL_ENTRY_CONTROLLER = "JournalEntryController"
        self.CREATE_JOURNAL_ENTRY = "createJournalEntry"
        self.UPDATE_JOURNAL_ENTRY = "updateJournalEntry"
        self.GET_JOURNAL_ENTRY = "getJournalEntry"
        self.GET_JOURNAL_ENTRY_BY_TRANSACTION_ID = "getJournalEntryByTransactionId"
        self.SET_TRANSACTION_ID_FOR_REVIEW = "setTransactionIdForReview"
    
je_controller_meta = JournalEntryControllerMetaData()
class JournalEntryController:
    def __init__(self, rrn = None):
        self.validator_model = JournalEntryModel
        self.engine = engine
        self.core_model = JournalEntryCore
        self.coa_core_model = ChartOfAccountsCore
        self.ti_core_model = TransactionIdsCore
        self.acp_core_model = AccountingPeriodsCore
        self.rrn = rrn

    @catchAndLog(Exception)
    def createJournalEntry(self, obj) -> dict:
        loggerOutput(rrn=self.rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.CREATE_JOURNAL_ENTRY} - Start Creating Journal Entry")
        return_data = {}
        je_obj = copy.deepcopy(obj)
        je_obj[je_meta.STATUS] = je_status.NEW
        je_obj[je_meta.POSTING_DATE] = None

        je_obj = self.validator_model(**je_obj)
        je_obj = je_obj.model_dump()

        core_model = self.core_model(self.rrn)
        coa_core_model = self.coa_core_model(self.rrn)
        ti_core_model = self.ti_core_model(self.rrn)
        acp_core_model = self.acp_core_model(self.rrn)
        
        account_number_exists = coa_core_model.selectRecordById(
            je_obj[je_meta.ACCOUNT_NUMBER]
        )

        if not account_number_exists:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}{COA_CODE}0101"))
            error[MESSAGE_KEY] = error[MESSAGE_KEY].format(
                account_id=je_obj[je_meta.ACCOUNT_NUMBER]
            )
            del core_model
            del coa_core_model
            del core_model
            del coa_core_model
            del ti_core_model
            del acp_core_model
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
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}{TIS_CODE}0103"))
                del core_model
                del coa_core_model
                del ti_core_model
                del acp_core_model
                raise Exception(error)
            # Add checking for Transaction Date here
            transaction_date = record[je_meta.TRANSACTION_DATE]
            
            if transaction_id_parts[ti_meta.MONTH] != transaction_date.month or transaction_id_parts[ti_meta.YEAR] != transaction_date.year:
                error = copy.deepcopy(error_map.get(f"{JNE_CODE}0103"))
                del core_model
                del coa_core_model
                del ti_core_model
                del acp_core_model
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
                del core_model
                del coa_core_model
                del ti_core_model
                del acp_core_model
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
            del core_model
            del coa_core_model
            del ti_core_model
            del acp_core_model
            raise Exception(error)
        loggerOutput(rrn=self.rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.CREATE_JOURNAL_ENTRY} - Done Creating Journal Entry")
        del core_model
        del coa_core_model
        del ti_core_model
        del acp_core_model
        return return_data
    
    @catchAndLog(Exception)
    def getJournalEntry(self, id: str) -> dict:
        return_data = {}
        core_model = self.core_model(self.rrn)
        loggerOutput(rrn=self.rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.GET_JOURNAL_ENTRY} - Start Get Journal Entry Record")  
        record = core_model.selectRecordById(id)
        if record is not None:
            return_data = record
        else:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0026"))
            del core_model
            raise Exception(error)
        loggerOutput(rrn=self.rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.GET_JOURNAL_ENTRY} - Done Get Journal Entry Record")  
        del core_model
        return return_data

    @catchAndLog(Exception)
    def getJournalEntryByTransactionId(self, transaction_id: str) -> dict:
        return_data = {}
        core_model = self.core_model(self.rrn)
        loggerOutput(rrn=self.rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.GET_JOURNAL_ENTRY_BY_TRANSACTION_ID} - Start Get Journal Entry Record By Transaction ID")  
        record = core_model.selectRecordByTransactionId(transaction_id)
        if record is not None:
            return_data = record
        else:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0028"))
            del core_model
            raise Exception(error)
        loggerOutput(rrn=self.rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.GET_JOURNAL_ENTRY_BY_TRANSACTION_ID} - Done Get Journal Entry Record By Transaction ID")  
        del core_model
        return return_data
    
    @catchAndLog(Exception)
    def getTransactionIdCreditDebitAmount(self, transaction_id: str) -> dict:
        return_data = {}
        core_model = self.core_model(self.rrn)
        loggerOutput(rrn=self.rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.GET_JOURNAL_ENTRY} - Start Get Transaction ID Credit & Debit Amount: {transaction_id}")  
        return_data = core_model.getTransactionIdAmount(transaction_id)
        loggerOutput(rrn=self.rrn, message=f"{je_controller_meta.JOURNAL_ENTRY_CONTROLLER}.{je_controller_meta.GET_JOURNAL_ENTRY} - Done Get Transaction ID Credit & Debit Amount: {transaction_id}")  
        del core_model
        return return_data
    
    @catchAndLog(Exception)
    def setTransactionIdForReview(self, transaction_id: str) -> dict:
        return_data = {}
        valid_statuses = [je_status.NEW, je_status.REJECTED]
        core_model = self.core_model(self.rrn)
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
                        rrn=self.rrn,
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
                    rrn=self.rrn,
                    message=f"{error}"
                )
                error[DETAILS_KEY] = error_details
                raise Exception(error)
        else:
            error = copy.deepcopy(error_map.get(f"{JNE_CODE}0106"))
            del core_model
            raise Exception(error)
        
        return return_data

    # def create_journal_entry(self, obj) -> dict:
    #     return_data = {}
    #     is_accounting_period_exists = False
    #     is_accounting_period_open = False
    #     is_transaction_id_exists = False
    #     try:
    #         je_obj = self.validator_model(**obj)
    #         je_obj = je_obj.model_dump()
    #         je_obj['id'] = uuid.uuid4()
    #         je_obj['status'] ="UNPOSTED"
    #         transaction_id = je_obj['transaction_id']
    #         transaction_id_entry_number = transaction_id.split("-")[1]
    #         transaction_id_month_year = transaction_id.split("-")[0]
    #         transaction_date_month = je_obj['transaction_date'].month
    #         transaction_date_year = je_obj['transaction_date'].year
            
    #         je_exists = je_record_value_validate(self.engine, 'id', je_obj['id'])
    #         accounting_periods = accounting_period_select_all_account_records(self.engine)
    #         if accounting_periods.shape[0] > 0:
    #             accounting_periods = accounting_periods[accounting_periods['year'] == transaction_date_year]
    #             if accounting_periods.shape[0] > 0:
    #                 accounting_periods = accounting_periods[accounting_periods['month'] == transaction_date_month]
    #         is_accounting_period_exists = True if accounting_periods.shape[0] == 1 else False
            
    #         if is_accounting_period_exists:
    #             accounting_periods = accounting_periods[accounting_periods['status'] == 'OPEN']
    #         is_accounting_period_open = True if accounting_periods.shape[0] == 1 else False

    #         transaction_ids_df = transaction_ids_select_by_month_year_record(engine, transaction_date_month, transaction_date_year)
    #         if transaction_ids_df.shape[0] > 0:
    #             transaction_ids_df = transaction_ids_df[transaction_ids_df['year'] == transaction_date_year]
    #             if transaction_ids_df.shape[0] > 0:
    #                 transaction_ids_df = transaction_ids_df[transaction_ids_df['month'] == transaction_date_month]
    #                 if transaction_ids_df.shape[0] > 0:
    #                     transaction_ids_df = transaction_ids_df[transaction_ids_df['id'] == transaction_id_entry_number]
    #                     is_transaction_id_exists = True if (transaction_ids_df.shape[0] == 1 and transaction_id_month_year == f"{transaction_date_year}{transaction_date_month:02}") else False

    #         if not je_exists:
    #             record = copy.deepcopy(je_obj)
    #             del record['created_date']
    #             del record['updated_date']

    #             if not is_accounting_period_exists:
    #                 raise Exception(f"create_journal_entry - Accounting Period {transaction_date_month:02}-{transaction_date_year} does not exist")
    #             if not is_accounting_period_open:
    #                 raise Exception(f"create_journal_entry - Accounting Period {transaction_date_month:02}-{transaction_date_year} is already closed")
    #             if not is_transaction_id_exists:
    #                 raise Exception(f"create_journal_entry - Transaction ID {transaction_id} does not exist or does not align with the transaction date used")
                
    #             account_numbers = account_select_all_account_records(self.engine)
    #             account_numbers_filtered = account_numbers[account_numbers['account_id'] == record['account_number']]
    #             is_account_number_exists = True if account_numbers_filtered.shape[0] == 1 else False
    #             if not is_account_number_exists:
    #                 raise Exception("create_journal_entry - account number does not exist")
                
    #             je_records = je_select_by_transaction_id_record(self.engine, transaction_id)
    #             if je_records.shape[0] > 0:
    #                 je_records = je_records[je_records['status'] == "POSTED"]
    #                 if je_records.shape[0] > 0:
    #                     raise Exception(f"create_journal_entry - Transaction ID already posted")
                
    #             je_insert_record(self.engine, record)
    #             new_transaction_id_validator = transaction_ids_select_by_month_year_record(engine, transaction_date_month, transaction_date_year)
    #             if int(transaction_id_entry_number) == new_transaction_id_validator.shape[0]:
    #                 new_entry_number = int(transaction_id_entry_number) + 1
    #                 new_entry_number = f"{new_entry_number:05}"
    #                 transaction_ids_record = self.transaction_ids_model(
    #                     month=transaction_date_month,
    #                     year=transaction_date_year,
    #                     id=new_entry_number
    #                 ).model_dump()
    #                 transaction_ids_insert_record(self.engine, transaction_ids_record)
                    
    #             record = je_select_record(self.engine, record['id'])
    #             loggerOutput(message=record)
    #             record = self.validator_model(**record)
    #             record = record.model_dump()
    #             return_data = {
    #                 "data": record
    #             }
    #             loggerOutput(message=f"create_journal_entry - {return_data}")
    #         else:
    #             return_data = {
    #                 "error": "create_journal_entry - Journal Entry already exists"
    #             }
    #     except TypeError as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"create_journal_entry - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     except BaseException as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"create_journal_entry - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     finally:
    #         loggerOutput(message=f"DONE: create_journal_entry - {return_data}")
    #         return return_data
    
    # def update_journal_entry(self, id, obj) -> dict:
    #     return_data = {}
    #     try:
    #         record = je_select_record(self.engine, id)
    #         if record:
    #             je_obj = self.validator_model(**record)
    #             je_obj = je_obj.model_dump()
    #             allowed_fields = [
    #                 'transaction_date',
    #                 'account_number',
    #                 'description',
    #                 'entry_type',
    #                 'amount'
    #             ]
    #             account_numbers = account_select_all_account_records(self.engine)
    #             account_numbers_filtered = account_numbers[account_numbers['account_id'] == record['account_number']]
    #             is_account_number_exists = True if account_numbers_filtered.shape[0] == 1 else False
    #             if not is_account_number_exists:
    #                 raise Exception("update_journal_entry - account number does not exist")
                
    #             if record['status'] != "UNPOSTED":
    #                 return_data = {
    #                         "error": f"update_journal_entry - Journal Entry already posted"
    #                     }
    #                 raise Exception(f"update_journal_entry - Journal Entry already posted")
                
    #             for key in obj.keys():
    #                 je_obj[key] = obj[key]
                    
    #             record = self.validator_model(**je_obj)
    #             record = record.model_dump()
    #             for key in obj.keys():
    #                 if key not in allowed_fields:
    #                     return_data = {
    #                         "error": f"update_journal_entry - {key} field not allowed"
    #                     }
    #                     raise Exception(f"update_journal_entry - {key} field not allowed")
                    
    #             now = datetime.now()
    #             now = now.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(now.microsecond/1000):03d}"
    #             record['updated_date'] = now
    #             for key in je_obj.keys():
    #                 if key in allowed_fields:
    #                     record[key] = je_obj[key]
                
    #             je_update_record(self.engine, id, record)
    #             record = je_select_record(self.engine, id)
    #             record = self.validator_model(**record)
    #             record = record.model_dump()

    #             return_data = {
    #                 "data": record
    #             }
    #             loggerOutput(message=f"update_journal_entry - {return_data}")
    #         else:
    #             return_data = {
    #                 "error": "update_journal_entry - Journal Entry ID Not Found"
    #             }
    #     except TypeError as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"update_journal_entry - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     except ValueError as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"update_journal_entry - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     except BaseException as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"update_journal_entry - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     finally:
    #         loggerOutput(message=f"DONE: update_journal_entry - {return_data}")
    #         return return_data

    # def post_journal_entry_by_transaction_id(self, id) -> dict:
    #     return_data = {}
    #     try:
    #         record = je_select_by_transaction_id_record(self.engine, id)
    #         if record.shape[0] > 0:
    #             unposted_record_filter = record[record['status'] == "UNPOSTED"]
    #             if unposted_record_filter.shape[0] == 0:
    #                 return_data = {
    #                     "error": f"post_journal_entry_by_transaction_id - Journal Entry already posted"
    #                 }
    #             else:
    #                 credit_je_records = record[record['entry_type'] == "CREDIT"]
    #                 debit_je_records = record[record['entry_type'] == "DEBIT"]
    #                 if credit_je_records.shape[0] == 0 or debit_je_records.shape[0] == 0:
    #                     return_data = {
    #                         "error": f"post_journal_entry_by_transaction_id - Journal Entry Transaction ID {id} has either no debit or credit record"
    #                     }
    #                 else:
    #                     credit_sum = credit_je_records.sum()
    #                     debit_sum = debit_je_records.sum()
    #                     if credit_sum == debit_sum:
    #                         je_update_to_post_record(self.engine, id)
    #                         return_data = {
    #                             "error": f"post_journal_entry_by_transaction_id - Journal Entry Transaction ID {id} have unbalanced amounts"
    #                         }
    #                     else:
    #                         return_data = {
    #                             "error": f"post_journal_entry_by_transaction_id - Journal Entry Transaction ID {id} have unbalanced amounts"
    #                         }
    #                 je_update_to_post_record(self.engine, id)
                
    #                 record = je_select_by_transaction_id_record(self.engine, id, record)

    #                 return_data = {
    #                     "data": record.to_dict()
    #                 }
    #                 loggerOutput(message=f"post_journal_entry_by_transaction_id - {return_data}")
    #         else:
    #             return_data = {
    #                 "error": "post_journal_entry_by_transaction_id - Journal Entry Transaction ID Not Found"
    #             }
    #     except TypeError as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"post_journal_entry_by_transaction_id - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     except ValueError as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"post_journal_entry_by_transaction_id - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     except BaseException as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"post_journal_entry_by_transaction_id - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     finally:
    #         loggerOutput(message=f"DONE: post_journal_entry_by_transaction_id - {return_data}")
    #         return return_data
        
    # def post_journal_entry_by_month_year(self, month, year) -> dict:
    #     return_data = {}
    #     try:
    #         record = je_select_by_transaction_date_month_year_record(self.engine, month, year)
    #         if record.shape[0] > 0:
    #             unposted_record_filter = record[record['status'] == "UNPOSTED"]
    #             if unposted_record_filter.shape[0] == 0:
    #                 return_data = {
    #                     "error": f"post_journal_entry_by_month_year - Journal Entry already posted"
    #                 }
    #             else:
    #                 transaction_ids = record['transaction_id'].unique()
    #                 loggerOutput(message="@@@@@@@@@@@@@@@@@")
    #                 loggerOutput(message=transaction_ids)
    #                 loggerOutput(message="@@@@@@@@@@@@@@@@@")
    #                 # record = je_select_by_transaction_date_month_year_record(self.engine, month, year)
    #                 for index in range(len(transaction_ids)):
    #                     loggerOutput(message="@@@@@@@@@@@@@@@@@")
    #                     loggerOutput(message=transaction_ids[index])
    #                     loggerOutput(message="@@@@@@@@@@@@@@@@@")
    #                     filtered_records = record[record['transaction_id'] == transaction_ids[index]]
    #                     credit_je_records = filtered_records[filtered_records['entry_type'] == 'CREDIT']
    #                     debit_je_records = filtered_records[filtered_records['entry_type'] == 'DEBIT']
    #                     if credit_je_records.shape[0] == 0 or debit_je_records.shape[0] == 0:
    #                         return_data = {
    #                             "error": f"post_journal_entry_by_month_year - Journal Entry Transaction IDs by month & year has either no debit or credit record"
    #                         }
    #                         raise Exception(f"post_journal_entry_by_month_year - Journal Entry Transaction IDs by month & year has either no debit or credit record")
    #                     else:
    #                         credit_sum = credit_je_records['amount'].sum()
    #                         debit_sum = debit_je_records['amount'].sum()
    #                         if credit_sum != debit_sum:
    #                             return_data = {
    #                                 "error": f"post_journal_entry_by_month_year - Journal Entry Transaction IDs by month & year have unbalanced amounts"
    #                             }
    #                             raise Exception(f"post_journal_entry_by_month_year - Journal Entry Transaction IDs by month & year have unbalanced amounts")
    #                 je_update_to_post_by_month_year_record(self.engine, month, year)
                        
    #                 record = je_select_by_transaction_date_month_year_record(self.engine, month, year)

    #                 return_data = {
    #                     "data": record.to_dict()
    #                 }
    #                 loggerOutput(message=f"post_journal_entry_by_month_year - {return_data}")
    #         else:
    #             return_data = {
    #                 "error": "post_journal_entry_by_month_year - Journal Entry Transaction IDs by given month & year Not Found"
    #             }
    #     except TypeError as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"post_journal_entry_by_month_year - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     except ValueError as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"post_journal_entry_by_month_year - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     except BaseException as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"post_journal_entry_by_month_year - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     finally:
    #         loggerOutput(message=f"DONE: post_journal_entry_by_month_year - {return_data}")
    #         return return_data
        
    
    
    # def get_journal_entry(self, id) -> dict:
    #     return_data = {}
    #     try:
    #         record = je_select_record(self.engine,id)
    #         if record:
    #             return_data = {
    #                 "data": record
    #             }
    #             loggerOutput(message=f"get_journal_entry - {return_data}")
    #         else:
    #             return_data = {
    #                 "error": "get_journal_entry - Journal Entry ID Not Found"
    #             }
    #     except TypeError as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"get_journal_entry - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     except BaseException as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"get_journal_entry - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     finally:
    #         loggerOutput(message=f"DONE: get_journal_entry - {return_data}")
    #         return return_data
        
    # def get_journal_entry_by_transaction_id(self, id) -> dict:
    #     return_data = {}
    #     try:
    #         record = je_select_by_transaction_id_record(self.engine,id)
    #         if record.shape[0] > 0:
    #             return_data = {
    #                 "data": record.to_dict()
    #             }
    #             loggerOutput(message=f"get_journal_entry_by_transaction_id - {return_data}")
    #         else:
    #             return_data = {
    #                 "error": "get_journal_entry_by_transaction_id - Transaction ID Not Found"
    #             }
    #     except TypeError as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"get_journal_entry_by_transaction_id - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     except BaseException as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"get_journal_entry_by_transaction_id - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     finally:
    #         loggerOutput(message=f"DONE: get_journal_entry_by_transaction_id - {return_data}")
    #         return return_data

    # def delete_journal_entry_by_transaction_id(self, id) -> dict:
    #     return_data = {}
    #     try:
    #         record = je_select_by_transaction_id_record(self.engine,id)
    #         if record.shape[0] > 0:
    #             je_record_filter = record[record['status'] == "POSTED"]
    #             if je_record_filter.shape[0] == 0:
    #                 je_delete_by_transaction_id_record(self.engine, id)
    #                 return_data = {
    #                     "data": {
    #                         "transactiond_id": id,
    #                         "status": "DELETED"
    #                     }
    #                 }
    #                 loggerOutput(message=f"delete_journal_entry_by_transaction_id - {return_data}")
    #             else:
    #                 return_data = {
    #                 "error": "delete_journal_entry_by_transaction_id - Transaction ID has posted records"
    #             }
    #         else:
    #             return_data = {
    #                 "error": "delete_journal_entry_by_transaction_id - Transaction ID Not Found"
    #             }
    #     except TypeError as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"delete_journal_entry_by_transaction_id - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     except BaseException as e:
    #         loggerOutput(method=logger_types.ERROR, message=f"delete_journal_entry_by_transaction_id - Caught something: {type(e).__name__} -> {e}")
    #         return_data = {
    #             "error": str(e)
    #         }
    #     finally:
    #         loggerOutput(message=f"DONE: delete_journal_entry_by_transaction_id - {return_data}")
    #         return return_data

        

    


    
