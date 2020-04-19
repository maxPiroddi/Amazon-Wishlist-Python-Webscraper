import requests
from bs4 import BeautifulSoup
import json


def check_price(URL_LIST, headers):
    PRICE_LIST = []
    for URL in URL_LIST:
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find(id="productTitle")
        if(title != None):
            title = title.get_text().strip()
        else:
            title = 'Unknown title'

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
        pricelist_item = {'title': title,
                          'price': price, 'img': img_src, 'url': URL}

        PRICE_LIST.append(pricelist_item)
    return PRICE_LIST
