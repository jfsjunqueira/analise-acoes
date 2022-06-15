from pandas import DataFrame


def treat_value(_df: DataFrame) -> DataFrame:
    """This function takes the VL_CONTA on the dataframe to the same unit in all rows.

    Args:
        _df (DataFrame): Dataframe taken from CVMs website regarding companies DFP.

    Returns:
        DataFrame: Dataframe with correct values at the VL_CONTA column.
    """
    _df["VL_CONTA"] = _df.apply(
        lambda x: x.VL_CONTA if x.ESCALA_MOEDA == "UNIDADE" else x.VL_CONTA * 1000,
        axis=1,
    )
    _df.drop(columns=["ESCALA_MOEDA"], inplace=True)
    return _df

