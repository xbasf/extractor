import pandas as pd
import numpy as np
from typing import List


def split_on_blank_row(df: pd.DataFrame) -> List[pd.DataFrame]:
    """
    This splits a dataframe in two anytime there is a row full of blank values
    returning a list of dataframes. The first row of the new dataframes becomes
    the dataframe column labels.

    """

    split_positions = df.index[df.isna().all(axis=1)]
    dfs = np.split(df, split_positions, axis=0)

    if len(dfs) == 1:
        return dfs

    clean_dfs = [dfs[0]]
    for df in dfs[1:]:
        clean_df = df.dropna(how="all", axis=0)
        clean_df = shift_up(clean_df)
        clean_dfs.append(clean_df)

    return clean_dfs


def has_multiple_label(df: pd.DataFrame) -> bool:
    """
    This checks if the dataframe has more than one label by checking if the
    contents of the first row contain no numbers at all
    """

    for el, is_null in zip(df.iloc[0], df.iloc[0].isna()):
        if is_null:
            continue
        try:
            float(el)
            return False
        except ValueError:
            continue
    return True


def shift_up(df: pd.DataFrame) -> pd.DataFrame:
    """
    This moves all the cells of a dataframe up by 1, meaning that the first
    row becomes the dataframe column names, the second row becomes first row
    and so on
    """
    df.columns = df.iloc[0].to_numpy()
    df = df.drop(df.index[0])
    df = df.reset_index(drop=True)
    return df


def remove_blank_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    This removes a column of the given dataframe if the column contains just
    null values
    """
    return df.dropna(how="all", axis=1)
