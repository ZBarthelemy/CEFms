from datetime import date


class Fund(object):
    def __init__(self,
                 name: str,
                 share_price: float,
                 net_asset_value: float,
                 current_premium_to_nav: float,
                 as_of: date):
        self.name = name,
        self.share_price = share_price,
        self.net_asset_value = net_asset_value,
        self.current_premium_to_nav = current_premium_to_nav
        self.as_of = as_of
