import numpy as np
import pandas as pd
import pytest

from extractor.clean import (has_multiple_label, remove_blank_col, shift_up,
                             split_on_blank_row)


@pytest.fixture
def df1():
    return pd.DataFrame(
        [
            [np.nan, "Current", np.nan],
            ["Commodities", "Price", "1M"],
            ["gold", 1234, 10],
        ],
        columns=["Unnamed: 0", "Current", "Unnamed: 1"],
    ).astype(object)


@pytest.fixture
def df2():
    return pd.DataFrame(
        [
            ["EUR-USD", 1.08, -2.8],
        ],
        columns=["Exchange rates", "Price", "1M"],
    ).astype(object)


@pytest.fixture
def df1_df2_concat():
    return pd.DataFrame(
        [
            [np.nan, "Current", np.nan],
            ["Commodities", "Price", "1M"],
            ["gold", 1234, 10],
            [np.nan, np.nan, np.nan],
            ["Exchange rates", "Price", "1M"],
            ["EUR-USD", 1.08, -2.8],
        ],
        columns=["Unnamed: 0", "Current", "Unnamed: 1"],
    ).astype(object)


def test_split_on_blank_row__df_with_no_splits(df1: pd.DataFrame):

    result = split_on_blank_row(df1)
    assert isinstance(result, list)
    assert len(result) == 1
    pd.testing.assert_frame_equal(result[0], df1)


def test_split_on_blank_row__df_with_splits(
    df1: pd.DataFrame, df2: pd.DataFrame, df1_df2_concat: pd.DataFrame
):

    result = split_on_blank_row(df1_df2_concat)
    assert isinstance(result, list)
    assert len(result) == 2
    pd.testing.assert_frame_equal(result[0], df1)
    pd.testing.assert_frame_equal(result[1], df2)


@pytest.mark.parametrize(
    "df, expected",
    [("df1", True), ("df2", False)],
)
def test_has_multiple_label(df: pd.DataFrame, expected: bool, request):
    result = has_multiple_label(request.getfixturevalue(df))
    assert result == expected


def test_shift_up(df1: pd.DataFrame):

    expected = pd.DataFrame(
        [
            ["Commodities", "Price", "1M"],
            ["gold", 1234, 10],
        ],
        columns=[np.nan, "Current", np.nan],
    ).astype(object)

    result = shift_up(df1)
    assert len(result) == (len(df1) - 1)
    pd.testing.assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "df, input_is_fixture, expected",
    [
        ("df1", True, "df1"),
        (
            pd.DataFrame(
                [
                    [np.nan, "Current", np.nan],
                    ["Commodities", "Price", np.nan],
                    ["gold", 1234, np.nan],
                ],
                columns=["Unnamed: 0", "Current", "Unnamed: 1"],
            ).astype(object),
            False,
            pd.DataFrame(
                [
                    [np.nan, "Current"],
                    ["Commodities", "Price"],
                    ["gold", 1234],
                ],
                columns=["Unnamed: 0", "Current"],
            ).astype(object),
        ),
    ],
)
def test_remove_blank_col(
    df: pd.DataFrame, input_is_fixture: bool, expected: pd.DataFrame, request
):
    if input_is_fixture:
        df = request.getfixturevalue(df)
        expected = request.getfixturevalue(expected)
    result = remove_blank_col(df)

    pd.testing.assert_frame_equal(result, expected)
