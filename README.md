# Installation:
1. Create a Python virtual environment and activate it:
    $ cd Python_ETL_Project/
    $ python -m venv ./venv
    $ .\venv\Scripts\activate
2. Install the dependencies:
    python -m pip install -r requirements.txt
# Usage:
1. You can get the list of available commands using:
python -m etl_project --help   
2. Command shown below returns list of available reports with their number (you will need this number to generate the report). This command doesn't require any arguments.
python -m etl_project display-reports
3. You can generate report by using command:
python -m etl_project generate-report report_number YYYY/MM/DD YYYY/MM/DD. 
For example, command:
python -m etl_project generate-report 2 2022/10/29 2022/10/31
returns report for 'Krajowe zapotrzebowanie na moc' from date range 2022/10/29-2022/10/31. It is important to use format YYYY/MM/DD. Additionaly, the end date must be greather than the start date. You can check the report number by using previous command "display-reports".
4. Report will be saved to folder /reports as a .csv file.