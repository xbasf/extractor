try:
    from .extractor import ExtractorManager
    from .model import PdfPageModel
    from .stats import get_top_bottom
except ImportError:
    from model import PdfPageModel
    from stats import get_top_bottom

    from extractor import ExtractorManager


def run(config_filename: str):

    pdf_page_model = PdfPageModel.from_yaml(filename=config_filename)

    extractor_mng = ExtractorManager(pdf_model=pdf_page_model)
    extractor_mng.get_raw_dfs()
    extractor_mng.clean_dfs()
    extractor_mng.impose_schema()
    extractor_mng.concat_dfs()
    extractor_mng.to_csv()

    extracted_df = extractor_mng.df_postproc

    if pdf_page_model.get_stats:
        _ = get_top_bottom(
            df=extracted_df,
            store=True,
            filename=pdf_page_model.output_stats_filename,
        )


if __name__ == "__main__":

    run(config_filename="src/extractor/config2.yaml")
    run(config_filename="src/extractor/config3.yaml")
