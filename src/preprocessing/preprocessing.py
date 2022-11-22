import pandas as pd
from pandas import DataFrame


def treat_value(_df: DataFrame) -> DataFrame:
    """This function takes the VL_CONTA on the dataframe to the same unit in all rows.

    Args:
        _df (DataFrame): Dataframe taken from CVMs website regarding companies DFP.

    Returns:
        DataFrame: Dataframe with correct values at the VL_CONTA column.
    """
    if "ESCALA_MOEDA" not in _df.columns:
        print("You need the column 'ESCALA_MOEDA' to be able to scale.")
        return _df
    _df["VL_CONTA"] = _df.apply(
        lambda x: x.VL_CONTA if x.ESCALA_MOEDA == "UNIDADE" else x.VL_CONTA * 1000,
        axis=1,
    )
    _df.drop(columns=["ESCALA_MOEDA"], inplace=True)
    return _df


def treat_date(_df: DataFrame, date_columns=None) -> DataFrame:
    """Treats date columns from a dataframe to be in datetime[ns] format.

    Args:
        _df (DataFrame): Target dataframe with date columns to treat.
        date_columns (_type_, optional): Group of columns to be treated.. Defaults to None.

    Returns:
        DataFrame: Original dataframe with date columns treated.
    """
    if date_columns is None:
        date_columns = []
    for col in date_columns:
        _df[col] = pd.to_datetime(_df[col])
    return _df


def filter_main_rows(df: DataFrame):
    return df[df["CD_CONTA"].str.len() == 4].copy()

