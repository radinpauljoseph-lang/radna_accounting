from .error_model import ErrorModel
COA_CODE = "COA"
JNE_CODE = "JNE"
TIS_CODE = "TIS"
ACP_CODE = "ACP"
JNV_CODE = "JNV"
HIS_CODE = "HIS"
WEB_CODE = "WEB"
SYS_CODE = "SYS"
MESSAGE_KEY = "message"
CODE_KEY = "code"
STATUS_KEY = "status"
DETAILS_KEY = "details"

error_map = {
    # Chart Of Accounts
    f"{COA_CODE}0001": ErrorModel(
        status=400,
        code=f"{COA_CODE}0001",
        message="Incorrect account ID data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{COA_CODE}0002": ErrorModel(
        status=400,
        code=f"{COA_CODE}0002",
        message="Account ID minimum field length not met",
        details=None
    ).model_dump(),
    f"{COA_CODE}0003": ErrorModel(
        status=400,
        code=f"{COA_CODE}0003",
        message="Account ID maximum length is {account_id_length}",
        details=None
    ).model_dump(),
    f"{COA_CODE}0004": ErrorModel(
        status=400,
        code=f"{COA_CODE}0004",
        message="Incorrect account name data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{COA_CODE}0005": ErrorModel(
        status=400,
        code=f"{COA_CODE}0005",
        message="Account name maximum length is {name_length}",
        details=None
    ).model_dump(),
    f"{COA_CODE}0006": ErrorModel(
        status=400,
        code=f"{COA_CODE}0006",
        message="Account name minimum length is 1",
        details=None
    ).model_dump(),
    f"{COA_CODE}0007": ErrorModel(
        status=400,
        code=f"{COA_CODE}0007",
        message="Incorrect account type data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{COA_CODE}0008": ErrorModel(
        status=400,
        code=f"{COA_CODE}0008",
        message="Unknown account type \'{account_type}\'",
        details=None
    ).model_dump(),
    f"{COA_CODE}0009": ErrorModel(
        status=400,
        code=f"{COA_CODE}0009",
        message="Incorrect account description data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{COA_CODE}0010": ErrorModel(
        status=400,
        code=f"{COA_CODE}0010",
        message="Account description field maximum length is {description_length}",
        details=None
    ).model_dump(),
    f"{COA_CODE}0011": ErrorModel(
        status=400,
        code=f"{COA_CODE}0011",
        message="Incorrect account mapping data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{COA_CODE}0012": ErrorModel(
        status=400,
        code=f"{COA_CODE}0012",
        message="Account mapping field maximum length is {account_id_length}",
        details=None
    ).model_dump(),
    f"{COA_CODE}0013": ErrorModel(
        status=400,
        code=f"{COA_CODE}0013",
        message="Account mapping value should not be the same as its account ID",
        details=None
    ).model_dump(),

    f"{COA_CODE}0101": ErrorModel(
        status=400,
        code=f"{COA_CODE}0101",
        message="Account ID \'{account_id}\' does not exist",
        details=None
    ).model_dump(),
    f"{JNV_CODE}{COA_CODE}0101": ErrorModel(
        status=400,
        code=f"{JNV_CODE}{COA_CODE}0101",
        message="Account ID \'{account_id}\' does not exist",
        details=None
    ).model_dump(),
    f"{JNE_CODE}{COA_CODE}0101": ErrorModel(
        status=400,
        code=f"{JNE_CODE}{COA_CODE}0101",
        message="Account ID \'{account_id}\' does not exist",
        details=None
    ).model_dump(),
    f"{COA_CODE}0102": ErrorModel(
        status=400,
        code=f"{COA_CODE}0102",
        message="\'{key}\' field not allowed",
        details=None
    ).model_dump(),
    f"{COA_CODE}0103": ErrorModel(
        status=400,
        code=f"{COA_CODE}0103",
        message="Account Name \'{account_name}\' already exists",
        details=None
    ).model_dump(),
    f"{COA_CODE}0104": ErrorModel(
        status=400,
        code=f"{COA_CODE}0104",
        message="Account Map \'{account_mapping}\' Not Found",
        details=None
    ).model_dump(),
    f"{COA_CODE}0105": ErrorModel(
        status=400,
        code=f"{COA_CODE}0105",
        message="Account ID \'{account_id}\' already exists",
        details=None
    ).model_dump(),
    f"{COA_CODE}0106": ErrorModel(
        status=400,
        code=f"{COA_CODE}0106",
        message="Account ID \'{account_id}\' Not Found",
        details=None
    ).model_dump(),
    f"{COA_CODE}0107": ErrorModel(
        status=400,
        code=f"{COA_CODE}0107",
        message="Account ID is required",
        details=None
    ).model_dump(),

    # Journal Entry
    f"{JNE_CODE}0001": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0001",
        message="Incorrect Journal Entry ID is not a valid UUID",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0002": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0002",
        message="Incorrect transaction ID data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0003": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0003",
        message="Transaction ID should not be empty",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0004": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0004",
        message="Transaction ID maximum length is {transaction_id_length}",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0005": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0005",
        message="Transaction ID not in proper format",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0006": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0006",
        message="Year in Transaction ID is not a valid year",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0007": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0007",
        message="Month in Transaction ID is not a valid month",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0008": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0008",
        message="Journal Entry ID is required",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0009": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0009",
        message="Transaction ID is required",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0010": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0010",
        message="Transaction Date not in proper format",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0011": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0011",
        message="Incorrect Transaction Date data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0012": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0012",
        message="Unknown entry type \'{entry_type}\'",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0013": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0013",
        message="Incorrect entry type data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0014": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0014",
        message="Incorrect description data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0015": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0015",
        message="Description field maximum length is {description_length}",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0015": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0015",
        message="Description field maximum length is {description_length}",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0016": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0016",
        message="Incorrect amount data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0017": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0017",
        message=" Currency Code required length is {currency_code_length}",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0018": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0018",
        message="invalid currency code \'{currency_code}\'",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0019": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0018",
        message="Incorrect Currency Code data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0020": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0020",
        message="Posting Date not in proper format",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0021": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0021",
        message="Incorrect Posting Date data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0022": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0022",
        message="Invalid Posting Date \'{posting_date}\'",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0023": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0023",
        message="Invalid Transaction Date \'{transaction_date}\'",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0024": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0024",
        message="Unknown status \'{status}\'",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0025": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0025",
        message="Incorrect status data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0026": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0026",
        message="Journal Entry ID does not exist",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0027": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0027",
        message="Journal Entry Status not valid for deletion",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0028": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0028",
        message="Transaction ID does not exist",
        details=None
    ).model_dump(),
    f"{JNV_CODE}{JNE_CODE}0028": ErrorModel(
        status=400,
        code=f"{JNV_CODE}{JNE_CODE}0028",
        message="Transaction ID does not exist",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0101": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0101",
        message="\'{key}\' field not allowed",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0101": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0101",
        message="\'{key}\' field not allowed",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0102": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0102",
        message="Journal Entry ID already exists",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0103": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0103",
        message="Transaction ID used not valid for given Transaction Date",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0104": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0104",
        message="Error during transition for review",
        details=[]
    ).model_dump(),
     f"{JNE_CODE}0105": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0105",
        message="Journal Entry {id}\'s status \'{status}\' not valid for review",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0106": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0106",
        message="Transaction ID\'s Credit & Debit amounts are not equal",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0107": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0107",
        message="Journal Entry {id} already for review",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0108": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0108",
        message="Transaction Dates not equal",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0109": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0109",
        message="\'{key}\' field not allowed",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0110": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0110",
        message="Journal Entry {id}\'s status \'{status}\' not valid for update",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0111": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0111",
        message="Journal Entry {id} already approved",
        details=None
    ).model_dump(),
     f"{JNE_CODE}0112": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0112",
        message="Journal Entry {id}\'s status \'{status}\' not valid for approval",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0113": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0113",
        message="Error during transition to approval",
        details=[]
    ).model_dump(),
    f"{JNE_CODE}0114": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0114",
        message="Journal Entry {id} already rejected",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0115": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0115",
        message="Journal Entry {id}\'s status \'{status}\' not valid for rejection",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0116": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0116",
        message="Error during transition to approval",
        details=[]
    ).model_dump(),
    f"{JNE_CODE}0117": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0117",
        message="Journal Entry {id} already posted",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0118": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0118",
        message="Journal Entry {id}\'s status \'{status}\' not valid for posting",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0119": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0119",
        message="Error during transition to approval",
        details=[]
    ).model_dump(),

    # Transaction IDs
    f"{TIS_CODE}0001": ErrorModel(
        status=400,
        code=f"{TIS_CODE}0001",
        message="Incorrect month data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{TIS_CODE}0002": ErrorModel(
        status=400,
        code=f"{TIS_CODE}0002",
        message="Value is not a valid month",
        details=None
    ).model_dump(),
    f"{TIS_CODE}0003": ErrorModel(
        status=400,
        code=f"{TIS_CODE}0003",
        message="Incorrect year data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{TIS_CODE}0004": ErrorModel(
        status=400,
        code=f"{TIS_CODE}0004",
        message="Value is not a valid year",
        details=None
    ).model_dump(),
    f"{TIS_CODE}0005": ErrorModel(
        status=400,
        code=f"{TIS_CODE}0005",
        message="Future accounting period is not allowed",
        details=None
    ).model_dump(),
    f"{TIS_CODE}0006": ErrorModel(
        status=400,
        code=f"{TIS_CODE}0006",
        message="Incorrect transaction ID data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{TIS_CODE}0007": ErrorModel(
        status=400,
        code=f"{TIS_CODE}0007",
        message="ID maximum length is {id_length}",
        details=None
    ).model_dump(),
    f"{TIS_CODE}0008": ErrorModel(
        status=400,
        code=f"{TIS_CODE}0008",
        message="ID not in proper format",
        details=None
    ).model_dump(),
    f"{TIS_CODE}0009": ErrorModel(
        status=400,
        code=f"{TIS_CODE}0009",
        message="Transaction ID not in proper format",
        details=None
    ).model_dump(),
    f"{JNE_CODE}0010": ErrorModel(
        status=400,
        code=f"{JNE_CODE}0010",
        message="Invalid Transaction ID",
        details=None
    ).model_dump(),
    f"{JNE_CODE}{TIS_CODE}0101": ErrorModel(
        status=400,
        code=f"{JNE_CODE}{TIS_CODE}0101",
        message="Invalid Transaction ID",
        details=None
    ).model_dump(),


    # Accounting Periods
    f"{ACP_CODE}0001": ErrorModel(
        status=400,
        code=f"{ACP_CODE}0001",
        message="Incorrect month data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{ACP_CODE}0002": ErrorModel(
        status=400,
        code=f"{ACP_CODE}0002",
        message="Value is not a valid month",
        details=None
    ).model_dump(),
    f"{ACP_CODE}0003": ErrorModel(
        status=400,
        code=f"{ACP_CODE}0003",
        message="Incorrect year data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{ACP_CODE}0004": ErrorModel(
        status=400,
        code=f"{ACP_CODE}0004",
        message="Value is not a valid year",
        details=None
    ).model_dump(),
    f"{ACP_CODE}0005": ErrorModel(
        status=400,
        code=f"{ACP_CODE}0005",
        message="Future accounting period is not allowed",
        details=None
    ).model_dump(),
    f"{ACP_CODE}0006": ErrorModel(
        status=400,
        code=f"{ACP_CODE}0006",
        message="Unknown status \'{status}\'",
        details=None
    ).model_dump(),
    f"{ACP_CODE}0007": ErrorModel(
        status=400,
        code=f"{ACP_CODE}0007",
        message="Incorrect status data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{ACP_CODE}0101": ErrorModel(
        status=400,
        code=f"{ACP_CODE}0101",
        message="Accounting Period is already closed",
        details=None
    ).model_dump(),
    f"{ACP_CODE}0102": ErrorModel(
        status=400,
        code=f"{ACP_CODE}0102",
        message="Accounting Period already exists",
        details=None
    ).model_dump(),
    f"{ACP_CODE}0103": ErrorModel(
        status=400,
        code=f"{ACP_CODE}0103",
        message="Accounting Period does not exist",
        details=None
    ).model_dump(),
    f"{ACP_CODE}0104": ErrorModel(
        status=400,
        code=f"{ACP_CODE}0104",
        message="Accounting Period contains unposted records",
        details=None
    ).model_dump(),
    f"{ACP_CODE}0105": ErrorModel(
        status=400,
        code=f"{ACP_CODE}0105",
        message="Unable to close period due to unused transaction IDs",
        details=None
    ).model_dump(),
    f"{JNE_CODE}{ACP_CODE}0101": ErrorModel(
        status=400,
        code=f"{ACP_CODE}0101",
        message="Accounting Period for {transaction_date} does not exist",
        details=None
    ).model_dump(),
     f"{JNE_CODE}{ACP_CODE}0102": ErrorModel(
        status=400,
        code=f"{JNE_CODE}{ACP_CODE}0102",
        message="Accounting Period is already closed",
        details=None
    ).model_dump(),

    # Journal Voucher
    f"{JNV_CODE}0001": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0001",
        message="Journal Voucher ID is not a valid UUID",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0002": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0002",
        message="Journal Entry ID is required",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0003": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0003",
        message="Incorrect transaction ID data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0004": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0004",
        message="Transaction ID should not be empty",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0005": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0005",
        message="Transaction ID maximum length is {transaction_id_length}",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0006": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0006",
        message="Transaction ID not in proper format",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0007": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0007",
        message="Year in Transaction ID is not a valid year",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0008": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0008",
        message="Month in Transaction ID is not a valid month",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0009": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0009",
        message="Transaction ID is required",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0010": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0010",
        message="Incorrect Document Name data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0011": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0011",
        message="Document Name field maximum length is {description_length}",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0012": ErrorModel(
        status=400,
        code=f"{JNV_CODE}012",
        message="Incorrect Document Path data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0013": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0013",
        message="Document Path field maximum length is {description_length}",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0014": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0014",
        message="Incorrect Document File Type data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0015": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0015",
        message="Document File Type field maximum length is {description_length}",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0016": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0016",
        message="Incorrect Signed Document Name data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0017": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0017",
        message="Signed Document Name field maximum length is {description_length}",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0018": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0018",
        message="Incorrect Signed Document Path data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0019": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0019",
        message="Signed Document Path field maximum length is {description_length}",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0020": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0020",
        message="Incorrect Signed Document File Type data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0021": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0021",
        message="Signed Document File Type field maximum length is {description_length}",
        details=None
    ).model_dump(),
    f"{JNV_CODE}0101": ErrorModel(
        status=400,
        code=f"{JNV_CODE}0101",
        message="Transaction ID does not exist",
        details=None
    ).model_dump(),

    # History Tables
    f"{JNE_CODE}{HIS_CODE}0001": ErrorModel(
        status=400,
        code=f"{JNE_CODE}{HIS_CODE}0001",
        message="Unknown History Operation \'{history_operation}\'",
        details=None
    ).model_dump(),
    f"{ACP_CODE}{HIS_CODE}0001": ErrorModel(
        status=400,
        code=f"{ACP_CODE}{HIS_CODE}0001",
        message="Unknown History Operation \'{history_operation}\'",
        details=None
    ).model_dump(),
    f"{JNV_CODE}{HIS_CODE}0001": ErrorModel(
        status=400,
        code=f"{JNV_CODE}{HIS_CODE}0001",
        message="Unknown History Operation \'{history_operation}\'",
        details=None
    ).model_dump(),

    # API Request
    f"{WEB_CODE}0001": ErrorModel(
        status=400,
        code=f"{WEB_CODE}0001",
        message="Missing headers: {header}",
        details=None
    ).model_dump(),
    f"{WEB_CODE}0002": ErrorModel(
        status=400,
        code=f"{WEB_CODE}0002",
        message="Request Method \'{method}\' not supported",
        details=None
    ).model_dump(),

    # Default
    f"{SYS_CODE}400": ErrorModel(
        status=400,
        code=f"{SYS_CODE}400",
        message="Bad Request",
        details=None
    ).model_dump(),
    f"{SYS_CODE}500": ErrorModel(
        status=500,
        code=f"{SYS_CODE}500",
        message="Internal Server Error",
        details=None
    ).model_dump()
}