from etl_project.extract import extract_link, extract_contract
from etl_project.dictionary import URL_DICT
from etl_project import transform
from etl_project.load import load


def etl_process(report_name, start_date, end_date):
    print("The report is being created. Please wait...")
    if report_name == URL_DICT[1][0]:
        df = extract_link(URL_DICT[1][1], "cp1250", ";", ",", start_date, end_date)
        df = transform.transform_PL_GEN_MOC(df)
        load(df, report_name)
    elif report_name == URL_DICT[2][0]:
        df = extract_link(URL_DICT[2][1], "cp1250", ";", ",", start_date, end_date)
        df = transform.transform_PL_WYK_KSE(df)
        load(df, report_name, False)
    elif report_name == URL_DICT[3][0]:
        df = extract_contract(
            URL_DICT[3][1], start_date, end_date, "footable_kontrakty_godzinowe"
        )
        df = transform.transform_contract(df)
        load(df, report_name, False)
