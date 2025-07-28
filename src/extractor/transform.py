from typing import List

import pandas as pd

try:
    from .model import SchemaModel
except ImportError:
    from model import SchemaModel


def impose_df_schema(schemas: List[SchemaModel], df: pd.DataFrame):
    for ii, col_schema in enumerate(schemas):
        if col_schema.label_col:
            df.insert(loc=ii, column=col_schema.name, value=df.columns[ii])
        if col_schema.rename_col:
            df.rename(columns={df.columns[ii]: col_schema.name}, inplace=True)
        col = df.columns[ii]
        if col_schema.dtype.startswith("datetime"):
            df[col] = pd.to_datetime(
                df[col] + f" {col_schema.dtype[-4:]}", format="%a. %d %b %Y"
            )
        else:
            df[col] = df[col].astype(col_schema.dtype)

    return df


def fill_NaT(df: pd.DataFrame) -> pd.DataFrame:
    """
    This forwards fills the null values when the column is called 'date'
    """
    for col in df.columns:
        if col == "date":
            df[col] = df[col].ffill()
    return df
