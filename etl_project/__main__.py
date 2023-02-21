from etl_project import cli, __app_name__, etl


def main():
    cli.cli(prog_name=__app_name__)


if __name__ == "__main__":
    main()
