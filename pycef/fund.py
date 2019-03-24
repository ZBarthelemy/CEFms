import json
from datetime import date
import requests
import pandas


class Fund(object):
    def __init__(self,
                 ticker: str,
                 name: str,
                 share_price: float,
                 net_asset_value: float,
                 current_premium_to_nav: float,
                 as_of: date,
                 client: requests.Session,
                 year_premium_st_dev,
                 year_premium_mean):
        self.ticker = ticker
        self.name = name
        self.share_price = share_price
        self.net_asset_value = net_asset_value
        self.current_premium_to_nav = current_premium_to_nav
        self.as_of = as_of
        self._client = client
        self.year_premium_st_dev = year_premium_st_dev
        self.year_premium_mean = year_premium_mean

    def __eq__(self, other):
        if isinstance(other, Fund):
            return (self.name == other.name
                    and self.share_price == other.share_price
                    and self.net_asset_value == other.net_asset_value
                    and self.current_premium_to_nav == other.current_premium_to_nav
                    and self.as_of == other.as_of)
        return False

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return ('Fund name:' + self.name + '<br> premium to nav: ' + (
                "%.2f" % self.current_premium_to_nav) + '%'
                + '<br>share_price:' + "{0:.2f}".format(self.share_price) + '<br>net_asset_value:' + "{0:.2f}".format(self.net_asset_value))

    def to_dict(self):
        return {
            'Name': self.name,
            'Ticker': self.ticker,
            'Date': self.as_of.strftime("%m-%d"),
            'M2M': "{0:.2f}".format(self.share_price),
            'Nav': "{0:.2f}".format(self.net_asset_value),
            'Premium': "{0:+.2f}".format(self.current_premium_to_nav),
            '52 wk avg': "{0:+.2f}".format(self.year_premium_mean),
            '1 Sigma': "{0:.2f}".format(self.year_premium_st_dev)
        }

    def is_present_discount_2sigma_plus(self) -> bool:
        fund_history = "https://www.cefconnect.com/api/v3/pricinghistory/" + self.ticker.upper() + "/1Y"
        r = self._client.get(fund_history)
        payload = json.loads(r.content)
        df: pandas.DataFrame = pandas.io.json.json_normalize(payload['Data']['PriceHistory'])
        present_discount = df.DiscountData.iat[-1]
        self.year_premium_mean = df.DiscountData.mean()
        self.year_premium_st_dev = df.DiscountData.std()
        if (self.year_premium_mean - 2 * self.year_premium_st_dev) > present_discount:
            return True
        else:
            return False
