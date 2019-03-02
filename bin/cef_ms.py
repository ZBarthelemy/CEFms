import logging
import pycef
from functional import seq


def main():
    fund_tickers = ["MHN", "MYN", "NVG", "NRK", "NAD", "RGT", "RMT", "JMF", "NML",
                    "JPS", "GGZ", "GDV", "GDL", "GGO", "NID", "BIT", "BTT"]
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: '
               '%(message)s'
    )
    c = pycef.Client()
    DiscountFundByName = (seq(fund_tickers)
                          .map(lambda f: c.get_fund_by_ticker(f))
                          .map(lambda f: {f.name: f.is_present_discount_2sigma_plus()})
                          .filter(lambda d: list(d.values())[0] == True))

    # Code above might not be thread safe.
    # should stick to the below.
    # funds: List[pycef.Fund] = map(lambda f: c.get_fund_by_ticker(f), fund_tickers)
    # isCheapByName = list(map(lambda f: {f.name: f.is_present_discount_2sigma_plus()}, funds))


if __name__ == '__main__':
    main()
