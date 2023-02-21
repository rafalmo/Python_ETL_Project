from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import requests


def check_status(url):
    try:
        page = requests.get(url, timeout=600)
    except Exception:
        raise Exception("Timeout has been raised")
    if page.status_code == 404:
        raise Exception("404 Not Found. Please try again later")
    if page.status_code == 429:
        raise Exception("HTTP Error 429: Too Many Requests. Please try again later")
    if page.status_code == 400:
        raise Exception("Error 400: Bad Request")
    return page


def check_value(dict_url, x):
    if x in dict_url.keys():
        return dict_url[x][0]
    else:
        raise Exception(
            "Wrong number! Please select the correct number. You can check the available report numbers with the command: display_reports "
        )


def check_date(start_date, end_date, URL_DICT, report_name):
    today = datetime.today()
    date_hist = today - relativedelta(months=2)
    try:
        start_date = datetime.strptime(start_date, "%Y/%m/%d")
        end_date = datetime.strptime(end_date, "%Y/%m/%d")
    except Exception as e:
        raise Exception("Wrong date format! Enter the date in the format YYYY/MM/DD")
    if start_date >= end_date:
        raise Exception("End date must be greater than start date!")
    if end_date > today:
        raise Exception("End date cannot be greater than today!")
    if report_name == URL_DICT[3][0]:
        if start_date < date_hist:
            raise Exception(
                f"For the {report_name} report, start date must be greater than {date_hist.date()}!"
            )
    if start_date < datetime.strptime("2012/01/01", "%Y/%m/%d"):
        raise Exception("Start date must be greather than 2012/01/01!")

    return start_date, end_date
