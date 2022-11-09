"""Scrapes """

from typing import List

import requests
from bs4 import BeautifulSoup

from src.config import BVMF_URL


def get_page(cd_cvm: str, bvmf_url=BVMF_URL) -> requests.models.Response:
    """Gets the BVMF page html code for the specified CD_CVM.

    Args:
        cd_cvm (str): CD_CVM that is used as ID for companies in CVM files.
        bvmf_url (str, optional): BVMF base website URL with information about the company. Defaults to BVMF_URL.

    Returns:
        requests.models.Response: Reponse object from the request.
    """
    return requests.get(bvmf_url + cd_cvm)


def scrap_ticker_list(bvmf_page: BeautifulSoup) -> List:
    """Scrapes the tickers of a company's page in BVMF.

    Args:
        bvmf_page (BeautifulSoup): BS4 object of the company's html code.

    Returns:
        List: List with all of the company's tickers.
    """
    raw_ticker_list = bvmf_page.find_all(class_="LinkCodNeg")
    return [ticker.contents[0] for ticker in raw_ticker_list]


def scrap_industry(bvmf_page: BeautifulSoup) -> List:
    """Scrapes the industry and sector especifications in a company's page in BVMF.

    Args:
        bvmf_page (BeautifulSoup): BS4 object of the company's html code.

    Returns:
        List: List with (1) Main activity and (2) Industry specification of the company.
    """
    raw_industry_list = bvmf_page.find(class_='ficha responsive').find_all('td')[-5:]
    return [raw_industry_list[0].contents[0], raw_industry_list[2].contents[0]]


# Not implemented yet!
def scrap_total_shares(bvmf_page: BeautifulSoup) -> List:
    pass
# soup.find(text=re.compile('Total de')).findParent().find_next_sibling().contents[0].replace('.','')