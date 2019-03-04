import logging
import pycef
from functional import pseq, seq
from typing import List
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yaml
import os
import datetime


def send_email(user, pwd, recipient, subject, body):
    _to = recipient if isinstance(recipient, list) else [recipient]
    _text = MIMEText(body, 'html')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = ','.join(_to)
    html = """\
    <html>
        <head><b>The funds listed below are trading below 2nd st dev from 52 week avg. discount</b></head>
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
    discounted_funds: List[pycef.Fund] = list((pseq(fund_tickers)
                                               .map(lambda f: c.get_fund_by_ticker(f))
                                               .map(lambda f: {f: f.is_present_discount_2sigma_plus()})
                                               .filter(lambda d: list(d.values())[0] == True))
                                              .map(lambda d: list(d.keys())[0]))

    with open(os.path.join(os.getcwd(), *["bin", "prod.yaml"]), 'r') as stream:
        try:
            email_configs = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    if len(discounted_funds) == 0:
        logging.info("no discounted funds today")
    else:
        pay_load = '<br><br>'.join(list(seq(discounted_funds).map(lambda f: str(f))))
        # noinspection PyUnboundLocalVariable
        send_email(user=email_configs['email_login'],
                   pwd=email_configs["email_pwd"],
                   recipient=email_configs['recipient'],
                   subject="CEF daily report {}".format(datetime.date.today().strftime('%Y-%m-%d')),
                   body=pay_load)


if __name__ == '__main__':
    main()
