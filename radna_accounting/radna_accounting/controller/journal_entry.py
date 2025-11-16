import copy
import uuid
from datetime import datetime

from ..configs.config import (
    logger, 
    engine
)
from ..validators.journal_entry import JournalEntryModel
from ..validators.transaction_id_tracker import TransactionIdTrackerModel
from ..core.chart_of_accounts.record_operations import account_select_all_account_records 
from ..core.accounting_periods.record_operations import accounting_period_select_all_account_records
from ..core.journal_entry.record_operations import (
    je_record_value_validate,
    je_select_record,
    je_select_multiple_record,
    je_select_transaction_id_distinct_values,
    je_insert_record,
    je_update_record,
    je_select_by_transaction_id_record,
    je_delete_by_transaction_id_record,
    je_update_to_post_record,
    je_update_to_post_by_month_year_record,
    je_select_by_transaction_date_month_year_record
)
from ..core.transaction_id_tracker.record_operations import (
    transaction_id_tracker_insert_record,
    transaction_id_tracker_select_by_month_year_record
)

class JournalEntryController:
    def __init__(self):
        self.validator_model = JournalEntryModel
        self.transaction_id_tracker_model = TransactionIdTrackerModel
        self.engine = engine

    def create_journal_entry(self, obj) -> dict:
        return_data = {}
        is_accounting_period_exists = False
        is_accounting_period_open = False
        is_transaction_id_exists = False
        try:
            je_obj = self.validator_model(**obj)
            je_obj = je_obj.model_dump()
            je_obj['id'] = uuid.uuid4()
            je_obj['status'] ="UNPOSTED"
            transaction_id = je_obj['transaction_id']
            transaction_id_entry_number = transaction_id.split("-")[1]
            transaction_id_month_year = transaction_id.split("-")[0]
            transaction_date_month = je_obj['transaction_date'].month
            transaction_date_year = je_obj['transaction_date'].year
            
            je_exists = je_record_value_validate(self.engine, 'id', je_obj['id'])
            accounting_periods = accounting_period_select_all_account_records(self.engine)
            if accounting_periods.shape[0] > 0:
                accounting_periods = accounting_periods[accounting_periods['year'] == transaction_date_year]
                if accounting_periods.shape[0] > 0:
                    accounting_periods = accounting_periods[accounting_periods['month'] == transaction_date_month]
            is_accounting_period_exists = True if accounting_periods.shape[0] == 1 else False
            
            if is_accounting_period_exists:
                accounting_periods = accounting_periods[accounting_periods['status'] == 'OPEN']
            is_accounting_period_open = True if accounting_periods.shape[0] == 1 else False

            transaction_ids_df = transaction_id_tracker_select_by_month_year_record(engine, transaction_date_month, transaction_date_year)
            if transaction_ids_df.shape[0] > 0:
                transaction_ids_df = transaction_ids_df[transaction_ids_df['year'] == transaction_date_year]
                if transaction_ids_df.shape[0] > 0:
                    transaction_ids_df = transaction_ids_df[transaction_ids_df['month'] == transaction_date_month]
                    if transaction_ids_df.shape[0] > 0:
                        transaction_ids_df = transaction_ids_df[transaction_ids_df['id'] == transaction_id_entry_number]
                        is_transaction_id_exists = True if (transaction_ids_df.shape[0] == 1 and transaction_id_month_year == f"{transaction_date_year}{transaction_date_month:02}") else False

            if not je_exists:
                record = copy.deepcopy(je_obj)
                del record['created_date']
                del record['updated_date']

                if not is_accounting_period_exists:
                    raise Exception(f"create_journal_entry - Accounting Period {transaction_date_month:02}-{transaction_date_year} does not exist")
                if not is_accounting_period_open:
                    raise Exception(f"create_journal_entry - Accounting Period {transaction_date_month:02}-{transaction_date_year} is already closed")
                if not is_transaction_id_exists:
                    raise Exception(f"create_journal_entry - Transaction ID {transaction_id} does not exist or does not align with the transaction date used")
                
                account_numbers = account_select_all_account_records(self.engine)
                account_numbers_filtered = account_numbers[account_numbers['account_id'] == record['account_number']]
                is_account_number_exists = True if account_numbers_filtered.shape[0] == 1 else False
                if not is_account_number_exists:
                    raise Exception("create_journal_entry - account number does not exist")
                
                je_records = je_select_by_transaction_id_record(self.engine, transaction_id)
                if je_records.shape[0] > 0:
                    je_records = je_records[je_records['status'] == "POSTED"]
                    if je_records.shape[0] > 0:
                        raise Exception(f"create_journal_entry - Transaction ID already posted")
                
                je_insert_record(self.engine, record)
                new_transaction_id_validator = transaction_id_tracker_select_by_month_year_record(engine, transaction_date_month, transaction_date_year)
                if int(transaction_id_entry_number) == new_transaction_id_validator.shape[0]:
                    new_entry_number = int(transaction_id_entry_number) + 1
                    new_entry_number = f"{new_entry_number:05}"
                    transaction_id_tracker_record = self.transaction_id_tracker_model(
                        month=transaction_date_month,
                        year=transaction_date_year,
                        id=new_entry_number
                    ).model_dump()
                    transaction_id_tracker_insert_record(self.engine, transaction_id_tracker_record)
                    
                record = je_select_record(self.engine, record['id'])
                logger.info(record)
                record = self.validator_model(**record)
                record = record.model_dump()
                return_data = {
                    "data": record
                }
                logger.info(f"create_journal_entry - {return_data}")
            else:
                return_data = {
                    "error": "create_journal_entry - Journal Entry already exists"
                }
        except TypeError as e:
            logger.error(f"create_journal_entry - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except BaseException as e:
            logger.error(f"create_journal_entry - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        finally:
            logger.info(f"DONE: create_journal_entry - {return_data}")
            return return_data
    
    def update_journal_entry(self, id, obj) -> dict:
        return_data = {}
        try:
            record = je_select_record(self.engine, id)
            if record:
                je_obj = self.validator_model(**record)
                je_obj = je_obj.model_dump()
                allowed_fields = [
                    'transaction_date',
                    'account_number',
                    'description',
                    'entry_type',
                    'amount'
                ]
                account_numbers = account_select_all_account_records(self.engine)
                account_numbers_filtered = account_numbers[account_numbers['account_id'] == record['account_number']]
                is_account_number_exists = True if account_numbers_filtered.shape[0] == 1 else False
                if not is_account_number_exists:
                    raise Exception("update_journal_entry - account number does not exist")
                
                if record['status'] != "UNPOSTED":
                    return_data = {
                            "error": f"update_journal_entry - Journal Entry already posted"
                        }
                    raise Exception(f"update_journal_entry - Journal Entry already posted")
                
                for key in obj.keys():
                    je_obj[key] = obj[key]
                    
                record = self.validator_model(**je_obj)
                record = record.model_dump()
                for key in obj.keys():
                    if key not in allowed_fields:
                        return_data = {
                            "error": f"update_journal_entry - {key} field not allowed"
                        }
                        raise Exception(f"update_journal_entry - {key} field not allowed")
                    
                now = datetime.now()
                now = now.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(now.microsecond/1000):03d}"
                record['updated_date'] = now
                for key in je_obj.keys():
                    if key in allowed_fields:
                        record[key] = je_obj[key]
                
                je_update_record(self.engine, id, record)
                record = je_select_record(self.engine, id)
                record = self.validator_model(**record)
                record = record.model_dump()

                return_data = {
                    "data": record
                }
                logger.info(f"update_journal_entry - {return_data}")
            else:
                return_data = {
                    "error": "update_journal_entry - Journal Entry ID Not Found"
                }
        except TypeError as e:
            logger.error(f"update_journal_entry - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except ValueError as e:
            logger.error(f"update_journal_entry - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except BaseException as e:
            logger.error(f"update_journal_entry - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        finally:
            logger.info(f"DONE: update_journal_entry - {return_data}")
            return return_data

    def post_journal_entry_by_transaction_id(self, id) -> dict:
        return_data = {}
        try:
            record = je_select_by_transaction_id_record(self.engine, id)
            if record.shape[0] > 0:
                unposted_record_filter = record[record['status'] == "UNPOSTED"]
                if unposted_record_filter.shape[0] == 0:
                    return_data = {
                        "error": f"post_journal_entry_by_transaction_id - Journal Entry already posted"
                    }
                else:
                    credit_je_records = record[record['entry_type'] == "CREDIT"]
                    debit_je_records = record[record['entry_type'] == "DEBIT"]
                    if credit_je_records.shape[0] == 0 or debit_je_records.shape[0] == 0:
                        return_data = {
                            "error": f"post_journal_entry_by_transaction_id - Journal Entry Transaction ID {id} has either no debit or credit record"
                        }
                    else:
                        credit_sum = credit_je_records.sum()
                        debit_sum = debit_je_records.sum()
                        if credit_sum == debit_sum:
                            je_update_to_post_record(self.engine, id)
                            return_data = {
                                "error": f"post_journal_entry_by_transaction_id - Journal Entry Transaction ID {id} have unbalanced amounts"
                            }
                        else:
                            return_data = {
                                "error": f"post_journal_entry_by_transaction_id - Journal Entry Transaction ID {id} have unbalanced amounts"
                            }
                    je_update_to_post_record(self.engine, id)
                
                    record = je_select_by_transaction_id_record(self.engine, id, record)

                    return_data = {
                        "data": record.to_dict()
                    }
                    logger.info(f"post_journal_entry_by_transaction_id - {return_data}")
            else:
                return_data = {
                    "error": "post_journal_entry_by_transaction_id - Journal Entry Transaction ID Not Found"
                }
        except TypeError as e:
            logger.error(f"post_journal_entry_by_transaction_id - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except ValueError as e:
            logger.error(f"post_journal_entry_by_transaction_id - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except BaseException as e:
            logger.error(f"post_journal_entry_by_transaction_id - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        finally:
            logger.info(f"DONE: post_journal_entry_by_transaction_id - {return_data}")
            return return_data
        
    def post_journal_entry_by_month_year(self, month, year) -> dict:
        return_data = {}
        try:
            record = je_select_by_transaction_date_month_year_record(self.engine, month, year)
            if record.shape[0] > 0:
                unposted_record_filter = record[record['status'] == "UNPOSTED"]
                if unposted_record_filter.shape[0] == 0:
                    return_data = {
                        "error": f"post_journal_entry_by_month_year - Journal Entry already posted"
                    }
                else:
                    transaction_ids = record['transaction_id'].unique()
                    logger.info("@@@@@@@@@@@@@@@@@")
                    logger.info(transaction_ids)
                    logger.info("@@@@@@@@@@@@@@@@@")
                    # record = je_select_by_transaction_date_month_year_record(self.engine, month, year)
                    for index in range(len(transaction_ids)):
                        logger.info("@@@@@@@@@@@@@@@@@")
                        logger.info(transaction_ids[index])
                        logger.info("@@@@@@@@@@@@@@@@@")
                        filtered_records = record[record['transaction_id'] == transaction_ids[index]]
                        credit_je_records = filtered_records[filtered_records['entry_type'] == 'CREDIT']
                        debit_je_records = filtered_records[filtered_records['entry_type'] == 'DEBIT']
                        if credit_je_records.shape[0] == 0 or debit_je_records.shape[0] == 0:
                            return_data = {
                                "error": f"post_journal_entry_by_month_year - Journal Entry Transaction IDs by month & year has either no debit or credit record"
                            }
                            raise Exception(f"post_journal_entry_by_month_year - Journal Entry Transaction IDs by month & year has either no debit or credit record")
                        else:
                            credit_sum = credit_je_records['amount'].sum()
                            debit_sum = debit_je_records['amount'].sum()
                            if credit_sum != debit_sum:
                                return_data = {
                                    "error": f"post_journal_entry_by_month_year - Journal Entry Transaction IDs by month & year have unbalanced amounts"
                                }
                                raise Exception(f"post_journal_entry_by_month_year - Journal Entry Transaction IDs by month & year have unbalanced amounts")
                    je_update_to_post_by_month_year_record(self.engine, month, year)
                        
                    record = je_select_by_transaction_date_month_year_record(self.engine, month, year)

                    return_data = {
                        "data": record.to_dict()
                    }
                    logger.info(f"post_journal_entry_by_month_year - {return_data}")
            else:
                return_data = {
                    "error": "post_journal_entry_by_month_year - Journal Entry Transaction IDs by given month & year Not Found"
                }
        except TypeError as e:
            logger.error(f"post_journal_entry_by_month_year - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except ValueError as e:
            logger.error(f"post_journal_entry_by_month_year - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except BaseException as e:
            logger.error(f"post_journal_entry_by_month_year - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        finally:
            logger.info(f"DONE: post_journal_entry_by_month_year - {return_data}")
            return return_data
        
    
    
    def get_journal_entry(self, id) -> dict:
        return_data = {}
        try:
            record = je_select_record(self.engine,id)
            if record:
                return_data = {
                    "data": record
                }
                logger.info(f"get_journal_entry - {return_data}")
            else:
                return_data = {
                    "error": "get_journal_entry - Journal Entry ID Not Found"
                }
        except TypeError as e:
            logger.error(f"get_journal_entry - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except BaseException as e:
            logger.error(f"get_journal_entry - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        finally:
            logger.info(f"DONE: get_journal_entry - {return_data}")
            return return_data
        
    def get_journal_entry_by_transaction_id(self, id) -> dict:
        return_data = {}
        try:
            record = je_select_by_transaction_id_record(self.engine,id)
            if record.shape[0] > 0:
                return_data = {
                    "data": record.to_dict()
                }
                logger.info(f"get_journal_entry_by_transaction_id - {return_data}")
            else:
                return_data = {
                    "error": "get_journal_entry_by_transaction_id - Transaction ID Not Found"
                }
        except TypeError as e:
            logger.error(f"get_journal_entry_by_transaction_id - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except BaseException as e:
            logger.error(f"get_journal_entry_by_transaction_id - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        finally:
            logger.info(f"DONE: get_journal_entry_by_transaction_id - {return_data}")
            return return_data

    def delete_journal_entry_by_transaction_id(self, id) -> dict:
        return_data = {}
        try:
            record = je_select_by_transaction_id_record(self.engine,id)
            if record.shape[0] > 0:
                je_record_filter = record[record['status'] == "POSTED"]
                if je_record_filter.shape[0] == 0:
                    je_delete_by_transaction_id_record(self.engine, id)
                    return_data = {
                        "data": {
                            "transactiond_id": id,
                            "status": "DELETED"
                        }
                    }
                    logger.info(f"delete_journal_entry_by_transaction_id - {return_data}")
                else:
                    return_data = {
                    "error": "delete_journal_entry_by_transaction_id - Transaction ID has posted records"
                }
            else:
                return_data = {
                    "error": "delete_journal_entry_by_transaction_id - Transaction ID Not Found"
                }
        except TypeError as e:
            logger.error(f"delete_journal_entry_by_transaction_id - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        except BaseException as e:
            logger.error(f"delete_journal_entry_by_transaction_id - Caught something: {type(e).__name__} -> {e}")
            return_data = {
                "error": str(e)
            }
        finally:
            logger.info(f"DONE: delete_journal_entry_by_transaction_id - {return_data}")
            return return_data

        

    


    
