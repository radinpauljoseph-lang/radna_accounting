from pathlib import Path
from radna_accounting.test.data.db.constants import SQL_FILES_DIR

def setSQLFilePath(base_path: str = Path(__file__).parent, file_name: str = ""):
    if not isinstance(file_name, str):
        raise ValueError(f"file_name: invalid data type {type(file_name)}")

    print()
    file_directory = Path(
        base_path / SQL_FILES_DIR / file_name
        ).read_text()
    return file_directory