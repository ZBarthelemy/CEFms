import json
from datetime import date
import requests
from pandas.io.json import json_normalize

class Fund(object):
    def __init__(self,
                 name: str,
                 share_price: float,
                 net_asset_value: float,
                 current_premium_to_nav: float,
                 as_of: date,
                 client: requests.Session):
        self.name = name
        self.share_price = share_price
        self.net_asset_value = net_asset_value
        self.current_premium_to_nav = current_premium_to_nav
        self.as_of = as_of
        self._client = client

    def __eq__(self, other):
        if isinstance(other, Fund):
            return (self.name == other.name
                    and self.share_price == other.share_price
                    and self.net_asset_value == other.net_asset_value
                    and self.current_premium_to_nav == other.current_premium_to_nav
                    and self.as_of == other.as_of)
        return False

    def is_present_discount_2sigma_plus(self) -> bool:
        fund_history = "https://www.cefconnect.com/api/v3/pricinghistory/" + self.name.upper() + "/1Y"
        r = self._client.get(fund_history)
        payload = json.loads(r.content)
        df = json_normalize(payload['Data']['PriceHistory'])
        present_discount = df.DiscountData.iat[-1]
        st_dev = df.DiscountData.std()
        avg = df.DiscountData.mean()

        df.to_csv(r'/Users/whitestallion/Desktop/JPS.csv')
        if (avg - 2 * st_dev) > present_discount:
            return True
        else:
            return False
