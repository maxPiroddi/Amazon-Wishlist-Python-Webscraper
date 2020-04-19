import price_scraper
import email_service
import os

URL_LIST = [
    'https://www.amazon.com.au/Nintendo-Switch-Console-Lite-Turquoise/dp/B07V8MLT39/',
    'https://www.amazon.com.au/Animal-Crossing-New-Horizons-Nintendo/dp/B083TYVJ22',
    'https://www.amazon.com.au/Legend-Zelda-Breath-Wild/dp/B076P6K4YT',
    'https://www.amazon.com.au/Nintendo-Switch-Neon-Blue-Joy/dp/B01MUAGZ49',
]

headers = {
    "User-Agent": os.environ.get('USER_AGENT')}

PRICE_LIST = price_scraper.check_price(URL_LIST, headers)
# print(PRICE_LIST)
email_service.send_email(PRICE_LIST)
