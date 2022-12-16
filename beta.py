from bs4 import BeautifulSoup
import requests
from BetaValue import BetaValue


# Gathering beta values by using requests to send request to http and use BeautifulSoup to parse the data
def get_html_and_parse_data(tickers):
    beta_values_list = []
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

    for i in range(len(tickers)):
        url = f"https://finance.yahoo.com/quote/{tickers[i]}/key-statistics?p={tickers[i]}"
        r = requests.get(url, headers=header)
        soup = BeautifulSoup(r.text, "html.parser")

        # Finding beta values and company name in web elements
        company_name = soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text
        company_beta = soup.find_all('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})[9].text

        beta_obj = BetaValue(company_name, company_beta)
        beta_values_list.append(beta_obj)

    return beta_values_list


# Sorting beta values list using bubblesort and return sorted list
def sort_beta_value(beta_list):
    for i in range(len(beta_list) - 1, 0, -1):
        for j in range(i):
            if beta_list[j] < beta_list[j + 1]:
                beta_list[j + 1], beta_list[j] = beta_list[j], beta_list[j + 1]

    return beta_list


def gather_beta_data(tickers):
    beta_values_list = get_html_and_parse_data(tickers)
    sorted_beta_list = sort_beta_value(beta_values_list)

    return sorted_beta_list
