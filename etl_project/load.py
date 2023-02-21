import pandas as pd
import os


def load(df, report_name, index=True):
    path = "reports"
    isExist = os.path.exists(path)
    if isExist:
        df.to_csv(path + "/" + report_name + ".csv", index=index)
        print("Saved")
    else:
        try:
            os.makedirs(path)
            df.to_csv(path + "/" + report_name + ".csv", index=index)
            print("Saved")
        except Exception as e:
            raise Exception("Unable to save report to folder {path} ")
