"""Scrapes """

import re
from typing import List

import requests
from bs4 import BeautifulSoup

from src.config import BVMF_URL


def bvmf_scrap(cd_cvm: str) -> dict:
    """Scrapes certain characteristics about a company based on its
    CVM code.

    Args:
        cd_cvm (str): CVM code referent to a specific company.

    Returns:
        dict: Dictionary with informations about a specific company.
    """
    bvmf_page = BeautifulSoup(get_page(cd_cvm).text, 'html.parser')
    ticker_list = scrap_ticker_list(bvmf_page)
    industry = scrap_industry(bvmf_page)
    n_shares = scrap_total_shares(bvmf_page)
    company_dict = {
        "ticker": ticker_list,
        "activity": [industry[0]] * len(ticker_list),
        "industry": [industry[1]] * len(ticker_list),
        "ord_n": [n_shares[0]] * len(ticker_list),
        "pre_n": [n_shares[1]] * len(ticker_list),
    }
    return company_dict


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
    raw_industry_list = bvmf_page.find(class_="ficha responsive").find_all("td")[-5:]
    return [raw_industry_list[0].contents[0], raw_industry_list[2].contents[0]]


def scrap_total_shares(bvmf_page: BeautifulSoup) -> List:
    """Scrapes the number of ordinary and preferential shares of a company's page
    in BVMF website.

    Args:
        bvmf_page (BeautifulSoup): BS4 object of the company's html code.

    Returns:
        List: List with (1) Number of ordinary and (2) preferential shares.
    """
    ord_n = (
        bvmf_page.find(text=re.compile("Quantidade de AÃ§Ãµes Ord"))
        .findParent()
        .find_next_sibling()
        .contents[0]
        .replace(".", "")
    )
    pre_n = (
        bvmf_page.find(text=re.compile("Quantidade de AÃ§Ãµes Pre"))
        .findParent()
        .find_next_sibling()
        .contents[0]
        .replace(".", "")
    )
    return [ord_n, pre_n]
