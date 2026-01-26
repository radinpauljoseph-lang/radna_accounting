from .error_model import ErrorModel
COA_CODE = "COA"
JNE_CODE = "JNE"
TIS_CODE = "TIS"
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
        message="{model_name} Error: incorrect account ID data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{COA_CODE}0002": ErrorModel(
        status=400,
        code=f"{COA_CODE}0002",
        message="{model_name} Error: account ID minimum field length not met",
        details=None
    ).model_dump(),
    f"{COA_CODE}0003": ErrorModel(
        status=400,
        code=f"{COA_CODE}0003",
        message="{model_name} Error: account ID maximum length is {account_id_length}",
        details=None
    ).model_dump(),
    f"{COA_CODE}0004": ErrorModel(
        status=400,
        code=f"{COA_CODE}0004",
        message="{model_name} Error: incorrect account name data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{COA_CODE}0005": ErrorModel(
        status=400,
        code=f"{COA_CODE}0005",
        message="{model_name} Error: account name maximum length is {name_length}",
        details=None
    ).model_dump(),
    f"{COA_CODE}0006": ErrorModel(
        status=400,
        code=f"{COA_CODE}0006",
        message="{model_name} Error: account name minimum length is 1",
        details=None
    ).model_dump(),
    f"{COA_CODE}0007": ErrorModel(
        status=400,
        code=f"{COA_CODE}0007",
        message="{model_name} Error: incorrect account type data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{COA_CODE}0008": ErrorModel(
        status=400,
        code=f"{COA_CODE}0008",
        message="{model_name} Error: Unknown account type \'{account_type}\'",
        details=None
    ).model_dump(),
    f"{COA_CODE}0009": ErrorModel(
        status=400,
        code=f"{COA_CODE}0009",
        message="{model_name} Error: incorrect account description data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{COA_CODE}0010": ErrorModel(
        status=400,
        code=f"{COA_CODE}0010",
        message="{model_name} Error: account description field maximum length is {description_length}",
        details=None
    ).model_dump(),
    f"{COA_CODE}0011": ErrorModel(
        status=400,
        code=f"{COA_CODE}0011",
        message="{model_name} Error: incorrect account mapping data type \'{variable_type}\'",
        details=None
    ).model_dump(),
    f"{COA_CODE}0012": ErrorModel(
        status=400,
        code=f"{COA_CODE}0012",
        message="{model_name} Error: account mapping field maximum length is {account_id_length}",
        details=None
    ).model_dump(),
    f"{COA_CODE}0013": ErrorModel(
        status=400,
        code=f"{COA_CODE}0013",
        message="{model_name} Error: account mapping value should not be the same as its account ID",
        details=None
    ).model_dump(),

    f"{COA_CODE}0101": ErrorModel(
        status=400,
        code=f"{COA_CODE}0101",
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
        message="Account ID required",
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

    # History Tables
    f"{JNE_CODE}{HIS_CODE}0001": ErrorModel(
        status=400,
        code=f"{JNE_CODE}{HIS_CODE}0001",
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