from pydantic import (
    BaseModel,
    Field
)
from pathlib import Path
from radna_accounting.test.data.db.helpers import setSQLFilePath

class SelectChartOfAccountsByDetails(BaseModel):
    text: str = Field(default_factory=lambda: setSQLFilePath(
        base_path=Path(__file__).parent, 
        file_name="select_coa_by_details.sql"
        )
    )
    coa_account_id: str | None = None
    coa_name: str | None = None
    coa_type: str | None = None
    coa_description: str | None = None
    coa_account_mapping: str = ""

class SelectChartOfAccountsByDetailsDescriptionIsNull(BaseModel):
    text: str = Field(default_factory=lambda: setSQLFilePath(
            base_path=Path(__file__).parent, 
            file_name="select_coa_by_details_description_is_null.sql"
        )
    )
    coa_account_id: str | None = None
    coa_name: str | None = None
    coa_type: str | None = None
    coa_account_mapping: str = ""

class SelectChartOfAccountsByAccountId(BaseModel):
    text: str = Field(default_factory=lambda: setSQLFilePath(
            base_path=Path(__file__).parent, 
            file_name="select_coa_by_account_id.sql"
        )
    )
    coa_account_id: str | None = None

class SelectChartOfAccountsByName(BaseModel):
    text: str = Field(default_factory=lambda: setSQLFilePath(
            base_path=Path(__file__).parent, 
            file_name="select_coa_by_name.sql"
        )
    )
    coa_name: str | None = None