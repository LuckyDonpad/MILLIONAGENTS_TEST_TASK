import requests
import fake_useragent
from bs4 import BeautifulSoup
from pprint import pformat

from requests import session

from card_parser import CardParser
from page_parser import PageParser
import utils
import argparse
from tqdm.asyncio import trange, tqdm
import aiohttp
import asyncio
import os
from file_saver import FileSaver


def parse_command_line():
    parser = argparse.ArgumentParser(
        prog='Metro parser',
        description='This program can parse products from Metro of chosen category.',
        epilog='Made by Donpad!',
        add_help=True)

    parser.add_argument('--url', type=str,
                        help='Base url for parsing example: '
                             '"https://online.metro-cc.ru/category/molochnye-prodkuty-syry-i-yayca/syry/polutverdye?from=under_search&in_stock=1"')
    parser.add_argument('--coords', type=str, help="Coords of shop, can be found in cookie 'coords'")
    parser.add_argument('--id', type=str, help="ID of shop, can be found in cookie 'metroStoreId'")
    parser.add_argument('--path', type=str, help="relative path to save htmls")
    parser.add_argument('--csv', type=str, help="relative path to save csv")
    parser.add_argument('--json', type=str, help="relative path to save json")

    args = parser.parse_args()
    return args


def get_urls(base_url, cookie, path):
    response = requests.get(base_url, headers=utils.get_fake_user_agent(), cookies=cookie).text
    with open(f"{path}/page_1.html", "w", encoding='utf-8') as file:
        file.write(response)
    soup = BeautifulSoup(response, 'lxml')

    pagecount = PageParser.parse_pagecount(soup)
    urls = utils.get_pages_url(base_url, pagecount)

    return urls


async def download_pages(urls, cookie, path):
    tasks = []

    async with aiohttp.ClientSession(cookies=cookie) as session:
        for i in range((len(urls))):
            task = asyncio.create_task(utils.download_task(i + 2, urls[i], session, path))
            tasks.append(task)
        await tqdm.gather(*tasks)


def main():
    args = parse_command_line()

    cookie = utils.get_cookie_from_args(args.coords, args.id)
    path = args.path
    os.makedirs(os.path.dirname(f"{path}/"), exist_ok=True)

    urls = get_urls(args.url, cookie, path)
    asyncio.run(download_pages(urls, cookie, path))

    pages_files = [f"{path}/page_1.html"]
    for i in range((len(urls))):
        pages_files.append(f"{path}/page_{i + 2}.html")

    cards = []
    brands = None
    for page in tqdm(pages_files):
        with open(page, "r", encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'lxml')
            if brands is None:
                brands = PageParser.parse_brands(soup)
            cards.extend(PageParser.parse_cards(soup))

    data = []
    for card in tqdm(cards):
        data.append(CardParser.parse(card, brands))

    if args.csv:
        FileSaver.save_csv(args.csv, data)
    if args.json:
        FileSaver.save_json(args.json, data)


if __name__ == '__main__':
    main()
