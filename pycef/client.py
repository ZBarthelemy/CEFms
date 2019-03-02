import requests
import bs4
from datetime import datetime
from pycef.fund import Fund
import pandas


class Client(object):
    _user_agent = "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36"

    def __init__(self):
        self.funds = {}
        self._client = requests.Session()
        self._client.headers = {
            'user-agent': self._user_agent,
            'X-Requested-With': 'XMLHttpRequest',
        }

    def get_fund_by_ticker(self, ticker: str) -> Fund or None:
        r = self._client.get('https://www.cefconnect.com/fund/' + ticker.upper(), timeout=30)
        if r.status_code != 200:
            return
        else:
            soup = bs4.BeautifulSoup(r.text, 'lxml')
            as_of_text = (soup.find("span", id="ContentPlaceHolder1_cph_main_cph_main_AsOfLabel")
                .text
                .split(' ')[2])
            as_of = datetime.strptime(as_of_text, '%m/%d/%Y').date()
            today_table_soup = soup.find(name='table', id='ContentPlaceHolder1_cph_main_cph_main_SummaryGrid')
            current_row = today_table_soup.findAll('tr')[1]
            row_columns = current_row.find_all('td')
            share_price = float(row_columns[1].text[1:])
            net_price = float(row_columns[2].text[1:])
            premium_p = float(row_columns[3].text[:-1]) / 100
            return Fund(name=ticker,
                        share_price=share_price,
                        net_asset_value=net_price,
                        current_premium_to_nav=premium_p,
                        as_of=as_of,
                        client=self._client)
