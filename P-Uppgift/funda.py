from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
import requests


@dataclass
class FundamentalData:
    company: str
    t_ppe: str
    f_ppe: str
    pps: str


def gather_funda_info(ticker):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    url = f"https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}"

    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, "html.parser")

    funda_info = FundamentalData(
        company=soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text,
        t_ppe=soup.find_all('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})[2].text,
        f_ppe=soup.find_all('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})[3].text,
        pps=soup.find_all('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})[5].text
    )
    return asdict(funda_info)
