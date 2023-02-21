import pandas as pd
import numpy as np
from etl_project.dictionary import POLISH_NAME_OF_WEEK


def transform_PL_GEN_MOC(df):
    df = df.fillna(0)
    df = df.melt(
        id_vars=["Doba", "Data publikacji", "Kod", "Nazwa", "Tryb pracy"],
        var_name="godzina",
    )
    df = (
        df.groupby(["Doba", "Kod", "Nazwa", "Tryb pracy"])["value"]
        .agg(
            Suma_Wygenerowanych_Wartosci_W_Ciagu_Dnia="sum",
            Srednia_Wygenerowanych_Wartosci_Na_Godzine="mean",
            Max_Wygenerowanych_Wartosci_Na_Godzine="max",
            Min_Wygenerowanych_Wartosci_Na_Godzine="min",
        )
        .round(3)
    )

    return df


def transform_PL_WYK_KSE(df):
    df = df.fillna(0)
    df["Data"] = pd.to_datetime(df["Data"])
    df["Dzien tygodnia"] = df["Data"].dt.day_name()
    df["Krajowe saldo wymiany miedzysystemowej sumarycznie"] = (
        df["Krajowe saldo wymiany międzysystemowej równoległej"]
        + df["Krajowe saldo wymiany międzysystemowej nierównoległej"]
    ).round(3)
    df["Liczba dni z ujemnym bilansem wymiany"] = [
        0 if x > 0 else 1
        for x in df["Krajowe saldo wymiany miedzysystemowej sumarycznie"]
    ]
    df = df.groupby("Godzina", group_keys=False).apply(min_day)
    df["Dzien Tygodnia z najmniejszym bilansem"] = df[
        "Dzien Tygodnia z najmniejszym bilansem"
    ].map(POLISH_NAME_OF_WEEK)
    df = (
        df.groupby(["Godzina", "Dzien Tygodnia z najmniejszym bilansem"])
        .agg(
            {
                "Krajowe zapotrzebowanie na moc": ["mean", "min", "max"],
                "Krajowe saldo wymiany miedzysystemowej sumarycznie": [
                    "mean",
                    "min",
                    "max",
                ],
                "Liczba dni z ujemnym bilansem wymiany": "sum",
            }
        )
        .round(3)
    )
    df.columns = [x + " " + y.capitalize() for x, y in df.columns]
    df.reset_index(inplace=True)
    df["rn"] = df["Godzina"].str.split("A").str[0].astype(float)
    df = df.sort_values("rn")
    df = df.drop("rn", axis=1)
    return df


def min_day(df):
    df["Dzien Tygodnia z najmniejszym bilansem"] = (
        df.sort_values(["Krajowe saldo wymiany miedzysystemowej sumarycznie"])
        .head(1)["Dzien tygodnia"]
        .squeeze()
    )
    return df


def transform_contract(df):
    df = df.fillna(0)
    df["Notowania ciągłe Kurs (PLN/MWh)"] = df[
        "Notowania ciągłe Kurs (PLN/MWh)"
    ].str.replace("-", "0")

    list_column_to_convert = [
        "Fixing I Kurs(PLN/MWh)",
        "Fixing I Wolumen(MWh)",
        "Fixing II Kurs(PLN/MWh)",
        "Fixing II Wolumen(MWh)",
        "Notowania ciągłe Kurs (PLN/MWh)",
        "Notowania ciągłe Wolumen (MWh)",
    ]

    df[list_column_to_convert] = df[list_column_to_convert].apply(
        lambda x: x.str.replace("-", "0")
    )

    df[list_column_to_convert] = df[list_column_to_convert].apply(
        lambda x: x.str.replace(",", ".").astype(float)
    )

    df = (
        df.groupby(["Godzina"])
        .agg(
            {
                "Fixing I Kurs(PLN/MWh)": ["mean", "min", "max"],
                "Fixing I Wolumen(MWh)": ["mean", "min", "max"],
                "Fixing II Kurs(PLN/MWh)": ["mean", "min", "max"],
                "Fixing II Wolumen(MWh)": ["mean", "min", "max"],
                "Notowania ciągłe Kurs (PLN/MWh)": ["mean", "min", "max"],
                "Notowania ciągłe Wolumen (MWh)": ["mean", "min", "max"],
            }
        )
        .round(3)
    )
    df.columns = [x + " " + y.capitalize() for x, y in df.columns]
    df = df.reset_index()

    df["rn"] = df["Godzina"].str.split("-").str[0].astype(float)

    df = df.sort_values("rn")
    df = df.drop("rn", axis=1)
    return df
