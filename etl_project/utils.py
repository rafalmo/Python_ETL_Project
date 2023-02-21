from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import pandas as pd
from etl_project.error_handling import check_status


def date_spliter(date):
    return str(date.year), str(date.strftime("%m")), str(date.strftime("%d"))


def scrap_table(url, table_id):
    page = check_status(url)
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        table = soup.find(id=table_id)
        for data in table.find_all("tbody"):
            rows = data.find_all("tr")
    except:
        raise Exception("Data not found. Please use correct date range")
    
    return rows


def read_file_csv(df,url, encoding, delimiter, decimal,i=1):
    check_status(url)
    if i == 1:
        try:
            df = pd.read_csv(
                url,
                encoding=encoding,
                delimiter=delimiter,
                decimal=decimal,
            )
        except Exception as e:
            df = reject_cols(
                url,
                encoding=encoding,
                delimiter=delimiter,
                decimal=decimal,
            )
    else:
        # time.sleep(2.5)
        try:
            df2 = pd.read_csv(
                url,
                encoding=encoding,
                delimiter=delimiter,
                decimal=decimal,
            )
        except Exception as e:
            df2 = reject_cols(
                url,
                encoding=encoding,
                delimiter=delimiter,
                decimal=decimal,
            )

        df = pd.concat([df, df2], ignore_index=True)
        df2 = df2.iloc[0:0]
    return df


def reject_cols(url, encoding, delimiter, decimal, nrows=1):

    df = pd.read_csv(
        url, encoding=encoding, delimiter=delimiter, decimal=decimal, nrows=nrows
    )
    columns = df.columns.tolist()
    usecols = columns[: len(columns)]
    df = pd.read_csv(
        url, encoding=encoding, delimiter=delimiter, decimal=decimal, usecols=usecols
    )
    return df
