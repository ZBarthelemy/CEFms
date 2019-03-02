import unittest
import requests_mock
import os
import pycef
from pycef import Fund
from datetime import date
import requests


class TestClient(unittest.TestCase):

    @requests_mock.Mocker()
    def setUp(self, mock_client):
        directory_path = os.path.dirname(__file__)
        self.system_path = os.getcwd()
        self.fixture_path = os.path.join(directory_path, 'fixtures/')
        self.mock_client = mock_client

        self.mock_cef_client = pycef.Client()

    def test_get_fund_data_when_return_normal_data_expect_fund(self):
        mq = self.mock_cef_client
        with requests_mock.Mocker() as m:
            m.get('https://www.cefconnect.com/fund/JPS',
                  content=open(self.fixture_path + 'jps.resp', 'rb').read())
            actual_f: Fund = mq.get_fund_by_ticker(ticker='jps')
        expected_f = Fund(name="jps",
                          share_price=9.06,
                          net_asset_value=9.46,
                          current_premium_to_nav=-0.042300000000000004,
                          as_of=date(2019, 2, 28),
                          client=requests.Session())
        self.assertEquals(actual_f, expected_f)

    def test_get_fund_data_when_return_no_data_expect_none(self):
        mq = self.mock_cef_client
        with requests_mock.Mocker() as m:
            m._adapter.register_uri('GET',
                                    'https://www.cefconnect.com/fund/JPS',
                                    text='Server side error',
                                    status_code=500)
            actual_f = mq.get_fund_by_ticker(ticker='jps')
        self.assertEquals(actual_f, None)

    def test_is_present_discount_2_sigma_when_cef_is_not_more_than_2_st_dev_from_mean_expect_false(self):
        mq = self.mock_cef_client
        with requests_mock.Mocker() as m:
            m.get('https://www.cefconnect.com/fund/JPS',
                  content=open(self.fixture_path + 'jps.resp', 'rb').read())
            m.get('https://www.cefconnect.com/api/v3/pricinghistory/JPS/1Y',
                  content=open(self.fixture_path + 'jps_1y_2019_03_01.json', 'rb').read())
            f: Fund = mq.get_fund_by_ticker(ticker='jps')
            actual = f.is_present_discount_2sigma_plus()
        self.assertFalse(actual)

    def test_is_present_discount_2_sigma_when_cef_is_more_than_2_st_dev_from_mean_expect_true(self):
        mq = self.mock_cef_client
        with requests_mock.Mocker() as m:
            m.get('https://www.cefconnect.com/fund/JPS',
                  content=open(self.fixture_path + 'jps.resp', 'rb').read())
            m.get('https://www.cefconnect.com/api/v3/pricinghistory/JPS/1Y',
                  content=open(self.fixture_path + 'jps_1y_2019_12_21.json', 'rb').read())
            f: Fund = mq.get_fund_by_ticker(ticker='jps')
            actual = f.is_present_discount_2sigma_plus()
        self.assertTrue(actual)
