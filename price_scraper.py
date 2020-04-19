import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os
import json

SECONDS_IN_DAY = 86400
URL_LIST = [
    'https://www.amazon.com.au/Nintendo-Switch-Console-Lite-Turquoise/dp/B07V8MLT39/',
    'https://www.amazon.com.au/Animal-Crossing-New-Horizons-Nintendo/dp/B083TYVJ22',
    'https://www.amazon.com.au/Legend-Zelda-Breath-Wild/dp/B076P6K4YT',
    'https://www.amazon.com.au/Nintendo-Switch-Neon-Blue-Joy/dp/B01MUAGZ49',
]

headers = {
    "User-Agent": os.environ.get('USER_AGENT')}

PRICE_LIST = []

def check_price():
    for URL in URL_LIST:
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find(id="productTitle").get_text().strip()
        price = soup.find(id="priceblock_ourprice")
        if(price != None):
            price = price.get_text()
            price = float(price[1:7])
        else:
            price = 'Out of stock'

        image = soup.find(id="imgTagWrapperId").findChildren(
            'img', recursive=False)[0]['data-a-dynamic-image']
        img_load = json.loads(image)
        img_src = list(img_load.keys())[0]
        pricelist_item = {'title': title, 'price': price, 'img': img_src, 'url': URL}

        PRICE_LIST.append(pricelist_item)
        print(PRICE_LIST)


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


# while(True):
check_price()
# time.sleep(SECONDS_IN_DAY)
