from pydantic import (
    BaseModel,
    Field
)
from pathlib import Path
from radna_accounting.test.data.db.helpers import setSQLFilePath

class SelectTransactionIdsDetails(BaseModel):
    text: str = Field(default_factory=lambda: setSQLFilePath(
                base_path=Path(__file__).parent, 
                file_name="select_ti_details.sql"
            )
        )
    ti_month: int | None = None
    ti_year: int | None = None
    ti_id: str | None = None