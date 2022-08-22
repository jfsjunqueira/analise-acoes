import pandas as pd
from pandas import DataFrame


def get_full_df():
    file_list = [name for name in os.listdir("../" + DATA_PATH) if name[-4:] != ".zip"]
    df = pd.DataFrame()
    for idx, file_name in enumerate(file_list):
        if idx == 0:
            df = read_cvm(parse_dre_filename(file_name))
        df = concat_dfs(
                df,
                read_cvm(parse_dre_filename(file_name))
                )
    return df

def concat_dfs(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    return pd.concat((df1, df2), ignore_index=True)

def parse_dre_filename(dir_name):
    return f"../{DATA_PATH}/{dir_name}/dfp_cia_aberta_DRE_con_{dir_name[-4:]}.csv"

def read_cvm(file_path):
    return pd.read_csv(file_path, delimiter=";", encoding="latin1")

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
    if date_columns is None:
        date_columns = []
    for col in date_columns:
        _df[col] = pd.to_datetime(_df[col])
    return _df


def filter_main_rows(df: DataFrame):
    return df[df['CD_CONTA'].str.len() == 4].copy()

