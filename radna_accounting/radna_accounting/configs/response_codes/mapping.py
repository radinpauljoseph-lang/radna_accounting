from .error_model import ErrorModel
COA_CODE = "COA"
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