import pandas as pd

from extractor.model import SchemaModel
from extractor.transform import impose_df_schema


def test_impose_df_schema():
    df = pd.DataFrame(
        [
            ["EUR-USD", 1.08, -2.8, -0.2, 0.9],
            ["EUR-GBP", 0.8, -0.1, 0.92, 1.7],
        ],
        columns=["Exchange rates", "Price", "1M", "3M", "6M"],
    ).astype(object)

    expected = pd.DataFrame(
        [
            ["Exchange rates", "EUR-USD", "Price", 1.08, -2.8, -0.2, 0.9],
            ["Exchange rates", "EUR-GBP", "Price", 0.8, -0.1, 0.92, 1.7],
        ],
        columns=[
            "market",
            "asset",
            "current_value_label",
            "current_value",
            "1M",
            "3M",
            "6M",
        ],
    )

    schemas = [
        SchemaModel(name="market", dtype="object", label_col=True),
        SchemaModel(name="asset", dtype="object", rename_col=True),
        SchemaModel(name="current_value_label", dtype="object", label_col=True),
        SchemaModel(name="current_value", dtype="float", rename_col=True),
        SchemaModel(name="1M", dtype="float"),
        SchemaModel(name="3M", dtype="float"),
        SchemaModel(name="6M", dtype="float"),
    ]
    result = impose_df_schema(schemas=schemas, df=df)

    pd.testing.assert_frame_equal(result, expected)
