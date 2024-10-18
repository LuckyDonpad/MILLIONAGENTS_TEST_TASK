import requests
import fake_useragent
from bs4 import BeautifulSoup
from card_parser import CardParser

user_agent = fake_useragent.UserAgent().random
headers = {"User-Agent": user_agent}

# url = "https://online.metro-cc.ru/category/molochnye-prodkuty-syry-i-yayca/syry/polutverdye?from=under_search&page=2"
# response = requests.get(url, headers=headers)

with open("response_page2.html", "r", encoding='utf-8') as file:
    response = file.read()
soup = BeautifulSoup(response, 'lxml')
cards = soup.find_all('div', class_='product-card__content')

print(CardParser.parse_link(cards[5]))
print(CardParser.parse_name(cards[5]))
print(CardParser.parse_actual_price(cards[5]))
print(CardParser.parse_old_price(cards[5]))

