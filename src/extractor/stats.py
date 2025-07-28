from typing import Optional

import pandas as pd


def get_top_bottom(
    df: pd.DataFrame,
    n: int = 3,
    label: str = "12M",
    store: bool = False,
    filename: Optional[str] = None,
) -> pd.DataFrame:
    """
    This returns the n top and bottom rows of a dataframe, ranked by the given
    label

    """
    top_bottom = pd.concat(
        [
            df.nlargest(n, label),
            df.nsmallest(n, label).sort_values(by=label, ascending=False),
        ],
        ignore_index=True,
    )
    if store:
        top_bottom.to_csv(filename, sep="\t", index=False)
        print(
            f"top and bottom {n} ranked by metric {label} exported onto {filename}"
        )
    return top_bottom
