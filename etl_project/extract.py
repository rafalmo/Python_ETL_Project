import pandas as pd
from datetime import timedelta
from etl_project.utils import read_file_csv, scrap_table , date_spliter
import requests
from datetime import date, datetime
import time


def extract_link(url_raw, encoding, delimiter, decimal, start_date, end_date):
    check, i, delta, temp_date = True, 0, timedelta(days=30), start_date
    df=[]
    while check == True:
        i += 1
        start_year, start_month, start_day = date_spliter(start_date)
        temp_date += delta
        if temp_date < end_date:
            end_year, end_month, end_day = date_spliter(temp_date - timedelta(days=1))
        else:
            end_year, end_month, end_day = date_spliter(end_date)
            check = False
        url = f"{url_raw}{start_year}{start_month}{start_day}/data_do/{end_year}{end_month}{end_day}"
        df = read_file_csv(df,url, encoding, delimiter, decimal,i)
        start_date += delta
    return df


def extract_contract(url_raw, start_date, end_date, table_id):

    delta = timedelta(days=1)
    raw_list = []

    while start_date.date() <= end_date.date():
        year, month, day = date_spliter(start_date)
        url = f"{url_raw}{day}-{month}-{year}&dateAction=prev"
        rows = scrap_table(url, table_id)

        for row in rows:
            godzina = row.find_all("td")[0].text.strip()
            fixingI_kurs = row.find_all("td")[1].text.strip()
            fixingI_wolumen = row.find_all("td")[2].text.strip()
            fixingII_kurs = row.find_all("td")[3].text.strip()
            fixingII_wolumen = row.find_all("td")[4].text.strip()
            notowania_kurs = row.find_all("td")[5].text.strip()
            notowania_wolumen = row.find_all("td")[6].text.strip()
            raw_list.append(
                {
                    "Data": start_date.date(),
                    "Godzina": godzina,
                    "Fixing I Kurs(PLN/MWh)": fixingI_kurs,
                    "Fixing I Wolumen(MWh)": fixingI_wolumen,
                    "Fixing II Kurs(PLN/MWh)": fixingII_kurs,
                    "Fixing II Wolumen(MWh)": fixingII_wolumen,
                    "Notowania ciągłe Kurs (PLN/MWh)": notowania_kurs,
                    "Notowania ciągłe Wolumen (MWh)": notowania_wolumen,
                }
            )
        start_date += delta
    return pd.DataFrame(raw_list)
