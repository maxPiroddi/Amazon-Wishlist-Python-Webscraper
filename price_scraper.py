import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os

SECONDS_IN_DAY = 86400
URL = 'https://www.amazon.com.au/Nintendo-Switch-Console-Lite-Turquoise/dp/B07V8MLT39/'
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}


def check_price():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text().strip()
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[1:7])

    if(converted_price < 350):
        send_email()


def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    login_email = os.environ.get('EMAIL_USER')
    login_password = os.environ.get('EMAIL_KEY')
    recipient_email = os.environ.get('EMAIL_RECIPIENT')

    server.login(login_email, login_password)

    subject = 'Your Daily Price Update'
    body = 'Check the amazon link https://www.amazon.com.au/Nintendo-Switch-Console-Lite-Turquoise/dp/B07V8MLT39/'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        login_email,
        recipient_email,
        msg
    )

    print('Email has been sent.')
    server.quit()

while(True):
    check_price()
    time.sleep(SECONDS_IN_DAY)
