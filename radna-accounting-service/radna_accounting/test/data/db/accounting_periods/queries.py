from pydantic import (
    BaseModel,
    Field
)
from pathlib import Path
from radna_accounting.test.data.db.helpers import setSQLFilePath

class SelectAccountingPeriodByMonthYear(BaseModel):
    text: str = Field(default_factory=lambda: setSQLFilePath(
            base_path=Path(__file__).parent, 
            file_name="select_ap_by_month_year.sql"
        )
    )
    period_month: int | None = None
    period_year: int | None = None