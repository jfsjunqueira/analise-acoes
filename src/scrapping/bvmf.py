"""Scrapes """

from typing import List

from pandas import DataFrame, read_html

from src.config import BVMF_URL


def bvmf_scrap(cd_cvm: str) -> List[DataFrame]:
    """Scrapes certain characteristics about a company based on its
    CVM code.

    Args:
        cd_cvm (str): CVM code referent to a specific company.

    Returns:
        table_list: List with tables containing informations about a specific company.
            [0] - General Information
            [1] - Institution
            [2] - Balance sheet summary for last 2 years YTD
            [3] - Income statement summary for last 2 years YTD
            [4] - Cashflow summary for last 2 years YTD
            [5] - Shareholders
            [6] - Types of shareholders
            [7] - Types of shares
            
    """
    return read_html(BVMF_URL + str(cd_cvm))
