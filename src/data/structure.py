""" Structure dataset with all csvs. """
import os

import pandas as pd

DATA_PATH = "data"


def create_pt(df):
    """
    Creates Pivot table from full df.
    """
    base_df = df.fillna(0).copy()
    base_df.VL_CONTA = base_df.VL_CONTA / 1_000_000
    structured_table = (
        base_df.pivot_table(
            values="VL_CONTA", index=["DENOM_CIA", "DT_REFER"], columns=["CD_CONTA"]
        )
        .reset_index()
        .fillna(1)
    )
    return structured_table


def get_full_df():
    """
    Structures dataframe with all csv files in data folder.

    Returns:
        pd.DataFrame: Dataframe with all registries of the csv files.
    """
    file_list = [name for name in os.listdir("../" + DATA_PATH) if name[-4:] != ".zip"]

    csv_list = []
    csv_list.extend([parse_dre_filename(file_name) for file_name in file_list])
    csv_list.extend([parse_bpa_filename(file_name) for file_name in file_list])
    csv_list.extend([parse_bpp_filename(file_name) for file_name in file_list])

    df = pd.DataFrame()
    for idx, file_name in enumerate(csv_list):
        if idx == 0:
            df = read_cvm(file_name)
        df = concat_dfs(df, read_cvm(file_name))
    return df


def concat_dfs(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    return pd.concat((df1, df2), ignore_index=True)


def parse_dre_filename(dir_name):
    return f"../{DATA_PATH}/{dir_name}/dfp_cia_aberta_DRE_con_{dir_name[-4:]}.csv"


def parse_bpa_filename(dir_name):
    return f"../{DATA_PATH}/{dir_name}/dfp_cia_aberta_BPA_con_{dir_name[-4:]}.csv"


def parse_bpp_filename(dir_name):
    return f"../{DATA_PATH}/{dir_name}/dfp_cia_aberta_BPP_con_{dir_name[-4:]}.csv"


def read_cvm(file_path):
    return pd.read_csv(file_path, delimiter=";", encoding="latin1")
