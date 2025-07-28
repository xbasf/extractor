from os.path import splitext
from typing import List, Literal, Optional, Tuple

import yaml
from pydantic import BaseModel, computed_field


class ConfigModel(BaseModel):
    pdf_filename: str
    pdf_data_pages: List[Tuple[int, int]]

    @classmethod
    def from_yaml(cls, filename: str):
        with open(filename, "r") as stream:
            config = yaml.safe_load(stream)
        return cls(**config)


class SchemaModel(BaseModel):
    name: str
    dtype: Literal["object", "int", "float", "bool", "datetime-2024", "string"]
    label_col: Optional[bool] = False
    rename_col: Optional[bool] = False


class PdfPageModel(BaseModel):
    filename: str
    data_page: int
    multiple_label_merge_strategy: Literal["shift_up", "collapse"] = "shift_up"
    schemas: Optional[List[SchemaModel]] = None
    get_stats: Optional[bool] = False

    @computed_field
    @property
    def output_filename(self) -> str:
        return f"{splitext(self.filename)[0]}_pg{self.data_page}.csv"

    @computed_field
    @property
    def output_stats_filename(self) -> str:
        return f"{splitext(self.filename)[0]}_pg{self.data_page}_stats.csv"

    @classmethod
    def from_yaml(cls, filename: str):
        with open(filename, "r") as stream:
            config = yaml.safe_load(stream)
        return cls(**config)


if __name__ == "__main__":
    config = ConfigModel.from_yaml(filename="src/extractor/config.yaml")
    print(config)

    pdf_page_model = PdfPageModel.from_yaml(
        filename="src/extractor/config.yaml"
    )
    print(pdf_page_model)
