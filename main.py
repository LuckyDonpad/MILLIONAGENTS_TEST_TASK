import requests
import fake_useragent
from bs4 import BeautifulSoup
from pprint import pformat

import card_parser
from card_parser import CardParser
from page_parser import PageParser

user_agent = fake_useragent.UserAgent().random
headers = {"User-Agent": user_agent}

# url = "https://online.metro-cc.ru/category/molochnye-prodkuty-syry-i-yayca/syry/polutverdye?from=under_search&page=2"
# response = requests.get(url, headers=headers)

with open("response_page2.html", "r", encoding='utf-8') as file:
    response = file.read()
soup = BeautifulSoup(response, 'lxml')
cards = PageParser.parse_cards(soup)

brands = PageParser.parse_brands(soup)

print(pformat(CardParser.parse(cards[0], brands)))
