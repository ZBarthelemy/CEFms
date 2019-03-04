import yaml
import os
import logging
import pycef
import smtplib
import pandas
import datetime
from typing import List
from functional import pseq
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(user, pwd, recipient, subject, body):
    _to = recipient if isinstance(recipient, list) else [recipient]
    _text = MIMEText(body, 'html')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = ','.join(_to)
    html = """\
    <html>
        <head>Please find the bi - weekly CEF report below</head>
        <body>
            <br>
            """ + body + """
        </body>
    </html>
    """
    embedded_payload = MIMEText(html, 'html')
    msg.attach(embedded_payload)
    try:
        mail_client = smtplib.SMTP("smtp.gmail.com", 587)
        mail_client.ehlo()
        mail_client.starttls()
        mail_client.login(user, pwd)
        mail_client.sendmail(user, _to, msg.as_string())
        mail_client.close()
        print('successfully sent the mail')
    except Exception as e:
        print(e)


def main():
    fund_tickers = ["MHN", "MYN", "NVG", "NRK", "NAD", "RGT", "RMT", "JMF", "NML",
                    "JPS", "GGZ", "GDV", "GDL", "GGO", "NID", "BIT", "BTT"]
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: '
               '%(message)s'
    )
    c = pycef.Client()
    all_funds_json: List[dict] = list((pseq(fund_tickers)
                                       .map(lambda f: c.get_fund_by_ticker(f))
                                       .map(lambda f: {f: f.is_present_discount_2sigma_plus()}))
                                      .map(lambda d: (list(d.keys())[0]).to_dict()))
    all_funds_df = (pandas.io.json.json_normalize(all_funds_json)
                    [['Name', 'Ticker', 'Date', 'M2M', 'Nav', 'Premium', '52 wk avg', 'Sigma']])
    pay_load = '<br><br>' + all_funds_df.to_html(index=False)

    with open(os.path.join(os.getcwd(), *["bin", "prod.yaml"]), 'r') as stream:
        try:
            email_configs = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    # noinspection PyUnboundLocalVariable
    send_email(user=email_configs['email_login'],
               pwd=email_configs["email_pwd"],
               recipient=email_configs['recipient'],
               subject="CEF bi-weekly report {}".format(datetime.date.today().strftime('%Y-%m-%d')),
               body=pay_load)


if __name__ == '__main__':
    main()
