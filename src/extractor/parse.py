import pandas as pd
import tabula


def parse_pdf(filename: str, page_num: int) -> pd.DataFrame:
    """
    This parses the data from 'filename' shown on page 'page_num' and
    returns it in a dataframe
    """
    return tabula.read_pdf(input_path=filename, pages=page_num)[0]
