import typer
import sys
from etl_project.dictionary import URL_DICT
from etl_project.error_handling import check_value, check_date
from etl_project.etl import etl_process

cli = typer.Typer()


@cli.command()
def generate_report(report_number: int, start_date: str, end_date: str):
    """Generate a report"""
    try:
        report_name = check_value(URL_DICT, report_number)
    except Exception as e:
        print(e)
        sys.exit()
    try:
        start_date, end_date = check_date(start_date, end_date, URL_DICT, report_name)
    except Exception as e:
        print(e)
        sys.exit()
    try:
        etl_process(report_name, start_date, end_date)
    except Exception as e:
        print(e)
        sys.exit()


@cli.command()
def display_reports():
    """View all available reports"""
    for key, value in URL_DICT.items():
        print(f"{key}. {value[0]}")


if __name__ == "__main__":
    cli()
