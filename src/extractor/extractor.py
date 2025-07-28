import pandas as pd

try:
    from .clean import (
        basic_formating,
        collapse,
        has_multiple_label,
        remove_blank_col,
        shift_up,
        split_on_blank_row,
    )
    from .model import PdfPageModel
    from .parse import parse_pdf
    from .transform import fill_NaT, impose_df_schema
except ImportError:
    from clean import (
        basic_formating,
        collapse,
        has_multiple_label,
        remove_blank_col,
        shift_up,
        split_on_blank_row,
    )
    from model import PdfPageModel
    from parse import parse_pdf
    from transform import fill_NaT, impose_df_schema


class ExtractorManager:
    def __init__(self, pdf_model: PdfPageModel):
        self.pdf = pdf_model
        self.raw_df = None
        self.dfs = None
        self.dfs_schema = None
        self.df_postproc = None

    def get_raw_dfs(self):
        try:
            self.raw_df = parse_pdf(
                filename=self.pdf.filename, page_num=self.pdf.data_page
            )
        except Exception as e:
            print(e)

    def clean_dfs(self):
        if self.raw_df is None:
            print("No data to clean")
            return None

        dfs = split_on_blank_row(df=self.raw_df)
        dfs_clean = []
        for df in dfs:
            if has_multiple_label(df=df):
                strategy = self.pdf.multiple_label_merge_strategy
                if strategy == "shift_up":
                    df = shift_up(df=df)
                elif strategy == "collapse":
                    df = collapse(df=df)
            df = remove_blank_col(df=df)
            df = basic_formating(df=df)
            dfs_clean.append(df)
        self.dfs = dfs_clean

    def impose_schema(self):
        if self.pdf.schemas is None:
            print("No schema supplied")
            return None

        dfs_schema = []
        for df in self.dfs:
            df_schema = impose_df_schema(schemas=self.pdf.schemas, df=df)
            df_schema = fill_NaT(df=df_schema)
            dfs_schema.append(df_schema)

        self.dfs_schema = dfs_schema

    def concat_dfs(self):
        if self.dfs_schema is not None:
            dfs = self.dfs_schema
        elif self.dfs is not None:
            dfs = self.dfs
        else:
            return None

        self.df_postproc = pd.concat(dfs, ignore_index=True)

    def to_csv(self):
        if self.df_postproc is None:
            print("No postprocessed df")
            return None

        self.df_postproc.to_csv(self.pdf.output_filename, sep="\t", index=False)
        print(f"extracted data exported onto {self.pdf.output_filename}")
